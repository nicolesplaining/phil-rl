"""Small chat-completions client for a local vLLM server or compatible endpoint."""

import json
from dataclasses import dataclass
from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class GenerationError(RuntimeError):
    def __init__(self, message: str, attempts: list | None = None):
        super().__init__(message)
        self.attempts = attempts or []


@dataclass(frozen=True)
class ModelConfig:
    base_url: str = "http://127.0.0.1:8000/v1"
    model: str = "Qwen/Qwen3-32B"
    api_key: str | None = None
    max_tokens: int = 8192
    temperature: float = 0.0
    seed: int = 0
    timeout: float = 180.0
    retries: int = 2
    structured: bool = True
    qwen_nonthinking: bool = True

    def __post_init__(self):
        if self.retries < 0 or self.retries > 5:
            raise ValueError("retries must be between 0 and 5.")
        if self.timeout <= 0 or self.max_tokens <= 0:
            raise ValueError("timeout and max_tokens must be positive.")
        url = httpx.URL(self.base_url)
        if url.scheme not in {"http", "https"} or not url.host or url.username or url.password:
            raise ValueError("Use an HTTP(S) base URL without embedded credentials.")

    def public(self) -> dict:
        # Never persist credentials, query strings, or URL userinfo in run artifacts.
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "seed": self.seed,
            "structured": self.structured,
            "qwen_nonthinking": self.qwen_nonthinking,
        }


class ChatClient:
    def __init__(self, config: ModelConfig, transport=None):
        self.config = config
        self.transport = transport

    def generate(
        self, schema: type[T], system: str, payload: dict, validate=None
    ) -> tuple[T, list]:
        config = self.config
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ]
        if not config.structured:
            messages[0]["content"] += "\nJSON schema:\n" + json.dumps(schema.model_json_schema())
        attempts = []
        headers = {"Authorization": f"Bearer {config.api_key}"} if config.api_key else {}
        with httpx.Client(timeout=config.timeout, transport=self.transport) as client:
            for attempt in range(config.retries + 1):
                body = {
                    "model": config.model,
                    "messages": messages,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "seed": config.seed,
                }
                if config.qwen_nonthinking:
                    body["chat_template_kwargs"] = {"enable_thinking": False}
                if config.structured:
                    body["response_format"] = {
                        "type": "json_schema",
                        "json_schema": {
                            "name": schema.__name__,
                            "schema": schema.model_json_schema(),
                        },
                    }
                try:
                    response = client.post(
                        config.base_url.rstrip("/") + "/chat/completions",
                        json=body,
                        headers=headers,
                    )
                except httpx.HTTPError as error:
                    # Library exception strings may contain credential-bearing URLs.
                    raise GenerationError(
                        f"Model request failed ({type(error).__name__})."
                    ) from None
                if response.is_error:
                    raise GenerationError(f"Model endpoint returned HTTP {response.status_code}.")
                try:
                    data = response.json()
                    choice = data["choices"][0]
                    if choice.get("finish_reason") not in {"stop", None}:
                        raise GenerationError(
                            "Model generation did not finish; increase max_tokens."
                        )
                    content = choice["message"]["content"]
                    if not isinstance(content, str) or not content.strip():
                        raise GenerationError("Model returned no text content.")
                except (ValueError, KeyError, IndexError, TypeError):
                    raise GenerationError("Malformed chat-completions response.") from None
                record = {"attempt": attempt + 1, "response": content, "usage": data.get("usage")}
                attempts.append(record)
                try:
                    result = schema.model_validate_json(content)
                    if validate:
                        validate(result)
                    record["accepted"] = True
                    return result, attempts
                except (ValidationError, ValueError) as error:
                    record["accepted"] = False
                    if isinstance(error, ValidationError):
                        detail = json.dumps(
                            error.errors(
                                include_input=False,
                                include_url=False,
                                include_context=False,
                            )
                        )
                    else:
                        detail = str(error)
                    record["validation_error"] = detail
                    messages.extend(
                        [
                            {"role": "assistant", "content": content},
                            {
                                "role": "user",
                                "content": (
                                    "The output failed structural validation: "
                                    + detail
                                    + "\nReturn corrected JSON. Preserve the meaning. "
                                    "This is not proof feedback. Do not repair invalid arguments."
                                ),
                            },
                        ]
                    )
        raise GenerationError(
            f"No structurally valid {schema.__name__} after {len(attempts)} attempts.",
            attempts=attempts,
        )
