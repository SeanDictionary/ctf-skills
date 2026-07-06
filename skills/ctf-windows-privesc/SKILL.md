---
name: ctf-windows-privesc
description: Use when Codex needs the local Windows 提权 tool set for privilege-escalation enumeration or exploit helpers such as winPEAS and JuicyPotato on an authorized Windows target. Trigger on mentions of 提权, winPEAS, JuicyPotato, or Windows local privesc triage.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\提权`
- Files: `winPEAS.bat`, `winPEASx64.exe`, `JuicyPotato.exe`

# Workflow

- Confirm the target OS version, integrity level, and privilege context first.
- Prefer `winPEAS` for enumeration before choosing an exploit helper.
- Use JuicyPotato only when the host version and COM/DCOM prerequisites make sense.

# Common Commands

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\提权
.\winPEAS.bat
.\winPEASx64.exe
.\JuicyPotato.exe -h
```

# Notes

- This bundle is for authorized Windows privilege-escalation work only.
- Capture the enumeration output before taking exploit actions.
