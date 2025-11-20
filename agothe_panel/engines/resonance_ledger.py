"""
Universal Resonance Ledger

This module defines a ledger for tracking resonance metrics across all
Agothe Panel engines and cycles. It centralizes data such as delta_H values,
LSSE signatures, contradiction counts, paradox gradients and other
quantitative measures of the system's state. The ledger can be updated
at each evolution cycle and exported as JSON for further analysis or
archival purposes.
"""

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ResonanceRecord:
    """Container for a single resonance record entry."""
    cycle: int
    delta_h: float
    lsse: float
    contradictions: int
    paradox_gradient: float
    notes: Optional[str] = None


class UniversalResonanceLedger:
    """Ledger for storing and exporting resonance-related metrics over time."""

    def __init__(self) -> None:
        # Initialize an empty list to hold ResonanceRecord entries.
        self.records: List[ResonanceRecord] = []

    def add_record(
        self,
        cycle: int,
        delta_h: float,
        lsse: float,
        contradictions: int,
        paradox_gradient: float,
        notes: Optional[str] = None,
    ) -> None:
        """
        Append a new resonance record to the ledger.

        :param cycle: The evolution cycle number.
        :param delta_h: Global delta_H measure for the system at this cycle.
        :param lsse: Global LSSE (latent suppression) measure.
        :param contradictions: Number of contradictions detected.
        :param paradox_gradient: Metric describing paradox intensity.
        :param notes: Optional notes or annotations for this record.
        """
        record = ResonanceRecord(
            cycle=cycle,
            delta_h=delta_h,
            lsse=lsse,
            contradictions=contradictions,
            paradox_gradient=paradox_gradient,
            notes=notes,
        )
        self.records.append(record)

    def to_dict(self) -> Dict[str, Any]:
        """Return the ledger as a serializable dictionary."""
        return {"records": [asdict(record) for record in self.records]}

    def to_json(self, indent: int = 2) -> str:
        """
        Serialize the ledger records to a JSON-formatted string.

        :param indent: Indentation level for the JSON output.
        :return: A JSON string representing the ledger.
        """
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, filepath: str, indent: int = 2) -> None:
        """
        Save the ledger to a JSON file.

        :param filepath: Path to the output file.
        :param indent: Indentation level for the JSON output.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_json(indent=indent))

    def clear(self) -> None:
        """Clear all records from the ledger."""
        self.records.clear()
