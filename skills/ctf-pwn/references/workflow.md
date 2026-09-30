# Workflow

## Triage

- Confirm file type and architecture.
- Check mitigations such as PIE, NX, RELRO, canary, and seccomp.
- Identify local runtime components: libc, loader, provided Docker image, remote banner, and protocol.

## Primitive Discovery

- Look for exact user-controlled lengths, format strings, bad index math, parser state bugs, and heap object lifetimes.
- Use small, proof-oriented inputs to verify crash shape or leak behavior.

## Exploit Path Selection

- No PIE or obvious win function: prefer direct control transfer.
- Leak available plus NX: prefer ret2libc or ORW.
- Format string: prioritize leaks, writes, and GOT or return-path control.
- Heap: prove one meaningful primitive before designing the final chain.

## Stability

- Keep exploit state minimal.
- Separate local and remote configs cleanly.
- Record offsets, leaks, and constraints so the solve can be reproduced.

## Alignment & Frame Constants (memorize-avoidance)

- Before running any chain ending in system/printf or re-entering a function via ret, track rsp mod 16 symbolically (vuln rbp is 16-aligned; every pop/ret adds 8). Target entry needs rsp ≡ 8 mod 16. Insert or remove one `ret` accordingly — direction differs per chain, never guess.
- SROP x86-64 rt_sigframe: 248 bytes, gregs start at +0x28 (rdi=0x68, rsi=0x70, rdx=0x88, rax=0x90, rsp=0xA0, rip=0xA8, CSGSFS=0xB8 set 0x33); fpstate=NULL is fine.
- ret2csu `call [r15]` must target a function that preserves rdi/rsi/rdx (modern glibc write/read wrappers do not); .fini_array's __do_global_dtors_aux is a safe default.
- Leaked libc addresses can contain 0x0a/0x00 bytes — parse by fixed byte count, never by line splitting.
