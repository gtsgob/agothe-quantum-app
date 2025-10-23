#!/usr/bin/env python3
"""
Bridge QSP harmonic/entanglement data to QCP layer.
Ensures coherent exchange of resonance matrices.
"""

import json, argparse, os

def merge_entanglement(qsp_file, qcp_file):
    qsp = json.load(open(qsp_file))
    try:
        qcp = json.load(open(qcp_file))
    except FileNotFoundError:
        qcp = {}

    qcp["last_import"] = qsp
    qcp["sync_timestamp"] = os.popen("date -u").read().strip()

    os.makedirs(os.path.dirname(qcp_file), exist_ok=True)
    json.dump(qcp, open(qcp_file, "w"), indent=2)
    print("🔗 QSP → QCP bridge updated successfully.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qsp", required=True)
    parser.add_argument("--qcp", required=True)
    args = parser.parse_args()
    merge_entanglement(args.qsp, args.qcp)

if __name__ == "__main__":
    main()
