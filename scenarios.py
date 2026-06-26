"""Bundled demo scenarios: sample log + matching config directory."""

from __future__ import annotations

from pathlib import Path
from typing import Final

# Values are relative to project root (directory containing main.py).
SCENARIOS: Final[dict[str, tuple[str, str]]] = {
    "success": ("logs/scenario_success.log", "configs"),
    "wrong_dnn": ("logs/scenario_wrong_dnn.log", "configs/scenarios/wrong_dnn"),
    "wrong_tac": ("logs/scenario_wrong_tac.log", "configs/scenarios/wrong_tac"),
    "wrong_slice": ("logs/scenario_wrong_slice.log", "configs/scenarios/wrong_slice"),
    "smf_down": ("logs/scenario_smf_down.log", "configs/scenarios/smf_down"),
}


def scenario_paths(root: Path, name: str) -> tuple[Path, Path]:
    rel_log, rel_cfg = SCENARIOS[name]
    return root / rel_log, root / rel_cfg
