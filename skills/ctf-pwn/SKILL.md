---
name: ctf-pwn
description: Use when a CTF problem requires binary exploitation or exploit-development reasoning against a local or remote service. Best for ELF, PE, libc, loader, crash traces, mitigations, gadgets, stack or heap corruption, format strings, seccomp constraints, shellcode, ret2libc, ROP, tcache abuse, socket-driven binaries, or challenges where a working exploit path matters more than full semantic reversal.
---

# CTF Pwn

## Overview

Treat pwn tasks as exploit engineering. Start with protections, input surface, and primitive discovery, then build the exploit around a proven memory corruption or logic primitive.

## Use This Skill For

- A binary or remote service crashes, hangs, or leaks.
- The user needs exploit planning, offset recovery, gadget strategy, or mitigation-aware reasoning.
- The real goal is code execution or arbitrary read or write rather than source-level understanding.

## Workflow

1. Fingerprint the target.
   Confirm architecture, protections, linked libc or loader, imports, strings, and entry behavior.
2. Find the primitive.
   Identify overflow, format string, arbitrary index, type confusion, UAF, or heap misuse.
3. Decide the shortest viable exploitation path.
   Leak plus ret2libc, direct win-function jump, SROP, ORW, heap metadata abuse, or shellcode under the given mitigations.
4. Prove before polishing.
   A clean leak or RIP control proof is more valuable than speculative exploit scaffolding.
5. Automate once the path is real.
   Turn the exploit into a stable script with the least moving parts.

## Guardrails

- Distinguish reverse questions from exploit questions. If understanding the check logic is the main blocker, hand off to reverse-style reasoning first.
- Avoid giant gadget hunts before proving a control primitive.
- Keep local and remote assumptions separate, especially libc and timing.
- When runtime debugging is necessary, say exactly what uncertainty it resolves.

## Reference Routing

- For the pwn triage and exploit-decision checklist, read [references/workflow.md](references/workflow.md).

## Output Expectations

- Report protections, the likely primitive, the chosen exploitation path, and what proof still needs to be established.
