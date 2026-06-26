"""Module 3 — PDU session validation."""

from __future__ import annotations

from dataclasses import dataclass

from parser.engine import ParsedLogBundle


@dataclass
class PduSessionResult:
    status: str
    has_ip: bool
    session_active: bool
    reachable_upf: bool | None
    reason: str | None
    details: dict[str, object]


def validate_pdu_session(
    bundle: ParsedLogBundle,
    ping_ok: bool | None = None,
) -> PduSessionResult:
    pdu = bundle.pdu_session
    accept = pdu.get("establishment_accept", False)
    reject = pdu.get("establishment_reject", False)
    ips = bundle.ip_addresses

    if reject:
        from parser import patterns as P

        c = bundle.causes_sm[0] if bundle.causes_sm else (
            bundle.causes_mm[0] if bundle.causes_mm else None
        )
        reason = P.explain_sm_cause(c) if c is not None else "PDU session establishment rejected"
        return PduSessionResult(
            status="FAIL",
            has_ip=bool(ips),
            session_active=False,
            reachable_upf=None,
            reason=reason,
            details={"sm_cause": c, "ip_list": ips},
        )

    has_ip = bool(ips)
    session_active = accept or has_ip

    # Without live ping, infer None unless caller passes ping result
    upf_ok: bool | None = ping_ok
    if ping_ok is None and session_active and has_ip:
        upf_ok = None  # unknown without runtime test

    if session_active and has_ip:
        return PduSessionResult(
            status="PASS",
            has_ip=True,
            session_active=True,
            reachable_upf=upf_ok,
            reason=None,
            details={"ip_list": ips},
        )

    return PduSessionResult(
        status="WARN",
        has_ip=has_ip,
        session_active=session_active,
        reachable_upf=upf_ok,
        reason="No clear PDU session accept or IP assignment in logs",
        details={"ip_list": ips},
    )
