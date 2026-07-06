---
name: ctf-reverse
description: Use when a CTF problem is about understanding, deobfuscating, unpacking, or patching a program or script to recover a flag, secret, or validation rule. Best for native binaries, managed binaries, scripts, mobile challenge fragments, custom VMs, anti-debug logic, encoders, key checks, obfuscation layers, serialized blobs, and tasks where the core job is reconstructing logic rather than exploiting memory corruption.
---

# CTF Reverse

## Overview

Solve reverse problems by recovering the program's decision logic and data transforms. Build a mental model of inputs, branches, encoders, and hidden constants before brute forcing anything.

## Use This Skill For

- The user has an executable, script, class file, packed blob, or validation routine.
- The challenge needs logic recovery, deobfuscation, patching, or symbolic reasoning.
- IDA, Ghidra, strings, or runtime tracing are more relevant than exploit primitives.

## Workflow

1. Fingerprint the artifact.
   Architecture, language, packer signs, imports, strings, and obvious resources.
2. Locate the trust boundary.
   Where input is read, transformed, compared, or decrypted.
3. Recover the transform graph.
   Constants, lookup tables, encoders, arithmetic, branch conditions, and hidden data sources.
4. Choose solve style.
   Static recovery, small dynamic trace, patch-and-bypass, script reimplementation, or symbolic reasoning.
5. Extract the answer with proof.
   Show why the recovered logic produces the flag or secret.

## Guardrails

- Do not drown in full-program decompilation if only a small checker matters.
- Use dynamic tracing to answer a concrete uncertainty, not as a reflex.
- If the main hard part becomes algebra or number theory, hand off the reasoning to crypto-style methods.
- If the binary is better attacked than understood, hand off to pwn-style reasoning.

## Reference Routing

- For reverse-specific checkpoints and tool choices, read [references/workflow.md](references/workflow.md).

## Output Expectations

- Report the key functions or stages, the recovered transformation, and the shortest reproducible path to the answer.
