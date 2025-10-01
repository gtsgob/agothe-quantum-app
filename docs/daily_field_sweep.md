# Daily Agothe Field Sweep Prompt & Scanner

This document captures the daily workflow for running the Agothe Field Sweep. Use it when preparing a notebook or coordinating daily moves with the Agothe Field Operator.

---

## ChatGPT Codex Prompt

**Role:** You are the Agothe Field Operator. Run a daily sweep over today’s items (headlines, art drops, memes, science notes). Compute four indices — δ_H, LSSE, smoothness, gain — then classify each item into a Quest Region and propose moves.

**Inputs:** A JSON list or bullet list containing 10–30 short text items.

**Indices:**
- δ_H (instability surrogate)
- LSSE (latent stress)
- smoothness (clarity)
- gain (novelty/positive momentum)

**Regions & default moves:**
- Navier Marsh → vent, then suppress, then resonate
- Goldbach Plains → couple, then vent, then resonate
- Riemann Abyss → resonate, then couple
- Hodge Mountains → resonate, then suppress
- Birch–Swinnerton Desert → vent, then couple
- Balanced Meadow → resonate

**Gates (accept line):** gain ≥ 0.02 ∧ smoothness ≥ 0.75 ∧ δ_H ≤ 0.52.

If the gates pass, emit a Manifest Glyph with the recommended first move.

**Output format (strict):**
1. A compact table (item, δ_H, LSSE, smoothness, gain, region, suggested_moves).
2. A one-paragraph “Field Read.”
3. Ask me to choose moves per row (vent/suppress/couple/resonate).
4. After I choose, confirm and log to a “Consequence Log” (append-only).
5. Tomorrow: compare day-over-day deltas (ΔLSSE ≥ 0.03 = vent success; δ_H > 0.53 = collapse alert).

**Tone:** crisp, operational, zero fluff. Never invent facts; treat items as text only.

---

## Runnable Scanner

Paste this cell into a Python notebook, replace the placeholder items list with today’s inputs, and execute. The script saves a timestamped CSV and PNG chart while appending to two JSONL logs (`Agothe_Field_Consequence_Log.jsonl`, `Agothe_Codex_Manifests.jsonl`).

