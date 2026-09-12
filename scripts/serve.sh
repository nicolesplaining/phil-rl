#!/usr/bin/env bash
set -euo pipefail

# Run on the GPU host. HF_TOKEN may be set in the environment; never echo it.
# This shared node reserves physical GPU 0 for another project.
export CUDA_VISIBLE_DEVICES=1
command -v nvidia-smi >/dev/null || { echo 'An NVIDIA GPU host is required.' >&2; exit 1; }

if [[ -x .venv-serve/bin/vllm ]]; then
  phil_server=(.venv-serve/bin/vllm)
else
  command -v uvx >/dev/null || { echo 'Install uv before launching the server.' >&2; exit 1; }
  phil_server=(uvx --python 3.12 --from "vllm==${VLLM_VERSION:-0.19.1}" vllm)
fi

exec "${phil_server[@]}" serve \
  "${PHIL_MODEL:-Qwen/Qwen3-32B}" \
  --host 127.0.0.1 \
  --port "${PHIL_PORT:-8011}" \
  --tensor-parallel-size 1 \
  --dtype bfloat16 \
  --max-model-len "${PHIL_CONTEXT:-16384}" \
  --max-num-seqs 1 \
  --gpu-memory-utilization 0.90 \
  "$@"
