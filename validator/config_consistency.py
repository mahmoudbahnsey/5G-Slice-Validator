"""Module 4 — Configuration consistency: DNN, TAC, S-NSSAI."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def _fmt_sd(sd: Any) -> str:
    if sd is None:
        return ""
    s = str(sd).strip()
    if s.startswith("0x") or s.startswith("0X"):
        return s[2:].upper().zfill(6)
    return s.upper().zfill(6) if s.isalnum() else s.upper()


def _slice_key(d: dict[str, Any]) -> tuple[int, str]:
    sn = d.get("s_nssai") or d.get("subscribed_slice") or {}
    sst = int(sn.get("sst", 0))
    sd = _fmt_sd(sn.get("sd"))
    return (sst, sd)


@dataclass
class ConsistencyCheck:
    check: str
    status: str
    expected: str
    actual: str
    detail: str


@dataclass
class ConfigConsistencyResult:
    checks: list[ConsistencyCheck] = field(default_factory=list)

    @property
    def overall(self) -> str:
        if any(c.status == "FAILED" for c in self.checks):
            return "FAIL"
        if any(c.status == "WARN" for c in self.checks):
            return "WARN"
        return "PASS"


def validate_config_consistency(config_dir: Path) -> ConfigConsistencyResult:
    ue = _load(config_dir / "ue.yaml")
    gnb = _load(config_dir / "gnb.yaml")
    amf = _load(config_dir / "amf.yaml")
    sub = _load(config_dir / "subscriber.yaml")

    result = ConfigConsistencyResult()

    # DNN
    ue_dnn = str(ue.get("dnn", "") or "")
    sub_dnn = str(sub.get("subscribed_dnn", "") or "")
    if ue_dnn and sub_dnn:
        ok = ue_dnn == sub_dnn
        result.checks.append(
            ConsistencyCheck(
                check="dnn_consistency",
                status="PASSED" if ok else "FAILED",
                expected=sub_dnn,
                actual=ue_dnn,
                detail="UE requested DNN must match subscriber profile",
            )
        )

    # TAC
    ue_tac = ue.get("tac")
    gnb_tac = gnb.get("tac")
    amf_tacs: list[int] = []
    tai = amf.get("amf", {}).get("tai") or amf.get("tai")
    if isinstance(tai, list):
        for t in tai:
            if isinstance(t, dict) and "tac" in t:
                amf_tacs.append(int(t["tac"]))
    if ue_tac is not None and gnb_tac is not None:
        g_ok = int(ue_tac) == int(gnb_tac)
        result.checks.append(
            ConsistencyCheck(
                check="ue_gnb_tac",
                status="PASSED" if g_ok else "FAILED",
                expected=str(gnb_tac),
                actual=str(ue_tac),
                detail="UE TAC must match gNB TAC",
            )
        )
    if gnb_tac is not None and amf_tacs:
        in_amf = int(gnb_tac) in amf_tacs
        result.checks.append(
            ConsistencyCheck(
                check="gnb_amf_tac",
                status="PASSED" if in_amf else "FAILED",
                expected=f"one of {amf_tacs}",
                actual=str(gnb_tac),
                detail="gNB TAC must be listed in AMF TAI configuration",
            )
        )

    # Slice S-NSSAI
    ue_sl = _slice_key(ue)
    sub_sl = _slice_key(sub)
    amf_slices: list[tuple[int, str]] = []
    ps = amf.get("amf", {}).get("plmn_support") or amf.get("plmn_support")
    if isinstance(ps, list):
        for block in ps:
            sn_list = block.get("s_nssai") if isinstance(block, dict) else None
            if isinstance(sn_list, list):
                for sn in sn_list:
                    if isinstance(sn, dict):
                        amf_slices.append(
                            (int(sn.get("sst", 0)), _fmt_sd(sn.get("sd")))
                        )

    if ue_sl[0] and sub_sl[0]:
        s_ok = ue_sl == sub_sl
        result.checks.append(
            ConsistencyCheck(
                check="slice_ue_subscriber",
                status="PASSED" if s_ok else "FAILED",
                expected=f"sst={sub_sl[0]}, sd={sub_sl[1]}",
                actual=f"sst={ue_sl[0]}, sd={ue_sl[1]}",
                detail="UE slice must match subscriber slice",
            )
        )

    if ue_sl[0] and amf_slices:
        in_amf = ue_sl in amf_slices
        result.checks.append(
            ConsistencyCheck(
                check="slice_ue_amf",
                status="PASSED" if in_amf else "FAILED",
                expected=f"AMF offers {amf_slices}",
                actual=f"sst={ue_sl[0]}, sd={ue_sl[1]}",
                detail="UE slice must be supported by AMF PLMN configuration",
            )
        )

    # PLMN quick check
    m_ue = f"{ue.get('mcc','')}{ue.get('mnc','')}"
    m_sub = f"{sub.get('plmn',{}).get('mcc','')}{sub.get('plmn',{}).get('mnc','')}"
    if m_ue and m_sub:
        p_ok = m_ue == m_sub
        result.checks.append(
            ConsistencyCheck(
                check="plmn_consistency",
                status="PASSED" if p_ok else "FAILED",
                expected=m_sub,
                actual=m_ue,
                detail="UE PLMN should match subscriber PLMN",
            )
        )

    return result
