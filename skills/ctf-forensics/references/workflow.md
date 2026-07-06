# Workflow

## Artifact Families

- Network: PCAP, flow logs, HTTP transcripts, DNS traces
- Host: memory dumps, disk images, registry hives, browser data
- Documents and media: office files, PDFs, images, audio, video, metadata-rich containers

## Core Questions

- What is the artifact and what time range does it cover?
- Which user, process, or peer matters most?
- Where could the flag logically be stored or transmitted?

## Good Evidence Targets

- Attachments, reconstructed files, extracted credentials, command history, suspicious URIs, hidden streams, deleted artifacts, timeline anomalies

## Correlation Rule

- Prefer at least two agreeing signals before making a final claim when the artifact set is noisy.
