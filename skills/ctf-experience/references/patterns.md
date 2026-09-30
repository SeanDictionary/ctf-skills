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

## Reverse Heuristics (Windows PE / DOS / PyInstaller)

### PyInstaller CArchive parsing is big-endian

- `Signal`: Hand-parsing a PyInstaller onefile exe (cookie `MEI\x0c\x0b\x0a\x0b\x0e`) and lengths look absurd (multi-GB toc/pkg on a small file).
- `Why It Matters`: The cookie and TOC entry structs use network byte order (`struct '>IIII'` / `'>IIIBc'`); little-endian parsing silently produces garbage instead of an error.
- `Default Action`: Parse cookie with `>`; `arch_start = cookie_pos + 88 - pkglen`; TOC entry is `>I` elen + `>IIIBc` + name. If the embedded python version matches the local interpreter, prefer `marshal.loads` + `exec(code, {'__name__':'notmain'})` to call inner functions directly instead of re-implementing transforms.
- `Stop Condition`: If marshal fails across versions, fall back to `dis` + manual reimplementation.

### Bytecode/math misread -> verify against authoritative disassembly, not more guessing

- `Signal`: A hand-copied transform (xor operand order, magic-number division, shift-add coefficients) produces garbage or z3 says unsat.
- `Why It Matters`: Manual transcription of assembly is the most common error source; `imul magic; shr; add; sar` sequences are signed division by a constant (e.g. `(i+k)%n`), and fused load/store pairs can hide extra terms.
- `Default Action`: Re-run objdump on the exact byte range and re-derive term by term; for unsat z3 models, suspect a missing/extra constraint term first, not the solver.
- `Stop Condition`: Once a decoded string starts with the flag prefix, one reverse-verification pass (re-encode and compare) closes the loop.

### 16-bit DOS MZ layout for static analysis

- `Signal`: `file` reports `MS-DOS executable, MZ` and the binary is tiny; no DOSBox needed.
- `Why It Matters`: Load module starts at file offset `e_cparhdr*16`; code VA 0 = that offset, so `file_off = VA + header_size`. objdump can disassemble with `-b binary -m i386 -Maddr16,data16`.
- `Default Action`: Parse the MZ header, dump the load module, disassemble 16-bit, and reimplement the loop in Python. Watch operand direction on `xor r/m, r` when copying.
- `Stop Condition`: If the program needs BIOS/DOS services beyond static comprehension, ask before installing an emulator.

### Flower instructions (junk bytes) -> patch NOPs then re-disassemble

- `Signal`: README/strings hint at junk byte groups, or linear disassembly shows `(bad)` / nonsense control flow after a conditional jump that is always taken (`xor reg,reg` + `je`).
- `Default Action`: Search the raw bytes for the junk patterns, patch them to `0x90` in a copy, re-run objdump; keep the original untouched.
- `Stop Condition`: Once disassembly aligns and cross-references to data strings resolve, stop hunting for more junk.

## Interactive Crypto Service Heuristics (0xGame2026 session)

### Non-ASCII input leaks Python source lines

- `Signal`: Any interactive Python netcat service whose logic is unclear.
- `Why It Matters`: Sending invalid UTF-8 (e.g. `\xff\xfe\x80\n`) makes `hmac.compare_digest` (and similar) raise `TypeError: comparing strings with non-ASCII characters` with a traceback showing the exact source line and file path. This reveals whether input is parsed (split/fromhex) or compared raw, the check variable names, and rough code structure — recon worth doing BEFORE brute-forcing formats.
- `Default Action`: Early in any unclear service interaction, send invalid UTF-8, empty line, and overlong inputs; compare traceback lines to map the code.
- `Stop Condition`: Once input semantics (what is compared to what) are known.

### DH public keys outside <g> + parallel hash list -> small-order residue leak

