# Clean installation check

On macOS arm64, a fresh temporary Python 3.12.2 environment installed a built wheel
from this repository, not an editable checkout. The installed CLI ran outside the
repository. Model-run code was `b83158a1901ff51a483228d79dca06fd141325e8`.

The nine-fixture demo passed 9/9. The installed CLI then sent
`examples/responsibility.txt` through both model stages using the shared-node Qwen
server. The resulting explicit argument was valid in Z3. Lean 4.19.0 accepted its
generated proof with only `propext`, `Classical.choice` and `Quot.sound`.

`clean-install-model/` preserves the actual model run and its manifest.
`clean-install-lean/` preserves the independently repeated kernel check. This is an
installation smoke test, not another held-out accuracy sample. Runtime versions and
model-serving details are in `runtime.json`.

Equivalent commands, with a fresh temporary directory and a running model endpoint:

```bash
uv venv /path/to/temp/venv --python 3.12
uv pip install --python /path/to/temp/venv/bin/python /path/to/phil-rl
/path/to/temp/venv/bin/phil demo --out /path/to/temp/demo
/path/to/temp/venv/bin/phil run /path/to/phil-rl/examples/responsibility.txt \
  --out /path/to/temp/model-run --base-url http://127.0.0.1:18011/v1 --timeout 360
/path/to/temp/venv/bin/phil lean /path/to/temp/model-run/argument.json \
  --out /path/to/temp/model-run/Proof.lean --prove --check --lean-bin /path/to/lean
```
