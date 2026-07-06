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
