---
name: ctf-antsword
description: Use when Codex needs the local AntSword client bundle for connecting to and managing an already-authorized WebShell session. Trigger on mentions of AntSword, 蚁剑, WebShell client management, or interactive shell management from Windows.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\AntSword-Loader-v4.0.3-win32-x64`
- GUI executable: `AntSword.exe`

# Workflow

- Launch only when the user explicitly wants the GUI workflow.
- Use it only for authorized shells or lab environments.
- Prefer non-GUI tooling when the task can be completed in-shell.

# Common Command

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\AntSword-Loader-v4.0.3-win32-x64
.\AntSword.exe
```

# Notes

- This is an interactive GUI client, not a command-line scanner.
- Opening the GUI may require host permissions outside a sandboxed shell.
