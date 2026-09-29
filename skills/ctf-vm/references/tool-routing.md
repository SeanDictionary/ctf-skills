# Tool Routing

## Goal

Use the fastest local tool that answers the current question, then move on.

## External Recon

- Fast port discovery: `ctf-fscan`
- Precise service detection or selective NSE work: `ctf-nmap`
- Linux-side commands or scripts: run directly in the native Linux shell

## Web Enumeration

- Hidden paths, backups, recursive content: `ctf-dirsearch`
- Passive or active web vulnerability checks: `ctf-xray`
- Shiro-specific checks: `ctf-shiro-attack`
- Chaitin POC pulls and quick sweeps: `ctf-xpoc`

## Credentials

- Password spraying or single-account brute force on authorized targets: `ctf-thc-hydra`
- Prefer tight scope. One service, one account set, clear rate limits.

## Shell / Persistence / Defense Utilities

- Tunnel or expose an internal service: `ctf-frp`
- Malware or webshell scans on a defended host: `ctf-clamav`, `ctf-dshield`, `ctf-hema-webshell`

## Binary Analysis

- Local ELF triage and exploit scaffolding: `ctf-pwn-local-analysis`
- Deep reverse-engineering with the active IDA session: IDA MCP tools
- AWD-style pwn traffic wrapper: `ctf-pwn-waf`

## Box-Focused Heuristics

- Start with `fscan` for quick signal.
- Switch to `nmap` when you need version accuracy, scripts, or a clean full-port record.
- Use `dirsearch` only after checking titles, parameters, alternate ports, and possible virtual hosts.
- Use IDA only when a binary or reverse-engineering question is truly blocking progress.

## Evidence Discipline

- After each tool run, extract the few findings that change the next step.
- Save exact paths, creds, payloads, and response fragments that support the hypothesis.
- If a tool adds noise but no decision value, stop and pivot.
