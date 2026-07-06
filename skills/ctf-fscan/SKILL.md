---
name: ctf-fscan
description: Use when Codex needs to use the local fscan tool for fast host discovery, port scanning, service identification, weak-password-oriented service checks, web title detection, or broad internal-network recon from Windows. Trigger on mentions of fscan or when the user wants a quick all-in-one scanner before deeper tooling.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\fscan`
- Primary binaries: `D:\\Docs\\1.CTF\\0.工具列表\\fscan\\fscan.exe`, `D:\\Docs\\1.CTF\\0.工具列表\\fscan\\fscan`
- Read `D:\\Docs\\1.CTF\\0.工具列表\\fscan\\doc.md` only when you need flag details or scan-engine behavior.

# Workflow

- Confirm authorization and target scope before scanning.
- Prefer `fscan.exe` on Windows.
- Start with a conservative discovery scan, then narrow ports/modules.
- Save scan logs under the current working directory unless the user asked for another path.

# Common Commands

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\fscan
.\fscan.exe -h 192.168.1.10
.\fscan.exe -h 192.168.1.0/24 -p 1-1000 -nopoc
.\fscan.exe -h 192.168.1.10 -m ssh -nobr
.\fscan.exe -h 192.168.1.10 -o result.txt
```

# Notes

- Use `-nopoc` when the user wants safer recon before active checks.
- Use `-m` to focus on a service family instead of scanning everything.
- Follow up with `nmap`, `dirsearch`, `hydra`, or `xray` when fscan finds interesting ports.
