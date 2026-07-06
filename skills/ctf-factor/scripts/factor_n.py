#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
from collections import Counter
from typing import Dict, Iterable, List, Optional

MAX_SAGE_TIMEOUT = 180.0


def parse_n(raw: str) -> int:
    text = raw.strip().replace("_", "")
    if text.lower().startswith("0x"):
        return int(text, 16)
    return int(text, 10)


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def is_probable_prime(n: int) -> Optional[bool]:
    if n < 2:
        return False
    if has_module("sympy"):
        import sympy

        return bool(sympy.isprime(n))
    return None


def refine_small_factor(n: int, max_bits: int) -> Optional[Dict[int, int]]:
    if n.bit_length() > max_bits or not has_module("sympy"):
        return None

    import sympy

    try:
        return {int(p): int(e) for p, e in sympy.factorint(n).items()}
    except Exception:
        return None


def factor_via_factordb(n: int, refine_bits: int) -> Dict[str, object]:
    try:
        from factordb.factordb import FactorDB
    except Exception as exc:
        return {
            "backend": "factordb",
            "status": "unavailable",
            "reason": f"factordb-python import failed: {exc}",
            "factors": [],
        }

    try:
        fdb = FactorDB(n)
        fdb.connect()
        status = None
        if hasattr(fdb, "get_status"):
            status = fdb.get_status()
        raw_factors = []
        if hasattr(fdb, "get_factor_list"):
            raw_factors = list(fdb.get_factor_list() or [])

        counter: Counter[int] = Counter()
        for value in raw_factors:
            ivalue = int(value)
            refined = refine_small_factor(ivalue, refine_bits)
            if refined:
                counter.update(refined)
            else:
                counter[ivalue] += 1

        factors = []
        product = 1
        all_prime = True
        for factor in sorted(counter):
            exponent = counter[factor]
            prime_flag = is_probable_prime(factor)
            if prime_flag is not True:
                all_prime = False
            product *= pow(factor, exponent)
            factors.append(
                {
                    "factor": str(factor),
                    "exponent": exponent,
                    "is_probable_prime": prime_flag,
                }
            )

        complete = product == n and factors and all_prime
        if status in {"FF", "P", "PRP"} and product == n:
            complete = True

        return {
            "backend": "factordb",
            "status": "complete" if complete else "partial",
            "factordb_status": status,
            "factors": factors,
        }
    except Exception as exc:
        return {
            "backend": "factordb",
            "status": "error",
            "reason": str(exc),
            "factors": [],
        }


def unique_existing(paths: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for path in paths:
        if not path:
            continue
        norm = os.path.normpath(path)
        if norm in seen:
            continue
        if os.path.exists(norm):
            out.append(norm)
            seen.add(norm)
    return out


def find_sage_paths() -> Dict[str, Optional[str]]:
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    sage_roots = glob.glob(os.path.join(local_appdata, "SageMath *"))

    bash_candidates = unique_existing(
        [
            os.environ.get("SAGE_BASH"),
            *(os.path.join(root, "runtime", "bin", "bash.exe") for root in sage_roots),
            shutil.which("bash"),
        ]
    )
    sage_candidates = unique_existing(
        [
            os.environ.get("SAGE_RUNNER"),
            *(os.path.join(root, "runtime", "opt", "sagemath-9.3", "sage") for root in sage_roots),
            *glob.glob(
                os.path.join(local_appdata, "SageMath *", "runtime", "opt", "sagemath-*", "sage")
            ),
        ]
    )

    return {
        "bash": bash_candidates[0] if bash_candidates else None,
        "sage": sage_candidates[0] if sage_candidates else None,
    }


def factor_via_sage(n: int, timeout_seconds: float) -> Dict[str, object]:
    timeout_seconds = min(float(timeout_seconds), MAX_SAGE_TIMEOUT)
    paths = find_sage_paths()
    bash_path = paths["bash"]
    sage_path = paths["sage"]
    if not bash_path or not sage_path:
        return {
            "backend": "sage",
            "status": "unavailable",
            "reason": "Sage bash runner or sage launcher was not found",
            "factors": [],
        }

    sage_code = (
        "import json\n"
        "from sage.all import ZZ, factor\n"
        f"n = ZZ('{n}')\n"
        "fac = factor(n)\n"
        "print(json.dumps([[str(p), int(e)] for p, e in fac]))\n"
    )
    command = f"'{sage_path.replace(os.sep, '/')}' -q -c {shlex.quote(sage_code)}"

    try:
        proc = subprocess.run(
            [bash_path, "-lc", command],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "backend": "sage",
            "status": "timeout",
            "reason": f"Sage factor exceeded {timeout_seconds}s",
            "factors": [],
        }

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        return {
            "backend": "sage",
            "status": "error",
            "reason": detail or f"Sage exited with code {proc.returncode}",
            "factors": [],
        }

    stdout = proc.stdout.strip().splitlines()
    if not stdout:
        return {
            "backend": "sage",
            "status": "error",
            "reason": "Sage returned no output",
            "factors": [],
        }

    raw = stdout[-1].strip()
    try:
        pairs = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "backend": "sage",
            "status": "error",
            "reason": f"Could not parse Sage output: {raw}",
            "factors": [],
        }

    factors = [
        {"factor": str(int(p)), "exponent": int(e), "is_probable_prime": True}
        for p, e in pairs
    ]
    return {"backend": "sage", "status": "complete", "factors": factors}


