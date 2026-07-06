---
name: ctf-misc
description: Use when a CTF challenge is intentionally mixed, puzzle-shaped, automation-heavy, or does not cleanly advertise its true category. Best for custom file formats, stego-adjacent puzzles, protocol toys, encoding chains, challenge wrappers, game-like prompts, scripting tasks, hidden file containers, and questions where the first job is figuring out what kind of problem it really is.
---

# CTF Misc

## Overview

Handle the weird stuff by reducing uncertainty fast. Fingerprint the artifact, unpack wrappers, test small transformations, and route to a more specific domain as soon as the real structure becomes visible.

## Use This Skill For

- The prompt says `misc` or the files look category-ambiguous.
- The challenge may hide a web, reverse, crypto, stego, or forensics core behind a wrapper.
- The user needs a general-purpose puzzle decomposition strategy.

## Workflow

1. Inventory the pieces.
   File types, metadata, obvious text, dimensions, magic bytes, embedded archives, transport formats, and challenge wording.
2. Remove wrappers.
   Decode, unzip, decompile, extract, or split until the inner artifact becomes clear.
3. Search for structure.
   Repetition, delimiter patterns, protocol framing, hidden channels, or suspicious transforms.
4. Decide whether misc is still the right category.
   If not, hand off immediately to the right specialist skill.
5. Keep the solve path compact.
   Misc challenges become unreadable fast if every dead end is preserved.

## Guardrails

- Avoid random tool spraying just because the category is unclear.
- Every transform should have a reason.
- When a file opens a real domain signal, pivot without hesitation.

## Reference Routing

- For misc triage and pivot patterns, read [references/workflow.md](references/workflow.md).

## Output Expectations

- Report what the artifact most likely is, what wrapper was removed, and whether the task should stay in misc or move elsewhere.
