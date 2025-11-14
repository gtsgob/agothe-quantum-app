"""
Crisis data models
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class Crisis:
    """Represents a crisis for analysis"""
    name: str
    crisis_type: str  # 'humanitarian', 'political', 'economic', etc.
    start_date: datetime
    location: str
    severity_metrics: Dict[str, float]
    status: str = "ongoing"
    end_date: Optional[datetime] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class CrisisSnapshot:
    """Point-in-time crisis measurement"""
    crisis_id: str
    timestamp: datetime
    delta: float
    lsse: float
    psi: Optional[float] = None
    gamma: Optional[float] = None
    geometries: List[str] = None

    def __post_init__(self):
        if self.geometries is None:
            self.geometries = []
