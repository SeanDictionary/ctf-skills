---
name: ctf-xpoc
description: Use when Codex needs the local xpoc executable for Chaitin cloud/local POC listing, pulling, and target scanning from Windows. Trigger on mentions of xpoc, quick POC sweep, Chaitin POC manager, or cloud POC scanning.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\xpoc`
- Binary: `D:\\Docs\\1.CTF\\0.工具列表\\xpoc\\xpoc.exe`
- Read `doc.md` for pull/list behavior and batch input modes.

# Workflow

- Use `list` first when the user wants to inspect available POCs.
- Use `pull` when the local plugin cache is stale or missing.
- Prefer targeted groups or IDs instead of broad scans when the target scope is narrow.

# Common Commands

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\xpoc
.\xpoc.exe list -a
.\xpoc.exe pull
.\xpoc.exe -t https://example.com -o result.html
.\xpoc.exe -g web.list -t https://example.com
.\xpoc.exe -i targets.txt
```

# Notes

- xpoc is a command-line binary; do not assume GUI behavior.
- Batch mode accepts redirected stdin or `-i targets.txt`.
- Favor narrow POC groups on fragile targets.
