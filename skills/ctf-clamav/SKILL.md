---
name: ctf-clamav
description: Use when Codex needs the local ClamAV packages for malware scanning or package deployment on Linux hosts. Trigger on mentions of ClamAV, clamscan, 病毒查杀, or package-based deployment of a signature scanner on a Linux target.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\clamav`
- Packages: `clamav-1.5.1.linux.x86_64.deb`, `clamav-1.5.1.linux.x86_64.rpm`

# Workflow

- Match the package to the target distro before suggesting installation.
- Use ClamAV for detection and triage, then confirm suspicious hits before deletion.
- If the target already has ClamAV installed, prefer native package-manager updates and `freshclam`.

# Notes

- This directory contains install packages, not a ready Windows binary.
- Deployment to a remote Linux host may require transfer plus package installation privileges.
