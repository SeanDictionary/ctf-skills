# Workflow

## Triage

- Run file-type and metadata checks first.
- Look for nested archives, encodings, or embedded executables.
- Inspect dimensions, channels, and container formats for media or document files.

## Pivot Clues

- Embedded executable or bytecode: move toward reverse.
- Strong arithmetic structure: move toward crypto.
- PCAP, logs, browser traces, or timeline evidence: move toward forensics.
- URL, HTML, or JS assets: move toward web.

## Good Discipline

- Keep a short list of transforms already attempted.
- Prefer reversible transforms and preserve originals.
- Stop once the hidden domain is clear.
