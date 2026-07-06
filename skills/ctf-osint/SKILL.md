---
name: ctf-osint
description: Use when a CTF challenge requires open-source intelligence, attribution, timeline reconstruction, public-profile discovery, geolocation, image context, or entity linking using public information. Best for usernames, aliases, domains, social accounts, leaked handles, EXIF clues, screenshots, public archives, and tasks where the answer depends on current or historical internet-visible evidence rather than a local exploit.
---

# CTF OSINT

## Overview

Solve OSINT tasks with disciplined verification. Turn weak public clues into candidate identities, locations, or timelines, then confirm them with independent sources before claiming the answer.

## Use This Skill For

- The challenge is about a person, alias, image, location, domain, or timeline.
- Public websites, archived pages, and search results are part of the solution path.
- The user needs help keeping evidence organized and avoiding false attribution.

## Workflow

1. Normalize the clue set.
   Names, handles, domains, image fragments, timestamps, languages, and context hints.
2. Expand candidates carefully.
   Search for exact matches, close variants, reused avatars, domain ownership, and contextual links.
3. Verify across independent sources.
   A match should survive cross-checking with dates, geography, visual evidence, or archived snapshots.
4. Keep a timeline when dates matter.
   Use exact dates rather than relative wording.
5. Stop when the answer is defensible.
   OSINT rewards precision more than volume.

## Guardrails

- Use live browsing when public information may have changed.
- Prefer primary or directly attributable sources when possible.
- State when a claim is an inference rather than a direct fact.
- Avoid doxxing behavior outside authorized CTF contexts.

## Reference Routing

- For OSINT clue handling and verification habits, read [references/workflow.md](references/workflow.md).

## Output Expectations

- Report the clue, candidate identity or explanation, the corroborating sources, and the confidence level.
