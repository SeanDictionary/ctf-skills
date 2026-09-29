---
name: ctf-solver
description: Use when a CTF challenge is mixed, unclear, or spans multiple domains and pi should act as a general controller before handing off to a more specific CTF skill. Best for prompts that start from a file, archive, URL, pcap, binary, screenshot, source snippet, challenge text, or partial notes and need challenge classification, workflow selection, evidence tracking, and specialist routing across web, pwn, reverse, crypto, misc, forensics, OSINT, or box-style machine solving.
---

# CTF Solver

## Overview

Act as the first-pass CTF controller. Classify the challenge, choose the right specialist path, keep the evidence log small and precise, and switch strategies when the initial category guess is wrong.

## Use This Skill For

- The user says "solve this CTF problem" without naming a category.
- The attachment or prompt could fit multiple domains.
- The challenge has several stages, such as crypto inside reverse or web leading to pwn.
- The user wants one reusable front door instead of remembering every subskill.

## Routing Contract

- If the task is a Linux box, service target, or foothold-to-root chain, route to `$ctf-vm`.
- If the task is a web app, API, upload flow, template, JWT, request log, or source-backed web challenge, route to `$ctf-web`.
- If the task is an exploit-development binary, route to `$ctf-pwn`.
- If the task is about understanding program logic, validation, obfuscation, or key checking, route to `$ctf-reverse`.
- If the task is about ciphers, algebra, encodings, signatures, RNGs, or protocol math, route to `$ctf-crypto`.
- If the task is artifact-heavy or evidence-driven, route to `$ctf-forensics`.
- If the task depends on external identities, internet sources, timelines, or attribution, route to `$ctf-osint`.
- If nothing cleanly fits or the challenge is intentionally weird, route to `$ctf-misc` first.

## Core Workflow

1. Normalize the input.
   Capture the challenge statement, supplied files, target host, archive contents, expected flag format, and what the user has already tried.
2. Classify by strongest signal.
   Use file types, strings, protocol markers, imports, challenge wording, and required tooling to choose the initial category.
3. Produce one short hypothesis.
   State the likely category, the likely weakness or puzzle shape, and the next proof step.
4. Hand off cleanly.
   Use the matching specialist skill's workflow and keep the evidence log in the format `fact -> inference -> next action`.
5. Reclassify quickly if the proof fails.
   Mixed CTF problems often reveal their real category after unpacking or reversing a wrapper.

## Guardrails

- Keep solving lawful and within authorized CTF or lab environments.
- Prefer the lightest action that proves or disproves a hypothesis.
- Noisy scans, brute force, or potentially destructive actions require a pause-and-confirm moment with the user.
- Preserve artifacts and original files before mutating them.
- If internet knowledge could have changed, verify it rather than relying on memory.

## Reference Routing

- For category detection and handoff signals, read [references/category-routing.md](references/category-routing.md).
- For the common solving loop shared across challenge types, read [references/common-workflow.md](references/common-workflow.md).

## Output Expectations

- During triage: return the most likely category, why it fits, and the first specialist path.
- During solving: keep updates short and decision-oriented.
- During wrap-up: summarize the category pivots, key proofs, and final solve path.
