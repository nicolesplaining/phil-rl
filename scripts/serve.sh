#!/usr/bin/env bash
set -euo pipefail

# Run on the GPU host. HF_TOKEN may be set in the environment; never echo it.
command -v uvx >/dev/null || { echo 'Install uv before launching the server.' >&2; exit 1; }
command -v nvidia-smi >/dev/null || { echo 'An NVIDIA GPU host is required.' >&2; exit 1; }

exec uvx --python 3.12 --from "vllm==${VLLM_VERSION:-0.19.1}" vllm serve \
  "${PHIL_MODEL:-Qwen/Qwen3-32B}" \
  --host 127.0.0.1 \
  --port "${PHIL_PORT:-8000}" \
  --tensor-parallel-size "${PHIL_TP:-2}" \
  --dtype bfloat16 \
  --max-model-len "${PHIL_CONTEXT:-16384}" \
  --max-num-seqs 4 \
  --gpu-memory-utilization 0.85 \
  "$@"
