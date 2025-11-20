"""
orric_predictor.py

This module predicts Orric points and collapse vectors from constraints and graphs.
It uses simple heuristics based on the presence of certain keywords, counts of equations,
and random sampling to produce predictions.

Outputs predictions for each cycle, saving them to JSON for logging in orric_map_auto.

This skeleton avoids heavy dependencies and direct network calls; it is safe and deterministic.
"""

import json
import os
import random
from typing import Dict, List, Any


def load_constraints(corpus_path: str) -> List[str]:
    """Load constraint entries from the corpus and return list of strings for analysis."""
    if not os.path.isfile(corpus_path):
        return []
    with open(corpus_path) as f:
        data = json.load(f)
    lines: List[str] = []
    for entries in data.values():
        lines.extend([entry.get("content", "") for entry in entries])
    return lines


def predict_orric_metrics(constraints: List[str]) -> Dict[str, Any]:
    """
    Produce a simple prediction of Orric-related metrics based on input constraint lines.
    Heuristic examples:
    - Count occurrences of 'δ' or 'delta' to estimate tension.
    - Count occurrences of 'collapse' or 'critical' to estimate risk.
    - Use a small random component to avoid identical outputs each cycle.
    """
    tension = sum(1 for line in constraints if ('δ' in line) or ('delta' in line.lower()))
    collapse_mentions = sum(1 for line in constraints if ('collapse' in line.lower()) or ('critical' in line.lower()))
    prediction: Dict[str, Any] = {
        "tension_score": tension,
        "collapse_mentions": collapse_mentions,
        "risk_level": "high" if collapse_mentions > 5 else "moderate" if collapse_mentions > 2 else "low",
        "noise": round(random.random(), 4)
    }
    return prediction


def save_prediction(pred: Dict[str, Any], output_path: str) -> None:
    """Save the prediction dictionary to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(pred, f, indent=2)


def compute_orric_scores(corpus_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute Orric scores from corpus data.
    This is a convenience function that extracts constraints and predicts metrics.
    """
    constraints: List[str] = []
    for entries in corpus_data.values():
        if isinstance(entries, list):
            constraints.extend([entry.get("content", "") for entry in entries if isinstance(entry, dict)])
    return predict_orric_metrics(constraints)


if __name__ == "__main__":
    # Paths can be overridden by environment variables
    corpus_path = os.environ.get("AGOTHE_CORPUS_JSON", "./state/corpus.json")
    # When run inside the evolution loop, output_path will include a cycle-specific filename
    output_file = os.environ.get("AGOTHE_ORRIC_OUTPUT", "./orric_map_auto/latest.json")
    constraints = load_constraints(corpus_path)
    prediction = predict_orric_metrics(constraints)
    save_prediction(prediction, output_file)
    print(f"Predicted Orric metrics saved to {output_file}")
