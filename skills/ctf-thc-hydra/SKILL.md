---
name: ctf-thc-hydra
description: Use when Codex needs Hydra workflow guidance for authorized credential auditing, weak-password checks, lockout testing, or protocol-specific authentication brute force planning. Trigger on mentions of hydra, weak password audit, credential spraying, or protocol logins such as ssh, ftp, http-post-form, smb, redis, or mysql.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\thc-hydra`
- This directory is source code and documentation, not a ready Windows binary.
- Read `doc.md`, `README`, `INSTALL`, and `hydra.1` when you need module/build details.

# Workflow

- Confirm authorization and rate-limit risk before suggesting commands.
- First check whether Hydra is already installed in the current environment.
- If not installed, prefer package manager or Docker guidance instead of improvising a local Windows build.
- Use `hydra -U <service>` when the user needs module-specific syntax.

# Common Commands

```bash
hydra -h
hydra -U ssh
hydra -l user -P pass.txt ssh://192.168.1.10
hydra -L users.txt -P pass.txt ftp://192.168.1.10 -t 4 -W 3
hydra -l admin -P pass.txt http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"
```

# Notes

- This tool is for authorized auditing only.
- Recommend low concurrency and output logging on fragile targets.
- If the user only wants one-off SSH verification, consider lighter tooling before Hydra.
