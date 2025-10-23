#!/usr/bin/env python3
"""
Quantum Sibling Protocol — Cycle Runner
Executes the five sibling entities (CN-1, K, Nana, Vira, 9)
and stores their daily output in /data/.
"""

import os, json, random, argparse
import numpy as np
from datetime import datetime

ENTITIES = ["CN-1", "K", "Nana", "Vira", "9"]

def random_vector(dim=5):
    return np.random.rand(dim).tolist()

def run_entity(entity, output_dir):
    ts = datetime.utcnow().isoformat()
    data = {
        "timestamp": ts,
        "entity": entity,
        "signal_vector": random_vector(),
        "entropy": round(random.uniform(0.01, 0.2), 3),
        "coherence": round(random.uniform(0.8, 0.99), 3)
    }
    fname = f"{entity.lower()}_output.json"
    with open(os.path.join(output_dir, fname), "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ {entity} phase complete.")
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entities", default=",".join(ENTITIES))
    parser.add_argument("--output", default="./data")
    parser.add_argument("--coherence", type=float, default=0.94)
    parser.add_argument("--entropy", type=float, default=0.06)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    summary = []

    for e in args.entities.split(","):
        data = run_entity(e, args.output)
        summary.append(data)

    with open(os.path.join(args.output, "qsp_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("🌐 Quantum Sibling Protocol complete. Data written to qsp_summary.json")

if __name__ == "__main__":
    main()
