# Workflow

## Quick Start

Start with the smallest concrete description of the target:

- IP or hostname
- Box name and platform
- What is already known
- Goal: user flag, root flag, source review, or writeup

Then use this order:

1. Fast external enumeration
2. Focused service testing
3. Single exploitation hypothesis
4. Post-foothold local enumeration
5. Privilege escalation
6. Writeup cleanup

## 1. Fast External Enumeration

- Identify open TCP services first.
- If the host looks sparse, follow with full-port enumeration.
- Record only actionable details: title, version, redirect target, auth prompt, certificate CN, interesting headers, robots, uploaded source, leaked paths.
- Treat mail, alternate web ports, and odd high ports as first-class leads.

## 2. Focused Service Testing

### Web

- View the root page, source, and obvious linked paths.
- Check alternate ports and virtual hosts before brute forcing directories.
- Test parameters for reflection, template rendering, file access, auth bypass, XML handling, and upload behavior.
- When code disclosure is possible, read application source early. It often collapses guesswork.
- If blocked by a blacklist or filter, inspect how the input is processed before trying bypasses.

### SSH / Credentials

- Validate whether a username is real before spending time on passwords.
- Reuse creds across SSH, web panels, and local files.
- If brute force is justified, keep it scoped: one account, one protocol, explicit wordlist, explicit rate.

### Mail / POP3 / IMAP / SMTP

- Enumerate banners and auth methods.
- Test credential reuse and look for mailbox clues that support a later path.
- Treat mailbox content as intelligence first, shell second.

### Exposed Files or Source

- Read config, entrypoint, environment handling, and deployment paths.
- Search for hardcoded paths, weak regex, unsafe deserialization, shell invocation, debug switches, and secrets.
- Look for the smallest proof that converts code insight into exploitability.

### Binary / Pwn Triage

- Confirm architecture, mitigations, entry points, and imported functions.
- Decide early whether this is a quick local logic bug or a deeper exploit-development task.
- Use disassembly or decompilation to answer a concrete question, not as a default ritual.

## 3. Hypothesis Format

Before the next exploit step, state:

- Vulnerability or abuse path
- Evidence already observed
- Minimal proof step
- Likely reward if it works
- Fallback if it fails

This keeps the run focused and makes writeups much easier later.

## 4. Post-Foothold Enumeration

Immediately collect:

- `id`, `whoami`, `hostname`, `uname -a`
- Current directory, home directory, shell history if readable
- `sudo -l`
- Interesting files in home, web roots, backups, configs, cron, systemd units
- SUID binaries, file capabilities, writable scripts, writable service paths
- Listening local services and localhost-only web apps
- Passwords, tokens, SSH keys, database creds

Do not jump straight to public privilege-escalation scripts if the box already exposes a custom script or app path. In easy and medium boxes, intended privesc often lives in a writable script, cron, sudo rule, or local service.

## 5. Privilege Escalation Heuristics

Prefer these paths first:

1. `sudo -l`
2. Writable scripts or service files executed by root
3. Secrets that unlock another user
4. SUID or capabilities with a realistic abuse path
5. Scheduled jobs and timers
6. Kernel or package exploits only when the simpler paths are exhausted

When a privesc idea depends on shell parsing, path resolution, or interpreter fallbacks, prove the behavior with a small local test before betting the solve on it.

## 6. Writeup Cleanup

Keep only:

- Commands that uncovered a new fact
- Payloads that directly proved or exploited the issue
- Code snippets that explain the bug
- The exact pivot from user to root

Drop repetitive scans, raw noise, and blind alleys unless they teach an important lesson.
