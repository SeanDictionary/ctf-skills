---
name: ctf-sqlmap
description: Use when Codex needs the local sqlmap setup for authorized SQL injection detection, parameter testing, raw HTTP request replay, tamper-assisted payload shaping, database enumeration, or controlled extraction in CTF and lab targets. Trigger on mentions of sqlmap, SQL injection automation, raw request files, tamper scripts, or sqlmap API usage.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\sqlmap`
- Entrypoint: `python .\\sqlmap.py`
- API entrypoint: `python .\\sqlmapapi.py`
- Request templates: `GET.txt`, `POST.txt`
- Config: `sqlmap.conf`
- Read `README.md` and `doc\\` when you need option details.

# Workflow

- Confirm authorization and target scope before using automated SQLi testing.
- Start from one reproducible request and pin the suspected parameter with `-p` before widening coverage.
- Prefer `-r` with a raw request file for authenticated, cookie-heavy, JSON, or custom-header targets.
- Escalate gradually: detection and fingerprinting first, then enumeration, then focused extraction.
- Reach for `--level`, `--risk`, `--tamper`, or extra threads only after a baseline probe shows they are needed.
- Avoid broad crawling or whole-site automation when a single proof request is enough.

# Common Commands

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\sqlmap
python .\\sqlmap.py -h
python .\\sqlmap.py -u "http://target/item.php?id=1" -p id --batch
python .\\sqlmap.py -u "http://target/item.php?id=1" -p id --dbs
python .\\sqlmap.py -r .\\POST.txt -p username --batch --current-user
python .\\sqlmap.py -r .\\GET.txt --level 3 --risk 2 --threads 4
python .\\sqlmap.py -r request.txt --cookie="PHPSESSID=xxxx" --tamper=space2comment --dump
python .\\sqlmapapi.py -s -H 127.0.0.1 -p 8775
```

# Notes

- `-r` is usually the most reliable path when the original request comes from Burp or a browser session.
- Use `-p` to keep probes bounded and reduce noise on multi-parameter requests.
- Save durable output when the user needs a reusable trail; sqlmap will also keep session data under its output directory.
- Treat `--os-shell`, file write, and similar post-exploitation features as higher-risk actions that need a stronger proof bar.
