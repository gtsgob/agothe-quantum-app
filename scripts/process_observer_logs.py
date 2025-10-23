#!/usr/bin/env python3
"""
process_observer_logs.py — merges AI reflections into memory_core.json
"""

import json, os, argparse, random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    state = json.load(open(args.state))
    logs = []

    for f in os.listdir(args.input):
        if f.endswith(".json"):
            with open(os.path.join(args.input, f)) as file:
                logs.append(json.load(file))

    if not logs:
        print("No new observer logs.")
        return

    # Compute average signal strength & update memory
    avg_signal = sum(log["signal_strength"] for log in logs) / len(logs)
    state["learning_cycles"] += 1
    state["observer_effect"] = round(avg_signal, 3)
    state["last_signals"] = [log["semantic_field"] for log in logs]
    state["entropy_vector"] = [round(random.random(), 3) for _ in range(5)]

    json.dump(state, open(args.output, "w"), indent=2)
    print(f"Integrated {len(logs)} observer logs → coherence {avg_signal:.3f}")

if __name__ == "__main__":
    main()
