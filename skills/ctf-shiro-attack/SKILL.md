---
name: ctf-shiro-attack
description: Use when Codex needs the local ShiroAttack2 package for Apache Shiro rememberMe key checks, gadget/key brute force, command execution attempts, proxy-assisted Shiro exploitation, or memory-shell operations. Trigger on mentions of Shiro 550, rememberMe, ShiroAttack2, or Shiro key/gadget brute force.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\shiro_attack-4.7.0-SNAPSHOT-all`
- Launcher: `START.bat`
- Jar: `shiro_attack-4.7.0-SNAPSHOT-all.jar`
- Read `doc.md` for setup expectations such as the `data\\shiro_keys.txt` file.

# Workflow

- Use this tool only on explicitly authorized Shiro targets.
- Confirm whether the user wants detection, key brute force, command execution, or memory-shell features.
- Ensure the `data` directory and key list exist before launch.
- Mention that key modification or memory-shell actions can impact the target.

# Common Commands

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\shiro_attack-4.7.0-SNAPSHOT-all
.\START.bat
java -jar .\shiro_attack-4.7.0-SNAPSHOT-all.jar
```

# Notes

- This tool is primarily GUI driven; launch it only when the user wants the interactive workflow.
- Prefer read-only detection steps before risky modification features.
- Support custom headers and proxying when the target path requires them.
