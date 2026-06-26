"""Tests for log parser."""

from __future__ import annotations

from pathlib import Path

from parser.engine import LogParserEngine

ROOT = Path(__file__).resolve().parents[1]


def test_parser_success_log_extracts_registration_and_pdu() -> None:
    text = (ROOT / "logs" / "scenario_success.log").read_text(encoding="utf-8")
    engine = LogParserEngine([])
    bundle = engine.parse(text)
    assert bundle.registration_flow["registration_accept"] is True
    assert bundle.pdu_session["establishment_accept"] is True
    assert bundle.ip_addresses


def test_parser_dnn_reject_cause_27() -> None:
    text = (ROOT / "logs" / "scenario_wrong_dnn.log").read_text(encoding="utf-8")
    bundle = LogParserEngine([]).parse(text)
    assert 27 in bundle.causes_sm or 27 in bundle.causes_mm


def test_mm_cause_mapping_non_empty() -> None:
    from parser import patterns as P

    assert "PLMN" in P.explain_mm_cause(11)
    assert "DNN" in P.explain_sm_cause(27)
