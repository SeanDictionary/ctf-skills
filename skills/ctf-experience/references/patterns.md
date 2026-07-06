# CTF Patterns

Use this file as the compact memory of stable, cross-challenge solving lessons.

## Pattern Schema

For each pattern, keep four fields:

- `Signal`: What should trigger recall.
- `Why It Matters`: Why this signal changes the solve plan.
- `Default Action`: The next proof step to try first.
- `Stop Condition`: When to stop forcing this pattern and pivot.

## Mixed Protocol -> Crypto -> VM Chains

### Framed custom protocol before encrypted payload

- `Signal`: A binary protocol repeats a short ASCII magic, then fixed-width integers, then a variable body, and payload parsing errors create impossible lengths or mixed garbage.
- `Why It Matters`: Many failures come from misplacing the length field or trailer, which poisons every downstream crypto or reverse conclusion.
- `Default Action`: Reconstruct the frame format first, verify `magic + typed header + payload + trailer`, and re-parse decisive packets before doing crypto analysis.
- `Stop Condition`: If multiple independent packets parse consistently and downstream behavior matches binary logic, stop revisiting old broken parses.

### Downloaded helper binary inside a pcap is part of the challenge, not noise

- `Signal`: Traffic contains a clean file transfer such as `GET /bash`, `/bin`, or other executable-looking object before the suspicious channel starts.
- `Why It Matters`: The file often explains the later protocol, crypto, or execution model faster than raw packet guessing.
- `Default Action`: Extract the object immediately, fingerprint it with `file`/`strings`, and correlate its control flow with the suspicious stream.
- `Stop Condition`: If the extracted object is clearly irrelevant or decoy after minimal validation, return to traffic-only analysis.

### VM-backed command channel hiding behind crypto

- `Signal`: Decrypted command bodies look like structured bytecode rather than shell text, especially with repeated small opcodes, register-like indices, or fixed-size state mutations.
- `Why It Matters`: The real breakthrough may be a lightweight interpreter that eventually reaches a command-execution primitive like `system`, `popen`, or output append, not a direct shell transcript.
- `Default Action`: Reverse the dispatch table, identify state layout, and implement only the opcodes needed to recover strings, commands, and outputs.
- `Stop Condition`: If the bytecode clearly maps to a standard format or the primitive cannot affect the result path, pivot to another layer.

## RSA Heuristics

### Weirdly large public exponent or unusual e/n relationship

- `Signal`: The modulus looks normal-sized, but `e` is also huge or otherwise unusual compared with the common `65537`, and blind factoring stalls.
- `Why It Matters`: This can indicate a deliberately weak private exponent setup where Wiener attack or related small-`d` techniques work immediately even when factoring does not.
- `Default Action`: Run a fast Wiener attack check before escalating factoring effort. Treat it as a cheap proof step, not an optional afterthought.
- `Stop Condition`: If Wiener and similar low-cost small-`d` checks fail cleanly, then resume structure-driven crypto analysis or controlled factoring.

### Stop generic factoring once structure gives more leverage

- `Signal`: FactorDB confirms compositeness but gives no factors, local Sage or heavy tools are unavailable or timing out, and protocol/binary structure is already exposing semantics.
- `Why It Matters`: Continuing blind factoring often burns time after the problem has already shifted into a richer reverse/protocol lane.
- `Default Action`: Freeze generic factoring escalation and pivot to binary semantics, side data, protocol structure, or plaintext recovery opportunities.
- `Stop Condition`: Return to factoring only if a new mathematical hypothesis appears, such as leaked partial factors, repeated primes, or a fresh key-generation flaw.

## Evil Bash Lesson

### `evil_bash`: cheap pivot order that should happen earlier next time

- `Signal`: Pcap downloads a stripped ELF, later stream uses a custom frame, `field=1` hands over `n|e`, `field=2` decrypts into non-text structured blobs, and `field=3` stays unreadable with only `(n,e)`.
- `Why It Matters`: This combination strongly suggests `extracted client + framed protocol + RSA block transform + embedded VM`, and huge `e` should trigger Wiener before any stubborn factoring attempts.
- `Default Action`: Do the steps in this order: fix frame parsing, extract the ELF, identify the RSA block transform, inspect the command executor/VM, then immediately test Wiener on `(n,e)`.
- `Stop Condition`: If `field=2` turns into clear text commands or `e` is ordinary and small-`d` tests fail, fall back to the simpler branch.
