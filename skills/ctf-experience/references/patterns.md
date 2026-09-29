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

## ECC / Discrete Log Heuristics

### Prime-order ECDLP with ~64-80 bit group order

- `Signal`: ECC challenge gives full curve params (p,A,B), base G, public Q=aG, and the group order n is prime with bit-size roughly in [64,80]; sage `E.order()==n`, `is_prime(n)`.
- `Why It Matters`: Pohlig-Hellman needs smooth n (here prime → useless); BSGS needs sqrt(n) memory (~2^32..2^40, infeasible); the only practical route is memoryless Pollard rho / lambda. Many such tasks bank on the solver not having a fast parallel rho.
- `Default Action`: First rule out structural shortcuts with sage in one shot: compute trace t=p+1-n (Smart/anomalous iff t==1; supersingular/MOV iff t==0), and scan embedding degree k in 1..~60 for n|p^k-1 (MOV feasible only if k<=~6). If none, commit to parallel Pollard rho in C/GMP with distinguished points; do NOT try sage's built-in `discrete_log`/PARI `elllog` on the full instance (they are BSGS/memory-bound and will OOM).
- `Stop Condition`: If the group order turns out smooth, anomalous (t==1 → Semaev-Smart), or has small embedding degree (→ MOV/Weil pairing to GF(p^k)*), pivot to those attacks; otherwise rho is correct, just needs compute.

### Distinguished-point parallel rho: get the recovery formula direction right

- `Signal`: Implementing parallel Pollard rho with walk invariant X = a*G + b*Q and storing distinguished points (x,a,b).
- `Why It Matters`: On collision V = a1*G+b1*Q = a2*G+b2*Q, the secret is a = (a1-a2)·(b2-b1)^-1 mod n — i.e. multiply the a-difference by the INVERSE of the b-difference. The mirrored form (b-diff)/(a-diff) is the single most common implementation bug and silently produces a wrong-but-plausible candidate.
- `Default Action`: Derive the formula freshly each time from (a1-a2)G = (b2-b1)Q = (b2-b1)·a·G; always re-verify recovered a by recomputing a*G == Q before trusting it. Also precompute a tiny known-a instance and check the solver reproduces it.
- `Stop Condition`: Once a*G==Q checks out (independent sage/second implementation), the value is confirmed; no further rho needed.

### Affine EC arithmetic in C/GMP: TLS temps and the doubling numerator

- `Signal`: Writing EC point add/double in C with GMP for a hot loop (rho walk, scalar mult).
- `Why It Matters`: Two recurring bugs: (1) `static` temporaries inside ec_add are shared across threads → data races / wrong points; use `__thread` persistent temps (init once) to get both correctness and speed (no per-call mpz_init/clear). (2) Short-Weierstrass doubling slope is (3·x1^2 + A)/(2·y1), NOT (3·x1 + A)/(2·y1) — the missing square breaks 2G immediately and is easy to miss until tested.
- `Default Action`: Always unit-test ec_mul on k=2 and k=3 against sage's 2*G, 3*G before running the real instance; benchmark a tight modmul/ec-add loop first to estimate rho wall-time and decide thread count / DP_BITS.
- `Stop Condition`: When 2G,3G and one known-a scalar all match sage, the arithmetic is trustworthy; switch focus to the rho harness.
