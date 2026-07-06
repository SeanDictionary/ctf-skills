# Writeup Style

This suite already leans toward concise Chinese writeups with a clear chain of reasoning. Match that style.

## Tone

- Explain why a step matters before or immediately after the command.
- Keep the narrative moving. One paragraph should usually advance one idea.
- Prefer calm, direct language over checklist dumping.

## Structure

Use this flow when turning notes into a writeup:

1. Basic machine info
2. Initial enumeration and why the first scan was insufficient or sufficient
3. The key clue that changed direction
4. Vulnerability confirmation
5. Exploitation with the smallest necessary payloads
6. Post-foothold reasoning
7. Privilege escalation path

## Keep

- Important commands
- Small output excerpts that prove a claim
- Short code excerpts when source explains the vulnerability
- The reasoning behind pivots

## Cut

- Repetitive scan output
- Full-screen command logs with no insight
- Dead ends that did not teach anything

## Good Narrative Pattern

- State the observation.
- Explain why it matters.
- Show the command or payload.
- Show the proof.
- Use that proof to justify the next move.

## Formatting

- Use fenced code blocks for commands and short outputs.
- Use inline code for ports, params, paths, payload fragments, usernames, and flags.
- When quoting source, keep only the lines needed to explain the bug.
