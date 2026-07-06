---
name: ctf-dirsearch
description: Use when Codex needs the local dirsearch setup for Web path brute forcing, hidden directory discovery, backup-file hunting, recursive content discovery, or authenticated directory fuzzing. Trigger on mentions of dirsearch, directory brute force, backup file search, or hidden path enumeration.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\dirsearch-0.4.3`
- Recommended entrypoint: `D:\\Docs\\1.CTF\\0.工具列表\\dirsearch-0.4.3\\START.bat`
- Python entrypoint: `.\.venv\Scripts\python.exe .\dirsearch.py`
- Read `doc.md` for local defaults and `config.ini` behavior.

# Workflow

- Prefer `START.bat` from the tool directory.
- Choose extensions based on the target stack.
- Add filters early if the site returns fake `200` or uniform `403` pages.
- Use `--cookie` or `--raw` for authenticated targets.

# Common Commands

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\dirsearch-0.4.3
.\START.bat -u http://target -e php,html,js
.\START.bat -u http://target -e php,zip,bak,old,txt -f
.\START.bat -u http://target -e php,html,js -r -R 2
.\START.bat -u http://target --cookie "PHPSESSID=xxxx" -e php,html,js
```

# Notes

- If the wordlist is not `%EXT%` based, remember `-f`.
- Use `--exclude-response`, `--exclude-text`, or `--exclude-sizes` when noise is high.
- Save reports with `--format` and `-o` when the user wants reusable output.
