"""Module 1 — Core health: AMF, SMF, UPF, NRF, UDM, AUSF."""

from __future__ import annotations

import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class CoreHealthResult:
    components: dict[str, str]
    mode: str
    notes: list[str]


def _load_probe_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"mode": "mock", "mock_status": {}, "systemd_units": {}}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _systemctl_is_active(unit: str) -> str:
    try:
        r = subprocess.run(
            ["systemctl", "is-active", unit],
            capture_output=True,
            text=True,
            timeout=5,
        )
        out = (r.stdout or "").strip()
        if out == "active":
            return "UP"
        if out == "inactive":
            return "DOWN"
        return "UNKNOWN"
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return "UNKNOWN"


def check_core_health(config_dir: Path) -> CoreHealthResult:
    probe_path = config_dir / "runtime_probe.yaml"
    cfg = _load_probe_config(probe_path)
    mode = str(cfg.get("mode", "mock")).lower()
    units: dict[str, str] = cfg.get("systemd_units") or {}
    mock: dict[str, str] = cfg.get("mock_status") or {}

    notes: list[str] = []
    if mode == "systemd" and platform.system() == "Linux":
        status: dict[str, str] = {}
        for name, unit in units.items():
            status[name] = _systemctl_is_active(unit)
        return CoreHealthResult(components=status, mode="systemd", notes=notes)

    # mock / non-Linux / fallback
    if mode == "systemd" and platform.system() != "Linux":
        notes.append("systemd mode requested but OS is not Linux; using mock_status.")

    status = {k: str(v).upper() for k, v in mock.items()}
    for key in ("AMF", "SMF", "UPF", "NRF", "UDM", "AUSF"):
        status.setdefault(key, "UNKNOWN")
    return CoreHealthResult(components=status, mode="mock", notes=notes)
