"""Data models supporting the field scanner daily sweep pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import numpy as np


@dataclass
class SensorReading:
    """Single reading captured by the field scanner."""

    sensor_id: str
    value: float
    position: np.ndarray
    quality: float = 1.0

    def __post_init__(self) -> None:
        self.position = np.asarray(self.position, dtype=float)
        if self.position.shape != (3,):
            raise ValueError("position must be a 3D vector")
        if not 0.0 <= self.quality <= 1.0:
            raise ValueError("quality must be within [0, 1]")


@dataclass
class SweepConfig:
    """Configuration values for a daily sweep."""

    name: str
    sensor_ids: List[str]
    calibration_offsets: Dict[str, float] = field(default_factory=dict)
    temperature_compensation: float = 0.0
    noise_floor: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    history_window: int = 7

    def normalized_offsets(self) -> Dict[str, float]:
        """Return calibration offsets with defaults for missing sensors."""

        return {sid: self.calibration_offsets.get(sid, 0.0) for sid in self.sensor_ids}


def rolling_mean(values: Iterable[float], window: int) -> List[float]:
    """Compute a trailing rolling mean for an iterable."""

    buffer: List[float] = []
    means: List[float] = []

    for value in values:
        buffer.append(float(value))
        if len(buffer) > window:
            buffer.pop(0)
        means.append(sum(buffer) / len(buffer))

    return means


def clip_outliers(values: Iterable[float], limit: float) -> List[float]:
    """Clip values to the provided symmetric limit."""

    clipped: List[float] = []
    for value in values:
        clipped.append(float(np.clip(value, -limit, limit)))
    return clipped
