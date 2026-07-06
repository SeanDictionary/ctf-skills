---
name: ctf-frp
description: Use when Codex needs the local frp package for internal tunneling, reverse proxying, port forwarding, dashboard configuration, or temporary exposure of internal services. Trigger on mentions of frp, frpc, frps, reverse tunnel, port forward, or intranet penetration.
---

# Local Assets

- Tool root: `D:\\Docs\\1.CTF\\0.工具列表\\frp`
- Bundles: `frp_0.67.0_windows_amd64`, `frp_0.67.0_linux_amd64`
- Docs: `common.md`, `client-configures.md`, `server-configures.md`

# Workflow

- Decide whether the user needs server (`frps`) or client (`frpc`) mode.
- Choose the Windows or Linux bundle that matches the current host.
- Prefer config-file based runs instead of long inline commands.
- Keep bind ports, auth, and dashboard exposure scoped tightly.

# Common Commands

```powershell
cd D:\\Docs\\1.CTF\\0.工具列表\\frp\\frp_0.67.0_windows_amd64
.\frps.exe -c .\frps.toml
.\frpc.exe -c .\frpc.toml
```

# Notes

- Read `common.md` for shared config fields.
- Read `server-configures.md` for `frps` options and `client-configures.md` for `frpc` options.
- Avoid opening public listeners wider than the user asked for.
