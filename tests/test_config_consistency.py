"""Configuration consistency module tests."""

from __future__ import annotations

from pathlib import Path

from validator.config_consistency import validate_config_consistency

ROOT = Path(__file__).resolve().parents[1]


def test_baseline_config_passes() -> None:
    r = validate_config_consistency(ROOT / "configs")
    assert r.overall == "PASS"


def test_wrong_dnn_fails() -> None:
    r = validate_config_consistency(ROOT / "configs" / "scenarios" / "wrong_dnn")
    names = {c.check for c in r.checks if c.status == "FAILED"}
    assert "dnn_consistency" in names


def test_wrong_tac_fails() -> None:
    r = validate_config_consistency(ROOT / "configs" / "scenarios" / "wrong_tac")
    assert r.overall == "FAIL"
