"""Small chat-completions client for a local vLLM server or compatible endpoint."""

import json
import time
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
    transport_retries: int = 2
    structured: bool = True
    qwen_nonthinking: bool = False

    def __post_init__(self):
        if not 0 <= self.retries <= 5 or not 0 <= self.transport_retries <= 5:
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
            "retries": self.retries,
            "transport_retries": self.transport_retries,
            "timeout_seconds": self.timeout,
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
        # Constrained decoding enforces shape but does not necessarily put the schema in
        # the model's context. Show it in both modes so the model can plan field meanings.
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
                for network_attempt in range(config.transport_retries + 1):
                    record = {
                        "attempt": attempt + 1,
                        "network_attempt": network_attempt + 1,
                        "accepted": False,
                    }
                    attempts.append(record)
                    try:
                        response = client.post(
                            config.base_url.rstrip("/") + "/chat/completions",
                            json=body,
                            headers=headers,
                        )
                    except httpx.HTTPError as error:
                        # Exception text can contain credentials. Store only the class.
                        detail = f"Model request failed ({type(error).__name__})."
                        transient = isinstance(error, (httpx.TransportError,))
                    else:
                        record["http_status"] = response.status_code
                        if not response.is_error:
                            break
                        detail = f"Model endpoint returned HTTP {response.status_code}."
                        transient = response.status_code in {408, 429, 500, 502, 503, 504}
                    record["error"] = detail
                    if not transient or network_attempt == config.transport_retries:
                        raise GenerationError(detail, attempts) from None
                    time.sleep(min(0.25 * 2**network_attempt, 2.0))
                try:
                    data = response.json()
                    choice = data["choices"][0]
                    content = choice["message"].get("content")
                    record.update(
                        {
                            "response": content,
                            "reasoning": choice["message"].get(
                                "reasoning", choice["message"].get("reasoning_content")
                            ),
                            "usage": data.get("usage"),
                            "finish_reason": choice.get("finish_reason"),
                            "served_model": data.get("model"),
                        }
                    )
                    if choice.get("finish_reason") not in {"stop", None}:
                        record["error"] = "Model generation did not finish; increase max_tokens."
                        raise GenerationError(record["error"], attempts)
                    if not isinstance(content, str) or not content.strip():
                        record["error"] = "Model returned no text content."
                        raise GenerationError(record["error"], attempts)
                except (ValueError, KeyError, IndexError, TypeError, AttributeError):
                    record["error"] = "Malformed chat-completions response."
                    raise GenerationError(record["error"], attempts) from None
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
