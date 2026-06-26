"""Streamlit dashboard — 5G Slice Validator visualization layer."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scenarios import SCENARIOS  # noqa: E402
from validator.pipeline import ValidationPipeline  # noqa: E402

st.set_page_config(
    page_title="5G Slice Validator",
    page_icon="📡",
    layout="wide",
)

DEFAULT_JSON = ROOT / "reports" / "last_run.json"


def load_report(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def run_live(scenario: str | None) -> dict:
    log_paths: list[Path] = []
    cfg_dir: Path | None = None
    if scenario and scenario in SCENARIOS:
        rel_log, rel_cfg = SCENARIOS[scenario]
        log_paths = [ROOT / rel_log]
        cfg_dir = ROOT / rel_cfg
    pipe = ValidationPipeline(
        project_root=ROOT,
        log_files=log_paths or None,
        config_dir=cfg_dir,
    )
    return pipe.run()


def status_badge(status: str) -> str:
    s = (status or "").upper()
    if s == "PASS" or s == "PASSED":
        return "🟢"
    if s == "WARN":
        return "🟡"
    return "🔴"


def main_ui() -> None:
    st.title("5G Slice Validator")
    st.caption("Open5GS + UERANSIM — configuration consistency, registration, PDU session, diagnosis.")

    tab_home, tab_val, tab_err, tab_rec = st.tabs(
        ["Overview", "Validation", "Errors & causes", "Recommendations"]
    )

    with st.sidebar:
        st.subheader("Run")
        scenario = st.selectbox(
            "Demo scenario",
            options=[None] + list(SCENARIOS.keys()),
            format_func=lambda x: "Default (success log)" if x is None else x,
        )
        if st.button("Run validation now", type="primary"):
            with st.spinner("Running pipeline…"):
                report = run_live(scenario)
                out_path = ROOT / "reports" / "last_run.json"
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(
                    json.dumps(report, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                st.session_state["last_report"] = report
                st.success("Validation finished.")
        path_json = st.text_input("Load JSON report", value=str(DEFAULT_JSON))
        if st.button("Load from file"):
            r = load_report(Path(path_json))
            if r:
                st.session_state["last_report"] = r
                st.success("Loaded.")
            else:
                st.error("Could not read JSON.")

    report = st.session_state.get("last_report") or load_report(DEFAULT_JSON)
    if report is None:
        report = run_live("success")
        st.session_state["last_report"] = report

    health = report.get("module_1_core_health", {})
    comp = health.get("components") or {}
    reg = report.get("module_2_registration", {})
    pdu = report.get("module_3_pdu_session", {})
    agg = report.get("aggregate_status", "?")
    diag = report.get("module_6_diagnosis", {})

    with tab_home:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Aggregate", f"{status_badge(agg)} {agg}")
        c2.metric("AMF", comp.get("AMF", "—"))
        c3.metric("Registration", reg.get("status", "—"))
        c4.metric("PDU session", pdu.get("status", "—"))

        st.markdown("#### Component status")
        rows = [{"Component": k, "Status": v} for k, v in comp.items()]
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("#### Registration steps")
        steps = reg.get("steps") or {}
        st.json(steps)

    with tab_val:
        cfg = report.get("module_4_config_consistency", {})
        st.subheader("Configuration consistency")
        st.write(f"Overall: **{cfg.get('overall')}**")
        checks = cfg.get("checks") or []
        if checks:
            st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)

        st.subheader("PDU session details")
        st.json(
            {
                k: report["module_3_pdu_session"].get(k)
                for k in ("status", "has_ip", "session_active", "reachable_upf", "reason", "details")
                if k in report.get("module_3_pdu_session", {})
            }
        )

    with tab_err:
        pr = report.get("module_5_parser_summary", {})
        st.write("**MM causes:**", pr.get("causes_mm"))
        st.write("**SM causes:**", pr.get("causes_sm"))
        st.write("**Parsed IPs:**", pr.get("ip_addresses"))
        st.subheader("Events")
        st.json(pr.get("events") or [])

        reg_reason = reg.get("reason")
        pdu_reason = pdu.get("reason")
        if reg_reason:
            st.error(f"Registration: {reg_reason}")
        if pdu_reason:
            st.warning(f"PDU session: {pdu_reason}")

    with tab_rec:
        st.markdown(f"### Root cause ({diag.get('confidence', '')})")
        st.info(diag.get("root_cause", ""))
        st.markdown("### Recommendations")
        for line in diag.get("recommendations") or []:
            st.write(f"- {line}")
        st.markdown("### Evidence")
        for line in diag.get("evidence") or []:
            st.caption(line)


if __name__ == "__main__":
    main_ui()
