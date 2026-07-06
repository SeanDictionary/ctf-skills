---
name: ctf-dshield
description: Use when Codex needs the local D盾 package for Windows webshell scanning, server hardening checks, or Web backdoor triage. Trigger on mentions of D盾, 网站后门查杀, 服务器安全检查, or Chinese Windows server defense tooling.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\D盾`
- GUI executable: `D_Safe_Manage.exe`

# Workflow

- Launch only when the user explicitly wants the GUI tool.
- Use it for scanning and review before making cleanup decisions.
- Prefer documenting findings or exportable evidence when used in incident response.

# Common Command

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\D盾
.\D_Safe_Manage.exe
```

# Notes

- This is a GUI-first Windows tool.
- Opening it may require host permissions outside a sandboxed terminal session.
