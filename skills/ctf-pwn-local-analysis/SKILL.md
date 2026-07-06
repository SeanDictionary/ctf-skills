---
name: ctf-pwn-local-analysis
description: Use when Codex needs to analyze a local Linux pwn binary, libc, loader, or exploit workflow from Windows. Covers ELF fingerprinting, protection checks, symbol and section inspection, gadget hunting, pwntools-based exploit scaffolding, and deciding when to switch from Windows-native tooling to a Linux shell for runtime debugging. Trigger on mentions of pwn, ELF, libc, ld.so, ROP, ret2libc, GOT/PLT, canary, PIE, checksec, gadgets, cyclic offsets, pwntools, or local binary analysis.
---

# CTF Pwn Local Analysis

Use this skill for local analysis of Linux pwn artifacts on this Windows host.

Default behavior:

- Prefer the Windows-native toolchain first.
- Pull the target binary, matching `libc.so.6`, and relevant helper files into the current workspace before deeper analysis.
- Use Linux-side execution only when the task truly needs runtime behavior, `gdb`, `gdbserver`, `/proc`, or a real Linux loader.

## Local Toolchain

Known working tools on this host:

- `file`: `C:\Users\SeanL\AppData\Local\SageMath 9.3\runtime\bin\file.exe`
- `checksec.exe`: `C:\Users\SeanL\AppData\Local\Programs\Python\Python310\Scripts\checksec.exe`
- `python`: `C:\Users\SeanL\AppData\Local\Programs\Python\Python310\python.exe`
- `ROPgadget`: `C:\Users\SeanL\AppData\Local\Programs\Python\Python310\Scripts\ROPgadget`
- `readelf`, `objdump`, `strings`, `gdb`: `C:\Program Files\minGW64\x86_84-11.3.0-realse-posix-seh\mingw64\bin\`

Notes:

- `pwntools` imports successfully in the local Python 3.10 environment.
- `ropper` is not installed; use `ROPgadget` instead.
- Prefer absolute paths if `PATH` resolution behaves inconsistently.
- Treat local `gdb.exe` as non-default for Linux ELF runtime debugging; switch to a Linux shell if you need to execute the target under a real Linux debugger.

## Workflow

1. Stage the artifacts locally.
2. Fingerprint the binary and protections.
3. Inspect sections, symbols, relocations, and imports.
4. Hunt gadgets and compute offsets.
5. Build or refine the exploit with `pwntools`.
6. Switch to Linux-side debugging only if static analysis is no longer enough.

## Quick Start

Use this initial pass on a new binary:

```powershell
file .\chall
& 'C:\Users\SeanL\AppData\Local\Programs\Python\Python310\Scripts\checksec.exe' .\chall
readelf -h .\chall
readelf -Ws .\chall
readelf -d .\chall
strings -a .\chall | Select-String -Pattern 'main|puts|system|/bin/sh|flag|menu'
```

Use this pass to answer:

- architecture and bitness
- dynamic vs static
- RELRO, Canary, NX, PIE
- stripped vs symbol-rich
- obvious imported functions, menus, and useful strings

## Static Analysis

Use `readelf` when you need structured metadata:

```powershell
readelf -l .\chall
readelf -S .\chall
readelf -Ws .\chall
readelf -r .\chall
readelf -d .\chall
```

Use `objdump` when you need disassembly or relocation context:

```powershell
objdump -d -M intel .\chall
objdump -R .\chall
objdump -T .\libc.so.6
```

Practical targets:

- find PLT/GOT entries for leak targets
- confirm whether the bug is before or after stack canary checks
- spot unsafe calls such as `gets`, `scanf`, `strcpy`, `memcpy`, `system`
- recover menu logic and argument flow when the binary is small

## Gadgets And Offsets

Use `ROPgadget` for gadget hunting:

```powershell
ROPgadget --binary .\chall --only "ret|pop|leave"
ROPgadget --binary .\libc.so.6 --only "ret|pop|leave"
```

Use local `pwntools` for cyclic patterns and address helpers:

```powershell
python -c "from pwn import *; print(cyclic(200))"
python -c "from pwn import *; print(cyclic_find(0x6161616c))"
python -c "from pwn import *; elf = ELF('./chall'); print(hex(elf.plt.get('puts', 0))); print(hex(elf.got.get('puts', 0)))"
```

Checklist:

- verify the RIP overwrite offset from disassembly or a cyclic pattern
- identify whether a stack-alignment `ret` gadget is needed on amd64
- if using ret2libc, compute `libc_base`, `system`, `setuid`, `dup2`, `execve`, and `"/bin/sh"` from the exact libc when possible

## Exploit Scaffolding

Prefer a small `pwntools` scaffold before writing the final exploit:

```python
from pwn import *

context.binary = elf = ELF("./chall")
libc = ELF("./libc.so.6", checksec=False)

io = process([elf.path])

# leak parsing here
# libc.address = leaked_puts - libc.sym.puts
# payload construction here
```

Keep these pieces separate:

- leak collection
- base-address calculation
- gadget and symbol lookup
- final payload assembly
- local or remote tube selection

## Linux Runtime Fallback

Switch to a Linux shell only when needed:

- the binary must actually execute under Linux
- you need `gdb`, `gdbserver`, `strace`, `/proc/<pid>/maps`, or loader behavior
- the target uses Linux-only syscalls, SUID behavior, namespaces, or seccomp details that static Windows-side inspection cannot validate

When that happens, use `wsl-ssh-linux` or `ctf-sage` as the next layer.

If the skill is running in a restricted sandbox and local tool access, WSL startup, or Linux-side network access fails for environmental reasons, ask the user for global permissions and retry instead of treating the failure as a property of the binary.

## Notes

- Pull the matching `libc.so.6` whenever a leak-based exploit depends on symbol offsets.
- Save large disassembly outputs to files instead of flooding the conversation.
- For quick triage of a suspicious SUID binary, prioritize `file`, `checksec.exe`, `strings`, `readelf -Ws`, and `objdump -d -M intel` before writing an exploit.
