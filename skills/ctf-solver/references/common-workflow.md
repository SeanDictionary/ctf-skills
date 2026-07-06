# Common Workflow

## 1. Intake

- Read the challenge text carefully.
- List supplied files and their types.
- Note the expected flag format if known.
- Record what the user already tried and what failed.

## 2. Fingerprint

- Use strings, metadata, magic bytes, imports, headers, and visible structure to narrow the domain.
- Prefer cheap facts before expensive tooling.

## 3. Hypothesis

State:

- What category this most likely is
- What weakness or puzzle family it likely belongs to
- What minimal proof action would validate that guess

## 4. Controlled Execution

- Run one decisive step.
- Save the artifact, output fragment, or proof that changes the next move.
- Avoid turning the session into a raw command dump.

## 5. Pivot Logic

- If the proof fails, say why the hypothesis weakened.
- Reclassify using the new evidence instead of doubling down blindly.

## 6. Wrap-Up

- Keep commands that mattered.
- Keep only small output fragments that prove a claim.
- Explain the path so it can become a writeup or solver script later.