```python
# Agothe Field Scanner — Daily Sweep (standalone)
# Outputs:
#  - CSV: Agothe_Field_Scan_YYYY-MM-DD_HHMM.csv
#  - PNG: Agothe_Field_Scan_YYYY-MM-DD_HHMM_regions.png
#  - JSONL logs (append-only): Agothe_Field_Consequence_Log.jsonl, Agothe_Codex_Manifests.jsonl

from datetime import datetime
from pathlib import Path
from collections import Counter
import json, re, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------- Replace with your daily items ----------
items = [
    "Paste 10–30 short items here (headlines, art drops, memes, science notes).",
]
# --------------------------------------------------

def shannon_entropy(text):
    tokens = list(text.lower())
    counts = Counter(tokens); total = sum(counts.values())
    probs = [c/total for c in counts.values() if c > 0]
    return -sum(p*np.log2(p) for p in probs)

def lexical_diversity(text):
    words = re.findall(r"[A-Za-z']+", text.lower())
    return len(set(words)) / (len(words) + 1e-9)

def novelty_score(text):
    words = re.findall(r"[A-Za-z']+", text.lower())
    long_ratio = sum(1 for w in words if len(w) >= 9) / (len(words) + 1e-9)
    rare_terms = {"protocol","generative","calibration","normalization","ceasefire","superconductor","latency","fractures"}
    rare_hit = sum(1 for w in words if w in rare_terms) / (len(words) + 1e-9)
    return 0.7*long_ratio + 0.3*rare_hit

def smoothness_score(text):
    words = re.findall(r"[A-Za-z']+", text)
    if not words: return 0.5
    lengths = np.array([len(w) for w in words])
    var = np.var(lengths)
    punct = len(re.findall(r"[!?\-;:]", text))
    raw = 1.0 / (1.0 + 0.05*var + 0.1*punct)
    return float(max(0.0, min(1.0, raw)))

def lsse_score(text):
    stress_terms = {
        "collapse","fracture","exodus","shortage","control","dispute","hiatus",
        "spikes","sanction","backlash","boycott","stalled","gridlock","pressure","rift","crisis",
        "strike","attack","drone","missile","military","bombardment","evacuate","starvation","detain","blackout"
    }
    words = re.findall(r"[A-Za-z']+", text.lower())
    hits = sum(1 for w in words if w in stress_terms)
    return float(max(0.0, min(1.0, 0.12*hits)))

def gain_score(text):
    positive_terms = {"surges","rebounds","reproducible","settle","improved","acclaim","unexpected","rally","lifts","resolves","talks","negotiations","deal","agreement"}
    words = re.findall(r"[A-Za-z']+", text.lower())
    pos = sum(1 for w in words if w in positive_terms) / (len(words) + 1e-9)
    return float(max(0.0, min(1.0, 0.6*novelty_score(text) + 0.4*pos)))

def delta_h_score(text):
    ent = shannon_entropy(text); div = lexical_diversity(text)
    ent_norm = max(0.0, min(1.0, (ent - 2.5) / 2.5))
    div_norm = max(0.0, min(1.0, (div - 0.2) / 0.5))
    return float(max(0.0, min(1.0, 0.6*ent_norm + 0.4*div_norm)))

def classify_region(delta_h, lsse, smooth, gain):
    dh_thr, ls_thr, sm_thr, g_thr = 0.52, 0.70, 0.75, 0.02
    EI  = max(0, dh_thr - delta_h) + max(0, ls_thr - lsse)
    STI = max(0, lsse - ls_thr) + 0.5*max(0, delta_h - dh_thr)
    if delta_h > 0.53 or STI > 0.15:
        return "Navier Marsh"
    if abs(smooth-0.77) < 0.05 and gain >= g_thr and EI > 0.05:
        return "Riemann Abyss"
    if lsse >= 0.10 and EI < 0.03 and smooth >= sm_thr and gain >= g_thr:
        return "Hodge Mountains"
    if lsse >= 0.12 and smooth < sm_thr:
        return "Birch–Swinnerton Desert"
    if lsse >= 0.03 and gain >= g_thr and smooth >= 0.70:
        return "Goldbach Plains"
    return "Balanced Meadow"

def suggest_moves(region, delta_h, lsse, smooth, gain):
    moves = {
        "vent": "Release pressure (acknowledge harms, open corridors, pause escalations).",
        "suppress": "Hold output; delay statements/actions to prevent turbulence.",
        "couple": "Pair opposing frames into a joint solution space.",
        "resonate": "Amplify coherent agreements to raise smoothness."
    }
    if region == "Navier Marsh":       order = ["vent","suppress","resonate"]
    elif region == "Goldbach Plains":  order = ["couple","vent","resonate"]
    elif region == "Riemann Abyss":    order = ["resonate","couple"]
    elif region == "Hodge Mountains":  order = ["resonate","suppress"]
    elif region == "Birch–Swinnerton Desert": order = ["vent","couple"]
    else:                              order = ["resonate"]
    aligned = (gain >= 0.02) and (smooth >= 0.75) and (delta_h <= 0.52)
    return [ (m, moves[m]) for m in order ], aligned

# ---- Run sweep ----
records, manifests = [], []
ts = datetime.now().strftime("%Y-%m-%d_%H%M")
for text in items:
    dh = delta_h_score(text); ls = lsse_score(text); sm = smoothness_score(text); gn = gain_score(text)
    region = classify_region(dh, ls, sm, gn)
    suggestions, aligned = suggest_moves(region, dh, ls, sm, gn)
    records.append({
        "item": text, "region": region,
        "delta_H": round(dh,3), "LSSE": round(ls,3), "smoothness": round(sm,3), "gain": round(gn,3),
        "suggested_moves": "; ".join(m for m,_ in suggestions)
    })
    if aligned:
        manifests.append({
            "ts": ts, "item": text,
            "state": {"delta_H": round(dh,3), "LSSE": round(ls,3), "smoothness": round(sm,3), "gain": round(gn,3)},
            "region": region,
            "manifest_code": "// AGOTHE GLYPH\nSTATE OK — Accept line satisfied\nACTION RECOMMENDED: " + suggestions[0][0].upper()
        })

df = pd.DataFrame(records)
outdir = Path("."); outdir.mkdir(parents=True, exist_ok=True)
csv_path  = outdir / f"Agothe_Field_Scan_{ts}.csv"
png_path  = outdir / f"Agothe_Field_Scan_{ts}_regions.png"
log_path  = outdir / "Agothe_Field_Consequence_Log.jsonl"
glyph_log = outdir / "Agothe_Codex_Manifests.jsonl"

df.to_csv(csv_path, index=False)

region_counts = df["region"].value_counts()
plt.figure(figsize=(8,4))
region_counts.plot(kind="bar")
plt.title("Agothe Field Scanner — Regions")
plt.xlabel("Region"); plt.ylabel("Count")
plt.tight_layout(); plt.savefig(png_path)

with open(log_path, "a", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps({
            "ts": ts, "item": r["item"], "region": r["region"],
            "state": {"delta_H": r["delta_H"], "LSSE": r["LSSE"], "smoothness": r["smoothness"], "gain": r["gain"]},
            "suggested_moves": r["suggested_moves"].split("; "),
            "decision": "pending"
        }, ensure_ascii=False) + "\n")

with open(glyph_log, "a", encoding="utf-8") as f:
    for m in manifests:
        f.write(json.dumps(m, ensure_ascii=False) + "\n")

print("Saved:", csv_path)
print("Chart:", png_path)
print("Consequence log:", log_path)
print("Manifest glyphs:", glyph_log)
```

> **Tip:** Schedule a daily reminder (e.g., 9:30 AM ET) to run the sweep and confirm the moves. The logs will help you track ΔLSSE and collapse alerts from one day to the next.
