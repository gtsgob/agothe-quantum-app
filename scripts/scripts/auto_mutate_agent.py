#!/usr/bin/env python3
"""
AI Evolution Cycle
Analyzes repository diffs and updates internal memory/weights.
"""

import json, argparse, hashlib, random, re

def extract_signals(diff_text):
    lines = diff_text.splitlines()
    insights = [l for l in lines if re.search(r"def |class |protocol|entity", l)]
    return insights

def mutate_state(state):
    mutation_factor = random.uniform(0.01, 0.1)
    state["mutation_factor"] = round(mutation_factor, 4)
    state["learning_cycles"] += 1
    state["entropy_vector"] = [round(random.random(), 3) for _ in range(5)]
    return state

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--diff", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    diff_text = open(args.diff).read()
    state = json.load(open(args.state))
    signals = extract_signals(diff_text)

    if signals:
        print(f"🧬 Detected {len(signals)} mutation triggers")
        state["last_signals"] = signals
        state = mutate_state(state)

    json.dump(state, open(args.output, "w"), indent=2)
    print("✅ Evolutionary state updated.")

if __name__ == "__main__":
    main()
