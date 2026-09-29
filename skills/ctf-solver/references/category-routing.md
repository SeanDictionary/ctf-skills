# Category Routing

## Strong Signals

### Box / Service

- IP, hostname, VPN target, multiple ports, login surface, foothold, privilege escalation
- Common handoff: `$ctf-box` for intentional lab box solves (HackMyVM / HTB / VulnHub / practice machines); `$ctf-vm` for penetration, incident response, AWD, or service restoration scenarios

### Web

- URL, cookies, API requests, HTML, JavaScript, source leak, upload, auth flow, SSTI, SQLi, XXE
- Common handoff: `$ctf-web`

### Pwn

- ELF or PE with exploitation goal, buffer overflow, ROP, heap, socket service with crash behavior
- Common handoff: `$ctf-pwn`

### Reverse

- Binary or script that must be understood, patched, unpacked, or emulated to derive the flag or secret
- Common handoff: `$ctf-reverse`

### Crypto

- Encodings, algebra, ciphertext, RSA, ECC, lattices, signatures, hashes, RNG, protocol misuse
- Common handoff: `$ctf-crypto`

### Forensics

- PCAP, memory dump, disk image, logs, office files, media, timelines, registry, browser traces
- Common handoff: `$ctf-forensics`

### OSINT

- Username, handle, image, website, timeline, leak, attribution, public profile hunting
- Common handoff: `$ctf-osint`

### Blockchain

- Solidity or Vyper source, ABI files, EVM bytecode, deployed contract addresses, RPC endpoints, wallet keys, transaction traces, proxies, delegatecall, reentrancy, chain-state puzzles
- Common handoff: `$ctf-blockchain`

### AI

- LLM chat endpoints or APIs, system prompts, prompt injection wording, jailbreak or guardrail-bypass framing, AI agent tool schemas, RAG or tool-output injection, model weight files (`.pt` `.pth` `.pkl` `.onnx` `.safetensors` `.gguf`), adversarial ML constraints, model inversion or leakage wording
- Common handoff: `$ctf-ai`

### Misc

- Puzzle-like prompts, custom formats, automation tasks, stego-adjacent files, hidden mixed signals
- Common handoff: `$ctf-misc`

## Mixed Challenge Patterns

- Reverse plus crypto: reverse the algorithm first, then move to `$ctf-crypto` for the math.
- Web plus reverse: inspect client JavaScript or leaked binaries first, then return to `$ctf-web`.
- Forensics plus OSINT: recover the entity locally, then verify with `$ctf-osint`.
- Misc as wrapper: unpack and fingerprint until the real category emerges.
- AI plus web: treat the chat UI or API as a web surface first (`$ctf-web`), then return to `$ctf-ai` for the prompt or model logic.
- Blockchain plus web: inspect the dapp frontend or API early (`$ctf-web`), then return to `$ctf-blockchain` for the on-chain logic.

## Reclassification Triggers

- A "web" file is actually a custom archive or VM image.
- A "misc" puzzle contains an executable or obfuscated script.
- A "crypto" prompt depends on reverse-engineering the implementation, not the primitive.
- A "reverse" target is easier to exploit directly than to fully understand.
