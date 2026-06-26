"""Module 6 — Root cause analyzer: correlate symptoms and config checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from parser import patterns as P
from parser.engine import ParsedLogBundle

from .config_consistency import ConfigConsistencyResult, ConsistencyCheck
from .core_health import CoreHealthResult
from .pdu_session import PduSessionResult
from .registration import RegistrationResult


@dataclass
class Diagnosis:
    summary: str
    root_cause: str
    confidence: str
    recommendations: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


def _failed(checks: list[ConsistencyCheck], name: str) -> bool:
    return any(c.check == name and c.status == "FAILED" for c in checks)


def analyze(
    health: CoreHealthResult,
    reg: RegistrationResult,
    pdu: PduSessionResult,
    config: ConfigConsistencyResult,
    bundle: ParsedLogBundle,
) -> Diagnosis:
    recs: list[str] = []
    evidence: list[str] = []

    # Down services
    for name, st in health.components.items():
        if st == "DOWN":
            evidence.append(f"Service {name} is DOWN")
            return Diagnosis(
                summary=f"Core service unavailable: {name}",
                root_cause=f"{name} is not running or not active",
                confidence="high",
                recommendations=[
                    f"Start or restart the {name} network function (e.g. open5gs service).",
                    "Verify SBI and PFCP peers after restart.",
                ],
                evidence=evidence,
            )

    checks = config.checks

    # Config-first rules (strong signal)
    if _failed(checks, "gnb_amf_tac") or _failed(checks, "ue_gnb_tac"):
        evidence.append("TAC mismatch between UE/gNB and AMF configuration")
        recs.extend(
            [
                "Align gNB TAC with AMF `tai` list.",
                "Ensure UE `tac` matches gNB and is allowed in AMF tracking areas.",
            ]
        )
        if reg.status == "FAIL":
            return Diagnosis(
                summary="Registration failure consistent with TAC / tracking area mismatch",
                root_cause="TAC mismatch - UE or gNB uses a tracking area not served by AMF",
                confidence="high",
                recommendations=recs,
                evidence=evidence,
            )

    if _failed(checks, "dnn_consistency"):
        evidence.append("UE DNN does not match subscriber DNN")
        recs.append(
            "Update subscriber APN/DNN in UDM/PCF or change UE requested DNN to match subscription."
        )
        if pdu.status == "FAIL":
            c = bundle.causes_sm[0] if bundle.causes_sm else None
            human = P.explain_sm_cause(c) if c is not None else ""
            if c == 27 or "DNN" in human:
                evidence.append(f"SM/PDU reject aligns with DNN issue: {human}")
            return Diagnosis(
                summary="PDU session rejection consistent with DNN mismatch",
                root_cause="Requested DNN is not configured or not allowed for this subscriber",
                confidence="high",
                recommendations=recs,
                evidence=evidence,
            )

    if _failed(checks, "slice_ue_subscriber") or _failed(checks, "slice_ue_amf"):
        evidence.append("S-NSSAI on UE does not match subscription or AMF slice support")
        recs.extend(
            [
                "Align UE SST/SD with subscriber slice and AMF `plmn_support` / NSSAI.",
                "Provision network slice in SMF/UPF if missing.",
            ]
        )
        if pdu.status == "FAIL":
            return Diagnosis(
                summary="PDU session failure consistent with slice inconsistency",
                root_cause="Slice (S-NSSAI) mismatch between UE, AMF, and subscriber",
                confidence="high",
                recommendations=recs,
                evidence=evidence,
            )

    # Log-derived MM causes
    if reg.status == "FAIL" and bundle.causes_mm:
        c = bundle.causes_mm[0]
        human = P.explain_mm_cause(c)
        evidence.append(f"NAS MM cause {c}: {human}")
        if c == 11:
            return Diagnosis(
                summary="Registration rejected by network",
                root_cause="PLMN not allowed - check SIM credentials and AMF PLMN support",
                confidence="medium",
                recommendations=[
                    "Verify IMSI MCC/MNC vs AMF `guami` / `plmn_support`.",
                    "Check subscriber is allowed on this PLMN.",
                ],
                evidence=evidence,
            )
        if c == 12:
            return Diagnosis(
                summary="Registration rejected - tracking area not allowed",
                root_cause="TAC / TA not allowed for this subscriber or roaming policy",
                confidence="medium",
                recommendations=recs
                or [
                    "Verify AMF TAI list includes gNB TAC.",
                    "Check roaming and forbidden TA lists.",
                ],
                evidence=evidence,
            )

    if pdu.status == "FAIL" and bundle.causes_sm:
        c = bundle.causes_sm[0]
        human = P.explain_sm_cause(c)
        evidence.append(f"SM cause {c}: {human}")
        return Diagnosis(
            summary="PDU session establishment failed",
            root_cause=human,
            confidence="medium",
            recommendations=[
                "Correlate SMF/UPF logs with AMF slice and DNN selection.",
                "Verify SMF session rules and UPF association.",
            ],
            evidence=evidence,
        )

    if reg.status == "PASS" and pdu.status == "PASS":
        return Diagnosis(
            summary="Registration and PDU session appear healthy in captured artifacts",
            root_cause="No dominant failure pattern detected",
            confidence="low",
            recommendations=["Continue monitoring; capture extended traces for intermittent issues."],
            evidence=evidence,
        )

    return Diagnosis(
        summary="Partial or unclear outcome - review individual module results",
        root_cause="Multiple or inconclusive signals - manual log review recommended",
        confidence="low",
        recommendations=[
            "Export fresh AMF/SMF/UE logs during reproduction.",
            "Run configuration consistency checks after any change.",
        ],
        evidence=evidence,
    )
