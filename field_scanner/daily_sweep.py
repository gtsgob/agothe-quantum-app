"""High level orchestration logic for the daily field scanner sweep."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np

from .data_models import SensorReading, SweepConfig, clip_outliers, rolling_mean


@dataclass
class SweepResult:
    """Structured result returned after completing a sweep."""

    config: SweepConfig
    calibrated_values: Dict[str, float]
    normalized_map: Dict[str, float]
    anomalies: Dict[str, float]
    aggregate_energy: float

    def summary(self) -> str:
        """Return a human readable summary of the sweep."""

        anomaly_count = len(self.anomalies)
        return (
            f"Sweep '{self.config.name}' processed {len(self.calibrated_values)} sensors "
            f"with {anomaly_count} anomalies and aggregate energy "
            f"{self.aggregate_energy:.3f}."
        )


class FieldScanner:
    """Process sensor inputs and calculate a daily sweep report."""

    def __init__(self, config: SweepConfig) -> None:
        self.config = config

    def run_sweep(self, readings: Iterable[SensorReading]) -> SweepResult:
        """Run the daily sweep against a list of sensor readings."""

        mapped_readings = self._map_readings(readings)
        calibrated = self._apply_calibration(mapped_readings)
        normalized = self._normalize_field(calibrated)
        anomalies = self._detect_anomalies(normalized)
        energy = self._compute_energy(normalized.values())

        return SweepResult(
            config=self.config,
            calibrated_values=calibrated,
            normalized_map=normalized,
            anomalies=anomalies,
            aggregate_energy=energy,
        )

    def _map_readings(self, readings: Iterable[SensorReading]) -> Dict[str, float]:
        """Map sensor IDs to their quality weighted values."""

        mapped: Dict[str, List[float]] = {sid: [] for sid in self.config.sensor_ids}

        for reading in readings:
            if reading.sensor_id not in mapped:
                continue
            weighted = reading.value * reading.quality
            mapped[reading.sensor_id].append(weighted)

        averaged: Dict[str, float] = {}
        for sensor_id, samples in mapped.items():
            if samples:
                averaged[sensor_id] = float(np.mean(samples))
            else:
                averaged[sensor_id] = 0.0
        return averaged

    def _apply_calibration(self, readings: Dict[str, float]) -> Dict[str, float]:
        """Apply calibration offsets and temperature compensation."""

        offsets = self.config.normalized_offsets()
        calibrated = {}
        for sensor_id, value in readings.items():
            offset = offsets.get(sensor_id, 0.0)
            compensated = value - offset - self.config.temperature_compensation
            calibrated[sensor_id] = compensated
        return calibrated

    def _normalize_field(self, readings: Dict[str, float]) -> Dict[str, float]:
        """Normalize readings by their rolling mean and noise floor."""

        series = list(readings.values())
        if not series:
            return {}

        baseline = rolling_mean(series, max(1, self.config.history_window))
        clipped = clip_outliers(series, limit=max(1.0, self.config.noise_floor))

        normalized: Dict[str, float] = {}
        for (sensor_id, value), base, clipped_value in zip(
            readings.items(), baseline, clipped
        ):
            if base == 0:
                normalized[sensor_id] = 0.0
            else:
                normalized[sensor_id] = (clipped_value - base) / abs(base)
        return normalized

    def _detect_anomalies(self, readings: Dict[str, float]) -> Dict[str, float]:
        """Find sensors that exceed a 2 sigma deviation."""

        if not readings:
            return {}

        values = np.array(list(readings.values()))
        mean = float(np.mean(values))
        std = float(np.std(values)) or 1.0
        threshold = mean + 2 * std

        anomalies: Dict[str, float] = {}
        for sensor_id, value in readings.items():
            if value >= threshold:
                anomalies[sensor_id] = value
        return anomalies

    def _compute_energy(self, readings: Iterable[float]) -> float:
        """Aggregate energy heuristic based on normalized readings."""

        total = 0.0
        for value in readings:
            total += float(value) ** 2
        return float(np.sqrt(total))


def build_sample_readings(config: SweepConfig, seed: int = 7) -> List[SensorReading]:
    """Generate deterministic sample readings for demos or tests."""

    rng = np.random.default_rng(seed)
    readings = []
    for sensor_id in config.sensor_ids:
        position = rng.normal(size=3)
        value = rng.normal(loc=5.0, scale=2.0)
        quality = float(np.clip(rng.uniform(), 0.5, 1.0))
        readings.append(
            SensorReading(
                sensor_id=sensor_id,
                value=float(value),
                position=position,
                quality=quality,
            )
        )
    return readings
