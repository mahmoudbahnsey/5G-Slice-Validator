"""Generate Markdown / HTML-friendly validation reports from pipeline output."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def write_markdown_report(report: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(f"# {report.get('project', 'Validation Report')}\n")
    lines.append(f"**Aggregate status:** `{report.get('aggregate_status', 'UNKNOWN')}`\n")

    mh = report.get("module_6_diagnosis", {})
    lines.append("## Executive summary\n")
    lines.append(f"- **Summary:** {mh.get('summary', '')}")
    lines.append(f"- **Root cause:** {mh.get('root_cause', '')}")
    lines.append(f"- **Confidence:** {mh.get('confidence', '')}\n")

    if mh.get("recommendations"):
        lines.append("### Recommendations\n")
        for r in mh["recommendations"]:
            lines.append(f"- {r}")
        lines.append("")

    ch = report.get("module_1_core_health", {})
    lines.append("## Module 1 — Core health\n")
    lines.append(f"- Mode: `{ch.get('mode')}`")
    comp = ch.get("components") or {}
    for k, v in comp.items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    reg = report.get("module_2_registration", {})
    lines.append("## Module 2 — Registration\n")
    lines.append(f"- Status: **{reg.get('status')}**")
    if reg.get("reason"):
        lines.append(f"- Reason: {reg['reason']}")
    steps = reg.get("steps") or {}
    for name, ok in steps.items():
        lines.append(f"  - {name}: {'yes' if ok else 'no'}")
    lines.append("")

    pdu = report.get("module_3_pdu_session", {})
    lines.append("## Module 3 — PDU session\n")
    lines.append(f"- Status: **{pdu.get('status')}**")
    lines.append(f"- IP assigned: {pdu.get('has_ip')}")
    lines.append(f"- Session active: {pdu.get('session_active')}")
    if pdu.get("reason"):
        lines.append(f"- Reason: {pdu['reason']}")
    lines.append("")

    cfg = report.get("module_4_config_consistency", {})
    lines.append("## Module 4 — Configuration consistency\n")
    lines.append(f"- Overall: **{cfg.get('overall')}**")
    for c in cfg.get("checks") or []:
        lines.append(
            f"- `{c.get('check')}` → {c.get('status')} (expected `{c.get('expected')}`, actual `{c.get('actual')}`)"
        )
    lines.append("")

    pr = report.get("module_5_parser_summary", {})
    lines.append("## Module 5 — Parsed causes\n")
    lines.append(f"- MM causes: {pr.get('causes_mm')}")
    lines.append(f"- SM causes: {pr.get('causes_sm')}")
    lines.append(f"- IP addresses: {pr.get('ip_addresses')}\n")

    lines.append("## Inputs\n")
    lines.append(f"- Config dir: `{report.get('config_dir')}`")
    lines.append(f"- Logs: {report.get('logs')}\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
