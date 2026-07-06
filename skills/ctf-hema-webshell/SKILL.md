---
name: ctf-hema-webshell
description: Use when Codex needs the 河马 WebShell scanner package for Windows or Linux webshell scanning and cleanup planning on a Web root. Trigger on mentions of 河马WebShell, webshell查杀, backdoor scan, or malicious PHP/ASPX file hunting in a site directory.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\河马WebShell`
- Windows package: `HmSetup.zip`
- Linux package: `hm-linux-amd64.tgz`
- Docs: `doc_win.md`, `doc_linux.md`

# Workflow

- Choose the package that matches the target OS.
- Use this for scanning and triage, not blind deletion.
- Preserve suspicious samples or hashes when the user is doing incident review.

# Notes

- Read `doc_win.md` for Windows usage.
- Read `doc_linux.md` for Linux usage.
- Favor reporting and quarantine plans before destructive cleanup.
