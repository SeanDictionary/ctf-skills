---
name: ctf-nmap
description: Use when Codex needs Nmap guidance or local Nmap installers for host discovery, port scanning, service/version detection, NSE scripts, OS detection, or precise network recon. Trigger on mentions of nmap, NSE, service detection, or when the user wants more control than fscan provides.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\nmap`
- Local files: `nmap-7.98-setup.exe`, `nmap-7.98-1.x86_64.rpm`
- Read `D:\\Docs\\1.CTF\\0.工具列表\\nmap\\doc.md` when you need detailed option references or NSE guidance.

# Workflow

- First check whether `nmap` is already installed and in `PATH`.
- If missing on Windows, use the local installer path above; if missing on Linux, use the RPM only when it matches the target distro.
- Prefer targeted commands such as `-sV`, `-sC`, `-p-`, or specific NSE scripts instead of overusing `-A`.

# Common Commands

```powershell
nmap -sC -sV 192.168.1.10
nmap -Pn -p- --min-rate 3000 192.168.1.10
nmap -sV --script http-title,http-headers -p 80,443 192.168.1.10
nmap -O --osscan-guess 192.168.1.10
```

# Notes

- Use `-Pn` when ICMP or discovery probes are filtered.
- Use NSE scripts only for the service family relevant to the user’s target.
- If the user only needs quick surface recon, fscan may be faster; use Nmap for precision.
