#!/usr/bin/env python3
"""Produce a quick markdown triage report for a PCAP or PCAPNG file using TShark."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_TSHARK_CANDIDATES = (
    r"D:\Wireshark\tshark.exe",
    r"C:\Program Files\Wireshark\tshark.exe",
    r"C:\Program Files (x86)\Wireshark\tshark.exe",
)


def find_tshark(explicit: str | None) -> str:
    candidates = []
    if explicit:
        candidates.append(explicit)

    env_candidate = os.environ.get("TSHARK_PATH")
    if env_candidate:
        candidates.append(env_candidate)

    path_candidate = shutil.which("tshark")
    if path_candidate:
        candidates.append(path_candidate)

    candidates.extend(DEFAULT_TSHARK_CANDIDATES)

    seen = set()
    for candidate in candidates:
        if not candidate:
            continue
        normalized = os.path.normcase(os.path.abspath(candidate))
        if normalized in seen:
            continue
        seen.add(normalized)
        if os.path.isfile(candidate):
            return candidate

    raise FileNotFoundError(
        "Could not find tshark.exe. Pass --tshark or set TSHARK_PATH."
    )


def find_capinfos(tshark_path: str) -> str | None:
    tshark = Path(tshark_path)
    sibling = tshark.with_name("capinfos.exe")
    if sibling.is_file():
        return str(sibling)

    sibling_no_ext = tshark.with_name("capinfos")
    if sibling_no_ext.is_file():
        return str(sibling_no_ext)

    return shutil.which("capinfos")


def run_command(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").replace("\r", " ").strip()


def add_code_section(lines: list[str], title: str, body: str) -> None:
    if not body:
        return
    lines.append(f"## {title}")
    lines.append("```text")
    lines.append(body)
    lines.append("```")
    lines.append("")


def add_table(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    if not rows:
        return
    lines.append(f"## {title}")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(markdown_escape(cell) for cell in padded[: len(headers)]) + " |")
    lines.append("")


def extract_fields(
    tshark_path: str,
    capture_path: str,
    display_filter: str,
    fields: list[str],
    limit: int,
) -> list[list[str]]:
    args = [tshark_path, "-r", capture_path, "-Y", display_filter, "-T", "fields"]
    args.extend(["-E", "header=n", "-E", "separator=\t", "-E", "quote=n"])
    if limit > 0:
        args.extend(["-c", str(limit)])
    for field in fields:
        args.extend(["-e", field])

    code, stdout, _stderr = run_command(args)
    if code != 0 or not stdout:
        return []

    rows: list[list[str]] = []
    for line in stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < len(fields):
            parts.extend([""] * (len(fields) - len(parts)))
        rows.append(parts[: len(fields)])
    return rows


def unique_nonempty(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        item = value.strip()
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def build_report(capture_path: str, tshark_path: str, limit: int) -> str:
    lines: list[str] = []
    lines.append("# PCAP Quick Analysis")
    lines.append("")
    lines.append(f"- Capture: `{capture_path}`")
    lines.append(f"- Generated: `{dt.datetime.now().astimezone().isoformat(timespec='seconds')}`")
    lines.append(f"- TShark: `{tshark_path}`")
    lines.append("")

    capinfos_path = find_capinfos(tshark_path)
    if capinfos_path:
        code, stdout, stderr = run_command([capinfos_path, capture_path])
        if code == 0 and stdout:
            add_code_section(lines, "Capture Metadata", stdout)
        elif stderr:
            lines.append(f"- capinfos warning: `{stderr}`")
            lines.append("")

    for title, args in (
        ("Protocol Hierarchy", [tshark_path, "-r", capture_path, "-q", "-z", "io,phs"]),
        (
            "Endpoints and Conversations",
            [tshark_path, "-r", capture_path, "-q", "-z", "endpoints,ip", "-z", "conv,tcp", "-z", "conv,udp"],
        ),
    ):
        code, stdout, stderr = run_command(args)
        if code == 0 and stdout:
            add_code_section(lines, title, stdout)
        elif stderr:
            lines.append(f"- {title} warning: `{stderr}`")
            lines.append("")

    http_rows = extract_fields(
        tshark_path,
        capture_path,
        "http.request",
        [
            "frame.number",
            "ip.src",
            "tcp.srcport",
            "ip.dst",
            "tcp.dstport",
            "http.host",
            "http.request.method",
            "http.request.uri",
        ],
        limit,
    )
    add_table(
        lines,
        "HTTP Requests",
        ["Frame", "Src", "SPort", "Dst", "DPort", "Host", "Method", "URI"],
        http_rows,
    )

    dns_rows = extract_fields(
        tshark_path,
        capture_path,
        "dns.flags.response == 0",
        ["frame.number", "ip.src", "ip.dst", "dns.qry.name", "dns.qry.type"],
        limit,
    )
    add_table(
        lines,
        "DNS Queries",
        ["Frame", "Src", "Dst", "Query", "Type"],
        dns_rows,
    )

    tls_rows = extract_fields(
        tshark_path,
        capture_path,
        "tls.handshake.extensions_server_name",
        ["frame.number", "ip.src", "ip.dst", "tls.handshake.extensions_server_name"],
        limit,
    )
    add_table(
        lines,
        "TLS SNI",
        ["Frame", "Src", "Dst", "Server Name"],
        tls_rows,
    )

    hostnames = unique_nonempty(
        [row[5] for row in http_rows if len(row) > 5]
        + [row[3] for row in dns_rows if len(row) > 3]
        + [row[3] for row in tls_rows if len(row) > 3]
    )
    if hostnames:
        lines.append("## Hostname Summary")
        for hostname in hostnames[: max(limit, 1)]:
            lines.append(f"- `{hostname}`")
        lines.append("")

    has_section = any(line.startswith("## ") for line in lines)
    if not has_section:
        lines.append("No packet sections were extracted. The capture may be empty, encrypted, or use protocols outside the default triage set.")
        lines.append("")

    lines.append("## Next Steps")
    lines.append("- Follow the busiest or most suspicious TCP stream in Wireshark.")
    lines.append("- Filter around any hostname, IP pair, or protocol that looks relevant.")
    lines.append("- Record the packet number and exact filter when you find decisive evidence.")
    lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a quick markdown report for a PCAP or PCAPNG file using TShark."
    )
    parser.add_argument("capture", help="Path to the .pcap or .pcapng file")
    parser.add_argument("--out", help="Write the markdown report to a file")
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of HTTP, DNS, or TLS rows to include per section",
    )
    parser.add_argument("--tshark", help="Explicit path to tshark.exe")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    capture_path = os.path.abspath(args.capture)
    if not os.path.isfile(capture_path):
        print(f"Capture not found: {capture_path}", file=sys.stderr)
        return 1

    try:
        tshark_path = find_tshark(args.tshark)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    report = build_report(capture_path, tshark_path, max(args.limit, 1))

    if args.out:
        output_path = os.path.abspath(args.out)
        Path(output_path).write_text(report, encoding="utf-8")
        print(f"Wrote report to {output_path}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
