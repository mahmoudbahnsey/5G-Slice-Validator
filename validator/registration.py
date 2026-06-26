"""Module 2 — Registration validator from parsed logs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from parser.engine import ParsedLogBundle


@dataclass
class RegistrationResult:
    status: str
    steps: dict[str, bool]
    reason: str | None


def validate_registration(bundle: ParsedLogBundle) -> RegistrationResult:
    flow = bundle.registration_flow
    reject = flow.get("registration_reject", False)
    accept = flow.get("registration_accept", False)

    steps = {
        "initial_registration_request": flow.get(
            "initial_registration_request", False
        ),
        "authentication_request": flow.get("authentication_request", False),
        "security_mode_complete": flow.get("security_mode_complete", False),
        "registration_accept": accept,
    }

    if reject:
        cause = bundle.causes_mm[0] if bundle.causes_mm else None
        from parser import patterns as P

        msg = P.explain_mm_cause(cause) if cause is not None else "Registration rejected"
        return RegistrationResult(status="FAIL", steps=steps, reason=msg)

    if accept and steps["initial_registration_request"]:
        return RegistrationResult(status="PASS", steps=steps, reason=None)

    if not flow.get("initial_registration_request"):
        return RegistrationResult(
            status="FAIL",
            steps=steps,
            reason="No Initial Registration Request observed in logs",
        )

    return RegistrationResult(
        status="WARN",
        steps=steps,
        reason="Incomplete registration flow in captured logs",
    )
