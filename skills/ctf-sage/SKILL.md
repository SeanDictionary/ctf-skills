---
name: ctf-sage
description: Use when you need SageMath or CTF Python tooling in the lab, specifically the conda environment named 'sage' on sean@172.17.122.193. Includes remote execution patterns that activate 'conda env sage' and run Sage/Python code using SageMath, pycryptodome, and pwntools.
---

# CTF Sage

Use this skill when the task needs the remote `sage` conda environment on `sean@172.17.122.193`.

Assume the normal path is:

- The Windows host can SSH to `sean@172.17.122.193` as `sean`.
- The remote machine has a conda environment named `sage`.
- The preferred execution path is `scripts\\ssh-sage.ps1`.

If basic SSH connectivity is questionable, use `wsl-ssh-linux` first and confirm the host is reachable before debugging Sage-specific behavior.

## Quick Start

Sanity-check the environment:

```powershell
$payload = @"
python - <<'PY'
import Crypto, pwn
print('ok')
PY
"@
powershell -ExecutionPolicy Bypass -File C:\\Users\\SeanL\\.codex\\skills\\ctf-sage\\scripts\\ssh-sage.ps1 -Payload $payload
```

Run a small Sage command:

```powershell
$payload = 'sage -q -c "print(factor(2026))"'
powershell -ExecutionPolicy Bypass -File C:\\Users\\SeanL\\.codex\\skills\\ctf-sage\\scripts\\ssh-sage.ps1 -Payload $payload
```

## Workflow

1. Confirm SSH works to the host.
2. Put the real work in `-Payload` and execute it through `scripts\\ssh-sage.ps1`.
3. Prefer non-interactive snippets, here-docs, and one-shot scripts.
4. Use `scp` plus a remote execution command when the payload becomes large.

## Patterns

### Run Multi-Line Python (pycryptodome / pwntools)

Use a here-doc inside the payload (non-interactive):

```powershell
$payload = @"
python - <<'PY'
from Crypto.Util.number import *
from pwn import *
print('ready')
PY
"@
powershell -ExecutionPolicy Bypass -File C:\\Users\\SeanL\\.codex\\skills\\ctf-sage\\scripts\\ssh-sage.ps1 -Payload $payload
```

### Run Multi-Line Sage

```powershell
$payload = @"
sage -q - <<'SAGE'
R.<x> = PolynomialRing(ZZ)
print((x^2+1).factor())
SAGE
"@
powershell -ExecutionPolicy Bypass -File C:\\Users\\SeanL\\.codex\\skills\\ctf-sage\\scripts\\ssh-sage.ps1 -Payload $payload
```

### Copy In An Exploit Or Script

Use Windows `scp`, then run it via `ssh-sage.ps1`:

```powershell
scp .\\solve.py sean@172.17.122.193:/tmp/solve.py
powershell -ExecutionPolicy Bypass -File C:\\Users\\SeanL\\.codex\\skills\\ctf-sage\\scripts\\ssh-sage.ps1 -Payload "python /tmp/solve.py"
```

## Script

### `scripts\\ssh-sage.ps1`

Execute a payload on the remote host by:

1. Sourcing `~/.bashrc` (best-effort).
2. Sourcing a common `conda.sh` location if needed (`miniforge3`, `miniconda3`, `anaconda3`, `mambaforge`).
3. Activating conda: `conda activate sage`.
4. Running your payload.

The script base64-wraps the remote bash block before sending it over SSH, which keeps multi-line payloads much more reliable than ad hoc quoting.

## Restricted Sandbox Fallback

If this skill is running inside a restricted sandbox and SSH or remote environment setup fails because the sandbox blocks network access, SSH, or access to the needed host tools, do not assume the lab is broken.

Ask the user for global permissions, explain that the failure is environmental, and retry the same command after permissions are expanded.

## Safety Notes

- Prefer non-interactive commands to avoid hanging the session.
- If you truly need an interactive TTY tool such as `gdb` or `tmux`, pause and confirm with the user first.
- If the command only needs generic Linux shell access and not the `sage` environment, use `wsl-ssh-linux` instead.
