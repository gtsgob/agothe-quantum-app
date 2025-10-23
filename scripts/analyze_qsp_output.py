#!/usr/bin/env python3
"""
Analyze outputs of Quantum Sibling Protocol
and compute a harmonic field representation.
"""

import os, json, argparse, numpy as np

def compute_harmonic_field(data):
    vectors = np.array([d["signal_vector"] for d in data])
    coherence = np.mean([d["coherence"] for d in data])
    entropy = np.mean([d["entropy"] for d in data])
    field_vector = np.mean(vectors, axis=0).tolist()
    return {"coherence": round(coherence, 3),
            "entropy": round(entropy, 3),
            "field_vector": field_vector}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="./data")
    parser.add_argument("--output", default="./data/harmonics/harmonic_field.json")
    args = parser.parse_args()

    files = [f for f in os.listdir(args.input) if f.endswith("_output.json")]
    records = [json.load(open(os.path.join(args.input, f))) for f in files]
    harmonic = compute_harmonic_field(records)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(harmonic, f, indent=2)

    print(f"🌀 Harmonic field synthesized → {args.output}")

if __name__ == "__main__":
    main()