def format_human(result: Dict[str, object], n: int) -> str:
    lines = [
        f"n: {n}",
        f"backend: {result.get('backend')}",
        f"status: {result.get('status')}",
    ]
    if result.get("reason"):
        lines.append(f"reason: {result['reason']}")
    if result.get("guidance"):
        lines.append(f"guidance: {result['guidance']}")
    if result.get("factordb_status") is not None:
        lines.append(f"factordb_status: {result['factordb_status']}")

    factors = result.get("factors", [])
    if factors:
        lines.append("factors:")
        for item in factors:
            prime_suffix = ""
            if item.get("is_probable_prime") is True:
                prime_suffix = " (prime)"
            elif item.get("is_probable_prime") is False:
                prime_suffix = " (composite or unknown)"
            lines.append(f"  {item['factor']}^{item['exponent']}{prime_suffix}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Factor n via factordb-python first, then Sage factor with timeout."
    )
    parser.add_argument("n", help="Integer to factor, decimal or 0x-prefixed hex")
    parser.add_argument(
        "--backend",
        choices=["auto", "factordb", "sage"],
        default="auto",
        help="Which backend to use",
    )
    parser.add_argument(
        "--sage-timeout",
        type=float,
        default=30.0,
        help="Hard timeout in seconds for Sage factor (capped at 180)",
    )
    parser.add_argument(
        "--refine-bits",
        type=int,
        default=80,
        help="Refine small FactorDB factors locally when they are at most this many bits",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable text",
    )
    args = parser.parse_args()

    n = parse_n(args.n)
    args.sage_timeout = min(float(args.sage_timeout), MAX_SAGE_TIMEOUT)

    if args.backend == "factordb":
        result = factor_via_factordb(n, args.refine_bits)
    elif args.backend == "sage":
        result = factor_via_sage(n, args.sage_timeout)
    else:
        first = factor_via_factordb(n, args.refine_bits)
        if first.get("status") == "complete":
            result = first
        else:
            second = factor_via_sage(n, args.sage_timeout)
            if second.get("status") == "complete":
                result = second
            else:
                result = second
                result["factordb_fallback"] = first
                result["guidance"] = (
                    "Generic factoring did not complete. Do not keep switching among similar "
                    "factoring methods without a new hypothesis; treat n as likely intentionally "
                    "hard and pivot to structure-specific analysis."
                )

    if args.backend in {"factordb", "sage"} and str(result.get("status")) != "complete":
        result.setdefault(
            "guidance",
            "This backend did not complete the factorization. Avoid blind retry loops with "
            "equivalent generic methods unless you have new structural evidence."
        )

    if args.json:
        payload = {"n": str(n), **result}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
    else:
        print(format_human(result, n))

    return 0 if str(result.get("status")) == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
