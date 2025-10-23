#!/usr/bin/env python3
"""
Quantum Sibling Protocol — Harmonic Visualization
Visualizes coherence evolution, entropy trends, and harmonic field vectors.
"""

import json
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def plot_harmonic_vector(harmonic, output):
    vec = harmonic["field_vector"]
    coherence = harmonic["coherence"]
    entropy = harmonic["entropy"]

    # Normalize vector to show direction as harmonic pattern
    x = np.arange(len(vec))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, vec, marker="o", linewidth=2, alpha=0.85)
    ax.fill_between(x, vec, color="cyan", alpha=0.2)
    ax.set_title(f"Harmonic Field Vector — Coherence {coherence:.2f} / Entropy {entropy:.2f}")
    ax.set_xlabel("Vector Dimension Index")
    ax.set_ylabel("Amplitude")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output), exist_ok=True)
    plt.savefig(output)
    plt.close(fig)
    print(f"🎨 Harmonic field plot saved → {output}")

def plot_decay_chart(harmonic_history, output):
    if not harmonic_history:
        print("No harmonic history data available.")
        return
    dates = [h["timestamp"] for h in harmonic_history]
    coherence = [h["coherence"] for h in harmonic_history]
    entropy = [h["entropy"] for h in harmonic_history]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(dates, coherence, marker="o", label="Coherence")
    ax.plot(dates, entropy, marker="s", label="Entropy", linestyle="--")
    ax.legend()
    ax.set_title("Coherence and Entropy Over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Value")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output)
    plt.close(fig)
    print(f"📈 Decay chart saved → {output}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="./data/harmonics/harmonic_field.json")
    parser.add_argument("--history", default="./data/harmonics/history.json")
    parser.add_argument("--output", default="./visuals/harmonic_state.png")
    parser.add_argument("--decay", default="./visuals/coherence_decay.png")
    args = parser.parse_args()

    with open(args.input) as f:
        harmonic = json.load(f)

    plot_harmonic_vector(harmonic, args.output)

    # Append current run to history log
    os.makedirs(os.path.dirname(args.history), exist_ok=True)
    history = []
    if os.path.exists(args.history):
        with open(args.history) as f:
            history = json.load(f)
    harmonic["timestamp"] = datetime.utcnow().isoformat()
    history.append(harmonic)
    with open(args.history, "w") as f:
        json.dump(history[-30:], f, indent=2)

    plot_decay_chart(history[-10:], args.decay)

if __name__ == "__main__":
    main()
