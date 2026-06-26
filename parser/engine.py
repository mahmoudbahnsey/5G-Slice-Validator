"""Parse Open5GS and UERANSIM text logs into structured events."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import patterns as P


@dataclass
class ParsedLogBundle:
    """Aggregated parse output from one or more log files."""

    events: list[dict[str, Any]] = field(default_factory=list)
    registration_flow: dict[str, bool] = field(default_factory=dict)
    pdu_session: dict[str, Any] = field(default_factory=dict)
    causes_mm: list[int] = field(default_factory=list)
    causes_sm: list[int] = field(default_factory=list)
    ip_addresses: list[str] = field(default_factory=list)
    raw_snippets: list[str] = field(default_factory=list)


class LogParserEngine:
    """Regex-driven parser with keyword mapping and error classification."""

    def __init__(self, log_paths: list[str | Path] | None = None):
        self.log_paths = [Path(p) for p in (log_paths or [])]

    def add_log(self, path: str | Path) -> None:
        self.log_paths.append(Path(path))

    def _read_all_text(self) -> str:
        chunks: list[str] = []
        for p in self.log_paths:
            if not p.exists():
                chunks.append(f"<!-- missing file: {p} -->\n")
                continue
            try:
                chunks.append(p.read_text(encoding="utf-8", errors="replace"))
            except OSError as e:
                chunks.append(f"<!-- read error {p}: {e} -->\n")
        return "\n".join(chunks)

    def parse(self, text: str | None = None) -> ParsedLogBundle:
        body = text if text is not None else self._read_all_text()
        bundle = ParsedLogBundle()

        for line in body.splitlines():
            self._scan_line(line, bundle)

        bundle.registration_flow = {
            "initial_registration_request": bool(
                P.REGISTRATION_REQUEST.search(body)
            ),
            "authentication_request": bool(P.AUTH_REQUEST.search(body)),
            "security_mode_complete": bool(P.SECURITY_MODE_COMPLETE.search(body)),
            "registration_accept": bool(P.REGISTRATION_ACCEPT.search(body)),
            "registration_reject": bool(P.REGISTRATION_REJECT.search(body)),
        }

        bundle.pdu_session = {
            "establishment_accept": bool(
                P.PDU_SESSION_ESTABLISHMENT_ACCEPT.search(body)
            ),
            "establishment_reject": bool(
                P.PDU_SESSION_ESTABLISHMENT_REJECT.search(body)
            ),
        }

        for m in P.NAS_CAUSE.finditer(body):
            c = P.extract_first_int(m)
            if c is not None:
                if P.REGISTRATION_REJECT.search(
                    body[max(0, m.start() - 200) : m.end() + 200]
                ):
                    bundle.causes_mm.append(c)

        for m in P.SM_CAUSE.finditer(body):
            bundle.causes_sm.append(int(m.group(1)))
        for m in P.SM_CAUSE_INLINE.finditer(body):
            bundle.causes_sm.append(int(m.group(1)))

        for m in P.NAS_CAUSE.finditer(body):
            ctx = body[max(0, m.start() - 120) : m.end() + 120]
            if P.PDU_SESSION_ESTABLISHMENT_REJECT.search(ctx) or "sm cause" in ctx.lower():
                c = P.extract_first_int(m)
                if c is not None and c not in bundle.causes_sm:
                    bundle.causes_sm.append(c)

        for m in P.CAUSE_EQUALS.finditer(body):
            ctx = body[max(0, m.start() - 160) : m.end() + 160]
            c = int(m.group(1))
            if P.PDU_SESSION_ESTABLISHMENT_REJECT.search(ctx) or "pdu_session" in ctx.lower():
                if c not in bundle.causes_sm:
                    bundle.causes_sm.append(c)
            if P.REGISTRATION_REJECT.search(ctx) or "registration reject" in ctx.lower():
                if c not in bundle.causes_mm:
                    bundle.causes_mm.append(c)

        for m in P.IP_ASSIGNED.finditer(body):
            ip = m.group(1) or m.group(2)
            if ip and ip not in bundle.ip_addresses:
                bundle.ip_addresses.append(ip)

        # Deduplicate causes preserving order
        def uniq(seq: list[int]) -> list[int]:
            seen: set[int] = set()
            out: list[int] = []
            for x in seq:
                if x not in seen:
                    seen.add(x)
                    out.append(x)
            return out

        bundle.causes_mm = uniq(bundle.causes_mm)
        bundle.causes_sm = uniq(bundle.causes_sm)

        # Short human-readable classification
        if bundle.registration_flow.get("registration_reject"):
            for c in bundle.causes_mm:
                bundle.events.append(
                    {
                        "type": "registration_reject",
                        "mm_cause": c,
                        "human": P.explain_mm_cause(c),
                    }
                )
        if bundle.pdu_session.get("establishment_reject"):
            for c in bundle.causes_sm or bundle.causes_mm:
                bundle.events.append(
                    {
                        "type": "pdu_session_reject",
                        "sm_cause": c,
                        "human": P.explain_sm_cause(c),
                    }
                )

        return bundle

    def _scan_line(self, line: str, bundle: ParsedLogBundle) -> None:
        if len(bundle.raw_snippets) < 50 and (
            "reject" in line.lower() or "fail" in line.lower()
        ):
            bundle.raw_snippets.append(line[:500])
