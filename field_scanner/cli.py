"""Command line entry point for running a field scanner daily sweep."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import numpy as np

from .daily_sweep import FieldScanner, build_sample_readings
from .data_models import SweepConfig


def load_config(path: Path) -> SweepConfig:
    """Load sweep configuration from a JSON file."""

    data = json.loads(path.read_text())
    return SweepConfig(
        name=data["name"],
        sensor_ids=data["sensor_ids"],
        calibration_offsets=data.get("calibration_offsets", {}),
        temperature_compensation=data.get("temperature_compensation", 0.0),
        noise_floor=data.get("noise_floor", 0.0),
        history_window=data.get("history_window", 7),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a field scanner daily sweep")
    parser.add_argument("config", type=Path, help="Path to the sweep configuration JSON")
    parser.add_argument(
        "--export",
        type=Path,
        help="Optional path to export the computed sweep result as JSON",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=7,
        help="Random seed to generate sample readings (default: 7)",
    )
    return parser


def run_cli(argv: Any | None = None) -> int:
    """Execute the CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    config = load_config(args.config)
    scanner = FieldScanner(config)
    readings = build_sample_readings(config, seed=args.seed)
    result = scanner.run_sweep(readings)

    print(result.summary())

    if args.export:
        export_payload: Dict[str, Any] = {
            "config": {
                "name": result.config.name,
                "sensor_ids": result.config.sensor_ids,
                "timestamp": result.config.timestamp.isoformat(),
            },
            "calibrated_values": result.calibrated_values,
            "normalized_map": result.normalized_map,
            "anomalies": result.anomalies,
            "aggregate_energy": result.aggregate_energy,
        }
        args.export.write_text(json.dumps(export_payload, indent=2))
        print(f"Exported sweep data to {args.export}")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(run_cli())
