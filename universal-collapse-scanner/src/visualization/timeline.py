"""
Timeline visualization for crisis metrics
"""

from typing import List, Dict
import matplotlib.pyplot as plt
from datetime import datetime

def plot_delta_timeline(snapshots: List[Dict], title: str = "Delta (δ) Over Time"):
    """
    Plot delta values over time

    Args:
        snapshots: List of crisis snapshots with 'timestamp' and 'delta' keys
        title: Plot title
    """
    if not snapshots:
        print("No data to plot")
        return

    timestamps = [s['timestamp'] for s in snapshots]
    deltas = [s['delta'] for s in snapshots]

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, deltas, marker='o', linewidth=2, markersize=6)

    # Add threshold lines
    plt.axhline(y=0.35, color='green', linestyle='--', label='Stable threshold')
    plt.axhline(y=0.65, color='yellow', linestyle='--', label='Moderate threshold')
    plt.axhline(y=0.85, color='red', linestyle='--', label='Critical threshold')

    plt.xlabel('Time')
    plt.ylabel('Delta (δ)')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return plt.gcf()

def plot_multi_metric(snapshots: List[Dict], metrics: List[str],
                     title: str = "Crisis Metrics Over Time"):
    """
    Plot multiple metrics on same timeline

    Args:
        snapshots: List of crisis snapshots
        metrics: List of metric names to plot
        title: Plot title
    """
    if not snapshots:
        print("No data to plot")
        return

    timestamps = [s['timestamp'] for s in snapshots]

    plt.figure(figsize=(12, 6))

    for metric in metrics:
        if metric in snapshots[0]:
            values = [s.get(metric, None) for s in snapshots]
            plt.plot(timestamps, values, marker='o', label=metric.upper(), linewidth=2)

    plt.xlabel('Time')
    plt.ylabel('Metric Value')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return plt.gcf()
