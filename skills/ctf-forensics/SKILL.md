---
name: ctf-forensics
description: Use when a CTF challenge focuses on analyzing artifacts, traces, timelines, and recovered evidence rather than direct exploitation. Best for pcap files, memory dumps, disk images, office documents, browser databases, logs, registry hives, filesystem remnants, media metadata, deleted content, and incident-style tasks where the flag is reconstructed from evidence.
---

# CTF Forensics

## Overview

Solve forensics tasks by preserving artifacts, extracting a timeline, and separating signal from noise. The goal is to recover decisive evidence, not to read every byte of every file.

## Use This Skill For

- The challenge provides captures, dumps, images, or historical traces.
- The user needs help recovering deleted data, session traces, credentials, or an event sequence.
- The flag is likely embedded in recovered evidence rather than guarded by an exploit.

## Workflow

1. Preserve and fingerprint.
   Identify artifact type, size, compression, and any embedded containers.
2. Build the evidence map.
   Filesystems, sessions, processes, users, timestamps, network peers, document edits, or browser activity.
3. Hunt the likely flag path.
   Exfil traces, attachments, deleted files, hidden streams, clipboard remnants, registry keys, or metadata.
4. Correlate before concluding.
   A single artifact can mislead; timestamps and cross-artifact consistency matter.
5. Keep the chain of proof.
   Save the exact file, offset, packet, record, or timeline event that proves the answer.

## Guardrails

- Preserve originals before extraction or carving.
- Prefer timelines and targeted queries over indiscriminate dumping.
- If an artifact turns out to be primarily a stego or reverse problem, pivot to the right specialist skill.

## Reference Routing

- For a compact artifact-handling checklist, read [references/workflow.md](references/workflow.md).

## Output Expectations

- Report artifact type, key evidence sources, the reconstruction logic, and the exact proof of the flag.
