---
name: ctf-crypto
description: Use when a CTF challenge centers on classical ciphers, modern crypto primitives, algebraic weaknesses, encodings that hide a cryptographic structure, weak randomness, signatures, or protocol math. Best for RSA, ECC, lattice-friendly constructions, hash misuse, MAC confusion, XOR families, stream ciphers, block-mode mistakes, nonce reuse, modular arithmetic, finite-field puzzles, and implementation flaws that become solvable once the primitive is identified.
---

# CTF Crypto

## Overview

Treat crypto problems as identification plus reduction. Name the primitive, identify the broken assumption, reduce the task to the smallest mathematical or scripting step, and prove the recovery path cleanly.

## Use This Skill For

- The challenge includes ciphertexts, keys, signatures, unusual number sets, or algebraic relations.
- The user needs help identifying the primitive before attacking it.
- The hard part is mathematical reasoning, scripting, or modeling randomness.

## Workflow

1. Identify the primitive.
   Infer the scheme from lengths, alphabets, modulus sizes, curve markers, padding, or protocol language.
2. Identify the weakness family.
   Small exponent, reused nonce, shared prime, bad padding oracle model, broken RNG, linear relation, known-plaintext structure, weak mode use, or algebraic leakage.
3. Reduce to a tractable model.
   Build equations, recover parameters, simulate the primitive, or script the decoder.
4. Verify with a tiny proof.
   Recover one plaintext block, one secret bit pattern, or one key relation before fully automating.
5. Script the solve path.
   Keep the math and assumptions explicit so the result is reproducible.

## Guardrails

- Do not brute force blindly until the primitive is named and the search space is justified.
- Separate pure encoding from actual cryptography.
- If the crucial insight depends on code behavior, use reverse-style reasoning first.
- Keep notation simple and executable.

## Reference Routing

- For crypto challenge triage and weakness families, read [references/workflow.md](references/workflow.md).

## Output Expectations

- Report the suspected primitive, the exploitable weakness, the minimal proof, and the scriptable recovery path.
