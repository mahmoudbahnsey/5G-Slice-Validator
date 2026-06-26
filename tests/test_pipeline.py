"""End-to-end pipeline tests for bundled scenarios."""

from __future__ import annotations

from pathlib import Path

from scenarios import SCENARIOS
from validator.pipeline import ValidationPipeline

ROOT = Path(__file__).resolve().parents[1]


def _run(name: str) -> dict:
    rel_log, rel_cfg = SCENARIOS[name]
    pipe = ValidationPipeline(
        project_root=ROOT,
        log_files=[ROOT / rel_log],
        config_dir=ROOT / rel_cfg,
    )
    return pipe.run()


def test_scenario_success_pass() -> None:
    r = _run("success")
    assert r["aggregate_status"] == "PASS"


def test_scenario_wrong_dnn_fail() -> None:
    r = _run("wrong_dnn")
    assert r["aggregate_status"] == "FAIL"


def test_scenario_smf_down_root_cause() -> None:
    r = _run("smf_down")
    d = r["module_6_diagnosis"]
    assert "SMF" in d.get("root_cause", "")