- `Signal`: A DH service hands a B array (or multiple B's) plus a hash list, and `ord(g)` is a large prime while B's are NOT in <g>.
- `Why It Matters`: If all B[i]^M == 1 for the smooth part M of p-1, each B[i] lives in smooth torsion, often with tiny order (e.g. exactly one small prime q_i). Then B[i]^a = B[i]^(a mod q_i); hash-verify each residue r in [0,q_i) against the provided hash list, then CRT all residues to recover a. Verify g^a == A.
- `Default Action`: Compute ord(g) and test B[i]^M; factor the dlogs of B[i] (PH is cheap in smooth torsion); look for b_i = c_i·(M/2)/q_i structure = order q_i; brute r per prime against sha256(Big-endian bytes).
- `Stop Condition`: g^a == A verified.

### ECDSA with structured nonce -> check r duplicates FIRST

- `Signal`: ECDSA service + hint that nonce comes from LFSR/PRNG with small state (e.g. "length five").
- `Why It Matters`: r = (kG).x depends only on k, so state periodicity shows up as repeated r values. A repeat pair (i, i+j) gives the classic repeated-nonce solve: k = (h_i-h_j)/(s_i-s_j), d = (s_i·k-h_i)/r_i. Period-31 LFSR means minimum 32 signatures — such services often gate the flag on "minimal interaction" = exactly that count.
- `Default Action`: Request max signatures, dedupe r values; if count == period, take pair (0, period). Test hash conventions: sha512 of the message STRING vs decoded bytes (services that print hex messages often hash the string form). For follow-up "sign with fixed r": check if r == Gx (k=±1) and try BOTH k=1 and k=n-1 — different failure messages usually distinguish wrong-s vs right-s-wrong-k.
- `Stop Condition`: d*G == pubkey, then final signature accepted.

### Truncated modulus + digit-count hint -> famous challenge numbers

- `Signal`: RSA n whose decimal digit count is one less than a hint asserts (e.g. len(n)==155 but printed n has 154 digits), plus wording like "broken/dusty".
- `Why It Matters`: The number is a famous factorization challenge number (RSA-155, RSA-704, ...) with the last digit cut off; FactorDB has it fully factored. Complete the last digit by querying FactorDB for each candidate — only the right one returns FF with two balanced prime factors.
- `Default Action`: Enumerate last digit 0-9 against FactorDB; decrypt with known factors; expect padding/mud in the plaintext that must be cleaned per hint.
- `Stop Condition`: FactorDB status FF and p*q == completed n.

### Pure-emoji ciphertext + password hint -> emoji-aes

- `Signal`: Ciphertext is a pure emoji string (40+ unique emojis including objects/animals/faces), challenge mentions a password/key.
- `Why It Matters`: The emoji-aes tool (Aaron Horler) does AES(CryptoJS passphrase mode) then maps base64 chars to a fixed 64-emoji table. Recognizable by the first 8 emojis decoding to "U2FsdGVk" ("Salted_"). Mirror: emoji-aes.miaotony.xyz. Implementable locally via OpenSSL EvpKDF (MD5, 1 iter) + AES-256-CBC.
- `Default Action`: Check emoji coverage against the tool's emojisInit table; decode emoji->base64; decrypt with the hinted key; expect inner layers (base64 of the next layer). Note: other emoji tools (表情密文翻译器 etc.) have different alphabets — verify coverage first.
- `Stop Condition`: "U2FsdGVk" prefix appears after emoji->b64 substitution.

## Pwn Exploitation Heuristics (0xGame2026 session)

### system/printf crash right after reaching target -> movaps 16-byte alignment, compute don't guess

- `Signal`: Chain visibly succeeds (win banner / leak prints) then process SIGSEGVs with no other explanation; or a re-entered function crashes inside printf.
- `Why It Matters`: glibc SSE code (movaps) requires rsp ≡ 8 at function entry (rsp ≡ 0 at the `call`). ROP `ret` chains land with either parity depending on chain length — the fix direction differs per chain and cannot be memorized globally (one challenge needed +ret, another needed -ret).
- `Default Action`: Track rsp mod 16 symbolically from vuln's `leave;ret` through every pop/ret (rbp of a standard frame is 16-aligned). If target entry rsp ≡ 0 (needs ≡8), insert one `ret` gadget; if already ≡8, don't. When re-entering a function via ret (e.g. returning into vuln for a second read), the SAME alignment fix applies before it.
- `Stop Condition`: Target function's first libc call runs without SIGSEGV.

### ret2csu `call [r15]` target must preserve rdi/rsi/rdx -> use .fini_array pointer

- `Signal`: ret2csu chain sets r12-r15, calls a GOT function (write/read) as "harmless", but win/next-stage receives garbage args ("key is not correct").
- `Why It Matters`: Modern glibc cancellation wrappers (write/read) reorder/clobber argument registers, so calling them between `mov edi,r12d...` and the target destroys the setup.
- `Default Action`: Point r15 at `.fini_array` (contains &__do_global_dtors_aux): its early-out path only touches rax/completed flag. Alternative: `_init` when __gmon_start__ is 0.
- `Stop Condition`: Target function receives the three intended register values.

### Hand-rolled SROP frame: registers start at 0x28, not 0x30

- `Signal`: SROP sigreturn "succeeds" but rip/rsp land on wrong values (e.g. rip equals your intended rsp slot) -> offsets shifted by 8.
- `Why It Matters`: x86-64 rt_sigframe is 248 bytes; gregs begin at frame+0x28 (r8). Correct offsets: rdi=0x68, rsi=0x70, rdx=0x88, rax=0x90, rcx=0x98, rsp=0xA0, rip=0xA8, CSGSFS=0xB8 (set 0x33). uc_flags/fpstate = 0 works (kernel clears FPU instead of restoring).
- `Default Action`: `write(1, msg, 0xf)` gadget style functions return rax=15 = rt_sigreturn — use as trigger when `vuln` ends with `xor rax,rax`. Two-stage SROP (read to fixed RW page, then execve) when "/bin/sh" has no known-address home.
- `Stop Condition`: sigreturn restores intended rip/rsp and chain continues.

### mmap-RWX shellcode with tiny read limit -> watch count register and self-overwrite

- `Signal`: Shellcode stage does `syscall` for a second read using an entry register (often rdx = page address) as count, then jumps back to page start; process spins (state R, userspace).
- `Why It Matters`: buf+count becomes non-canonical -> read returns immediately with error -> `jmp` loops forever. Also, the second read overwrites the page start INCLUDING not-yet-executed bytes after the syscall.
- `Default Action`: Shrink count in-place (`shr edx,0x10`, 3 bytes, also zeroes upper half); after the syscall, rip sits at page+7, so lay stage-2 with nops at [7:9] and real code from offset 9, falling through instead of jumping. Clear rdx/envp in stage-2 execve (count residue causes EFAULT).
- `Stop Condition`: execve succeeds / shell responds.

### Format-string leak bytes may contain 0x0a -> parse by byte count, never split lines

- `Signal`: Leak parse intermittently yields a wrong (truncated) address value.
- `Why It Matters`: A 6-byte leaked libc address can contain 0x0a or 0x00; line-splitting or strip() breaks the value. Same class of bug: `%<n>c` padding output (up to 65k chars) clogs the pipe and buries shell responses.
- `Default Action`: Read a fixed byte window or up to a unique trailing marker; u64() zero-pads correctly for short values. After a printf-write stage, drain the pipe (repeated recv with idle timeout) before sending commands.
- `Stop Condition`: Repeated runs parse identical correct base addresses.

### Partial GOT overwrite needs only low 4 bytes when target is same-libc

- `Signal`: Format-string write available, GOT entry already resolved to a libc function, goal is another function in the same libc (e.g. puts@got -> system).
- `Why It Matters`: Same mapping means upper 4 bytes match; two `%hn` writes (low16 then bits16-31, ordered small->large so the second directive prints the delta) suffice. Addresses for the writes live inside the fmt buffer itself; compute their `%N$` slot from actual directive length (iterate to fixed point since slot number length changes the directive).
- `Stop Condition`: /proc/pid/mem (or behavior) confirms GOT now holds target address.

### Interactive math/quiz services -> normalize full-width & lookalike operators, anchor regex to the question

- `Signal`: Scripting challenge asks to answer N arithmetic questions fast; first answers marked wrong despite "obviously correct" math.
- `Why It Matters`: Two decoy classes: progress markers like `[round:1/100]` match a naive `(\d+)([+-*/])(\d+)` regex (parsed 1/100 as the question!); operators use full-width `＋－×÷` and lookalike chars — the nastiest being CJK `一` (U+4E00) as minus.
- `Default Action`: Anchor parsing to the `calculate:` (or equivalent) prefix only; normalize ＋－−×÷／ AND 一(-> -) before matching; integer division.
- `Stop Condition`: N consecutive correct responses.

### ptrace-in-python debugging quirks in this lab environment

- `Signal`: Writing ctypes ptrace tools to debug exploits when pwntools/gdb are unavailable.
- `Why It Matters`: (1) `libc.ptrace` default restype is c_int — PEEKDATA values get sign-extended and a naive POKEDATA restore corrupts adjacent bytes (set `restype=c_long`). (2) PTRACE_SINGLESTEP returns EIO when the tracee was stopped while blocked in a syscall; prefer breakpoints (0xCC + PTRACE_CONT) or PTRACE_SYSCALL. (3) Run python with `-u`, else debug prints buffer away on timeout. (4) `/proc/pid/syscall` "running" + state R means userspace spin; "-1 0x0 0x0" can also mean the process already died (check state Z).
- `Default Action`: Attach early, use INT3 breakpoints at target functions, read/write regs via GETREGS/SETREGS with proper restype.
- `Stop Condition`: Chain flow observed end-to-end.

### A "hanging" process after a leak stage is usually a silent crash -> check /proc state

- `Signal`: After an exploit stage, no further output and recv times out; easy to misread as "blocked waiting for input".
- `Why It Matters`: Post-leak alignment crash (see movaps rule) kills the process immediately; `poll()` checked too late or output backlog hides it.
- `Default Action`: Check `/proc/<pid>/stat` state (Z = already dead) and drain pipes before concluding the process is stuck; a Z state right after a stage means the stage itself crashed, not the next read.
- `Stop Condition`: State S (sleeping) in the expected read syscall.
