---
name: ctf-wireshark
description: Use when Codex needs local Wireshark or TShark workflow for PCAP or PCAPNG traffic analysis, packet triage, stream following, endpoint or conversation summaries, HTTP or DNS or TLS extraction, or automated first-pass review of a capture on Windows. Trigger on mentions of Wireshark, tshark, pcap, pcapng, packet capture, traffic capture, 流量包, 抓包, follow stream, protocol analysis, or when a forensics task needs quick network evidence extraction.
---

# CTF Wireshark

## Overview

Use this skill to turn local Wireshark tooling into a repeatable packet-analysis workflow. Start with the bundled TShark automation to produce a quick evidence map, then pivot into focused filters or the Wireshark GUI only when the automated pass reveals something worth drilling into.

## Local Assets

- Preferred CLI binary: `D:\\Wireshark\\tshark.exe`
- Common GUI binary: `D:\\Wireshark\\Wireshark.exe`
- Automated first pass: [scripts/analyze_pcap.py](scripts/analyze_pcap.py)
- Protocol filter cheatsheet: [references/filters.md](references/filters.md)

## Workflow

1. Preserve the original capture.
   Work on a copy if you plan to export objects or split streams.
2. Run the automated first pass.
   Use the bundled script to collect metadata, protocol hierarchy, endpoint stats, conversations, HTTP requests, DNS queries, TLS SNI values, and a deduplicated hostname list.
3. Form one short hypothesis.
   Decide whether the likely flag path is web traffic, beaconing, lateral movement, file transfer, cleartext credentials, or exfil.
4. Pivot to focused filters.
   Follow suspicious TCP streams, isolate one host pair, or filter to the protocol family that matters.
5. Keep exact proof.
   Save the packet numbers, display filter, and extracted object or transcript that proves the answer.

## Quick Start

If `python` is still shadowed by an alias in the current shell, call the real interpreter path directly.

```powershell
& 'C:\Users\SeanL\AppData\Local\Programs\Python\Python313\python.exe' `
  'C:\Users\SeanL\.codex\skills\ctf-wireshark\scripts\analyze_pcap.py' `
  'C:\path\to\capture.pcapng'
```

Write the report to a file and increase the sample size when needed:

```powershell
& 'C:\Users\SeanL\AppData\Local\Programs\Python\Python313\python.exe' `
  'C:\Users\SeanL\.codex\skills\ctf-wireshark\scripts\analyze_pcap.py' `
  '.\Traffic.pcapng' `
  --out '.\traffic-report.md' `
  --limit 40
```

## Good Fits

- The user hands over a `.pcap` or `.pcapng` file and wants a fast triage.
- The task mentions Wireshark or TShark directly.
- A forensics challenge likely hides the flag in HTTP, DNS, TLS, SMB, FTP, or raw TCP streams.
- You need a machine-generated starting point before opening the GUI.

## Notes

- Prefer `tshark` for repeatable summaries and bulk extraction.
- Open Wireshark GUI when stream reassembly, packet-by-packet browsing, or follow-stream context matters more than automation.
- Keep captures read-only unless you explicitly need exported objects or filtered subsets.
