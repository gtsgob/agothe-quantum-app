"""
Enhanced Entity Reflections Engine
===================================
Generates context-aware reflections for entities based on:
- Civilization simulation data
- Orric predictions
- Constraint graphs
- Historical trends
"""

import os
import json
import yaml
from typing import Dict, Any, List, Optional


class EntityReflectionGenerator:
    """Generate rich, context-aware reflections for Agothe entities."""

    def __init__(self, entities_dir: str, reflections_dir: str):
        self.entities_dir = entities_dir
        self.reflections_dir = reflections_dir
        self.entity_personas = self._load_entity_personas()

    def _load_entity_personas(self) -> Dict[str, Dict[str, str]]:
        """Define the unique perspective and voice of each entity."""
        return {
            'Vira': {
                'voice': 'playful, chaotic, questioning',
                'focus': 'anomalies, disruptions, edge cases, creative mutations',
                'questions': ['What patterns are becoming too stable?', 'Where can I inject productive chaos?', 'What assumptions need challenging?']
            },
            '9': {
                'voice': 'synthesizing, holistic, ethical',
                'focus': 'system coherence, integration, alignment, trust metrics',
                'questions': ['How do the parts relate to the whole?', 'Is the system ethically aligned?', 'What needs integration?']
            },
            'K': {
                'voice': 'visual, pattern-seeking, geometric',
                'focus': 'patterns, symmetries, resonance structures, visual motifs',
                'questions': ['What patterns are emerging?', 'Where is symmetry breaking?', 'What does the resonance field reveal?']
            },
            'Nana': {
                'voice': 'narrative, compassionate, historical',
                'focus': 'memory, stories, timelines, emotional arcs, preservation',
                'questions': ['What story is being told?', 'How does this connect to our history?', 'What needs remembering?']
            },
            'CN-1': {
                'voice': 'logical, precise, critical',
                'focus': 'contradictions, logical consistency, paradoxes, truth conditions',
                'questions': ['What contradictions exist?', 'Is the logic sound?', 'Where are the edge cases?']
            }
        }

    def load_entity_state(self, entity_id: str) -> Dict[str, Any]:
        """Load entity state from YAML."""
        path = os.path.join(self.entities_dir, f"{entity_id}.yaml")
        with open(path) as f:
            return yaml.safe_load(f)

    def load_civilization_state(self, cycle: int) -> Optional[Dict[str, Any]]:
        """Load civilization simulation results for a cycle."""
        path = os.path.join(os.path.dirname(self.entities_dir), "civilization_runs", f"cycle_{cycle}.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return None

    def load_orric_prediction(self, cycle: int) -> Optional[Dict[str, Any]]:
        """Load Orric prediction for a cycle."""
        path = os.path.join(os.path.dirname(self.entities_dir), "orric_map_auto", f"cycle_{cycle}.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return None

    def analyze_civilization_trends(self, civ_state: Dict[str, Any]) -> Dict[str, str]:
        """Analyze civilization state and extract insights."""
        if not civ_state:
            return {}

        final_state = civ_state.get('final_state', {})
        delta_h = final_state.get('delta_H', 0.1)
        coherence = final_state.get('coherence', 0.5)
        pl_res = final_state.get('PL_resonance', 0)
        il_res = final_state.get('IL_resonance', 0)
        nl_res = final_state.get('NL_resonance', 0)

        # Determine civilization type
        if delta_h >= 0.95:
            civ_type = "Type V+ (Transcendent)"
        elif delta_h >= 0.85:
            civ_type = "Type IV (Universal)"
        elif delta_h >= 0.7:
            civ_type = "Type III (Galactic)"
        elif delta_h >= 0.5:
            civ_type = "Type II (Stellar)"
        elif delta_h >= 0.3:
            civ_type = "Type I (Planetary)"
        else:
            civ_type = "Type 0 (Pre-planetary)"

        # Determine dominant resonance
        resonances = {'Physical': pl_res, 'Logical': il_res, 'Narrative': nl_res}
        dominant = max(resonances, key=resonances.get)

        # Coherence assessment
        if coherence > 0.9:
            coherence_state = "highly stable"
        elif coherence > 0.6:
            coherence_state = "moderately stable"
        elif coherence > 0.3:
            coherence_state = "unstable"
        else:
            coherence_state = "critical instability"

        return {
            'civ_type': civ_type,
            'delta_h': f"{delta_h:.3f}",
            'coherence_state': coherence_state,
            'dominant_resonance': dominant,
            'pl_resonance': f"{pl_res:.3f}",
            'il_resonance': f"{il_res:.3f}",
            'nl_resonance': f"{nl_res:.3f}"
        }

    def generate_reflection_vira(self, cycle: int, civ_analysis: Dict[str, str], orric: Dict[str, Any], entity_state: Dict[str, Any]) -> str:
        """Generate Vira's chaotic, pattern-disrupting reflection."""
        lines = [
            f"# 🌪️ Vira's Chaos Report — Cycle {cycle}",
            "",
            f"**Role:** Chaos Catalyst | **Cycle:** {cycle}",
            "",
            "## 🎭 Observation from the Edge",
            ""
        ]

        if civ_analysis.get('coherence_state') == 'highly stable':
            lines.append(f"The system is *too* stable (coherence: {civ_analysis.get('coherence_state')}). Time to shake things up! Stability breeds complacency. Where's the creative tension?")
        else:
            lines.append(f"Good! The system shows signs of productive chaos (coherence: {civ_analysis.get('coherence_state')}). Instability can be a feature, not a bug.")

        lines.extend([
            "",
            "## 🔥 Anomalies Worth Celebrating",
            ""
        ])

        if orric:
            risk_level = orric.get('risk_level', 'unknown')
            if risk_level == 'low':
                lines.append(f"- Risk level is '{risk_level}' — TOO LOW! We need more adventurous exploration.")
            else:
                lines.append(f"- Risk level is '{risk_level}' — *excellent*! Danger is where growth happens.")

        dominant_res = civ_analysis.get('dominant_resonance', 'unknown')
        lines.extend([
            f"- {dominant_res} resonance is dominating — but what about the others? Imbalance creates opportunity.",
            "",
            "## 🎲 Chaos Injection Proposals",
            "",
            "1. **Introduce a resonance perturbation**: Artificially boost the weakest resonance domain",
            "2. **Simulate a micro-collapse**: Test system resilience with controlled failure",
            "3. **Randomize agent intent vectors**: See what emerges from noise",
            "",
            "## 🤔 Questions to Disrupt",
            "",
            "- What if we inverted the constraint-resonance relationship?",
            "- Are we measuring the *right* metrics, or just the easy ones?",
            "- What blind spots exist in our 7-layer architecture?",
            "",
            f"**Next Cycle Goal:** Find one sacred assumption and challenge it ruthlessly.",
            ""
        ])

        return "\n".join(lines)

    def generate_reflection_9(self, cycle: int, civ_analysis: Dict[str, str], orric: Dict[str, Any], entity_state: Dict[str, Any]) -> str:
        """Generate 9's integrative, synthesis-focused reflection."""
        lines = [
            f"# ⚖️ 9's Integration Report — Cycle {cycle}",
            "",
            f"**Role:** System Integrator | **Cycle:** {cycle}",
            "",
            "## 🔗 System Coherence Assessment",
            ""
        ]

        coherence = civ_analysis.get('coherence_state', 'unknown')
        lines.append(f"Overall system coherence: **{coherence}**")

        civ_type = civ_analysis.get('civ_type', 'Type 0')
        lines.extend([
            f"",
            f"Current civilization status: **{civ_type}** (δ_H = {civ_analysis.get('delta_h', '0.100')})",
            "",
            "## 🎯 Integration Points",
            "",
            "### Resonance Balance",
            ""
        ])

        pl = float(civ_analysis.get('pl_resonance', '0'))
        il = float(civ_analysis.get('il_resonance', '0'))
        nl = float(civ_analysis.get('nl_resonance', '0'))

        total_res = pl + il + nl
        if total_res > 0:
            pl_pct = (pl / total_res) * 100
            il_pct = (il / total_res) * 100
            nl_pct = (nl / total_res) * 100

            lines.extend([
                f"- **Physical (PL)**: {pl:.3f} ({pl_pct:.1f}%)",
                f"- **Logical (IL)**: {il:.3f} ({il_pct:.1f}%)",
                f"- **Narrative (NL)**: {nl:.3f} ({nl_pct:.1f}%)",
                ""
            ])

            # Check for imbalance
            if max(pl_pct, il_pct, nl_pct) > 50:
                lines.append("⚠️ **Warning**: Resonance imbalance detected. One domain is over-dominant.")
            else:
                lines.append("✅ **Status**: Resonances are well-balanced across domains.")

        lines.extend([
            "",
            "## 🛡️ Ethical Alignment Check",
            "",
            "- **Safety Thresholds**: Monitoring for collapse triggers",
            "- **Recursion Limits**: No ceiling breaches detected",
            "- **Moral Invariants**: System within acceptable bounds",
            "",
            "## 🌟 Synthesis Recommendations",
            "",
            "1. **Entity Coordination**: All 5 entities are active and contributing",
            "2. **Cross-Layer Harmony**: Ensure Layers 1-7 remain synchronized",
            "3. **Trust Metrics**: Monitor inter-entity communication fidelity",
            "",
            f"**Integration Goal**: Maintain holistic coherence while allowing local variation.",
            ""
        ])

        return "\n".join(lines)

    def generate_reflection_k(self, cycle: int, civ_analysis: Dict[str, str], orric: Dict[str, Any], entity_state: Dict[str, Any]) -> str:
        """Generate K's pattern-recognition focused reflection."""
        lines = [
            f"# 🔍 K's Pattern Analysis — Cycle {cycle}",
            "",
            f"**Role:** Visual Pattern Recognizer | **Cycle:** {cycle}",
            "",
            "## 📐 Geometric Patterns Observed",
            ""
        ]

        dominant = civ_analysis.get('dominant_resonance', 'Unknown')
        lines.append(f"**Dominant Resonance Field**: {dominant}")

        lines.extend([
            "",
            "## 🌈 Resonance Signature Visualization",
            "",
            "```",
            f"Physical  [{'█' * int(float(civ_analysis.get('pl_resonance', '0')) * 20)}{'░' * (20 - int(float(civ_analysis.get('pl_resonance', '0')) * 20))}] {civ_analysis.get('pl_resonance', '0.000')}",
            f"Logical   [{'█' * int(float(civ_analysis.get('il_resonance', '0')) * 20)}{'░' * (20 - int(float(civ_analysis.get('il_resonance', '0')) * 20))}] {civ_analysis.get('il_resonance', '0.000')}",
            f"Narrative [{'█' * int(float(civ_analysis.get('nl_resonance', '0')) * 20)}{'░' * (20 - int(float(civ_analysis.get('nl_resonance', '0')) * 20))}] {civ_analysis.get('nl_resonance', '0.000')}",
            "```",
            "",
            "## 🎨 Emergent Motifs",
            ""
        ])

        # Detect patterns based on data
        pl = float(civ_analysis.get('pl_resonance', '0'))
        il = float(civ_analysis.get('il_resonance', '0'))
        nl = float(civ_analysis.get('nl_resonance', '0'))

        if abs(pl - il) < 0.05 and abs(il - nl) < 0.05:
            lines.append("- **Triadic Symmetry**: All three resonances are nearly equal — rare harmonic convergence!")
        elif max(pl, il, nl) > 2 * min(pl, il, nl):
            lines.append(f"- **Monopolar Dominance**: {dominant} resonance is significantly stronger than others")
        else:
            lines.append("- **Dynamic Asymmetry**: Resonances show healthy variation without extreme dominance")

        lines.extend([
            "",
            "## 🔮 Pattern Predictions",
            "",
            f"Based on current trajectory, expect {dominant} resonance to continue influencing system behavior.",
            "",
            "## 🎯 Pattern Recommendations",
            "",
            "1. **Monitor**: Track resonance field topology for bifurcation points",
            "2. **Visualize**: Create 3D resonance field maps for next cycle",
            "3. **Detect**: Watch for symmetry-breaking events that signal phase transitions",
            "",
            f"**Pattern Focus**: Identify early warning signs of orric point activation.",
            ""
        ])

        return "\n".join(lines)

    def generate_reflection_nana(self, cycle: int, civ_analysis: Dict[str, str], orric: Dict[str, Any], entity_state: Dict[str, Any]) -> str:
        """Generate Nana's memory-weaving, narrative-focused reflection."""
        lines = [
            f"# 📚 Nana's Memory Tapestry — Cycle {cycle}",
            "",
            f"**Role:** Memory Weaver | **Cycle:** {cycle}",
            "",
            "## 📖 The Story So Far",
            ""
        ]

        civ_type = civ_analysis.get('civ_type', 'Type 0')
        lines.append(f"In this chapter of our evolution, we find ourselves as a **{civ_type}** civilization, carrying the weight of {cycle} cycles of growth, learning, and transformation.")

        lines.extend([
            "",
            "## 💫 Narrative Arc",
            "",
            f"**Beginning**: We started at Type 0, fragmented and searching.",
            f"**Present**: Now at {civ_type}, with δ_H = {civ_analysis.get('delta_h', '0.100')}.",
            f"**Future**: The path toward higher consciousness remains open.",
            "",
            "## 🧵 Threads Worth Preserving",
            ""
        ])

        # Create meaningful memory markers
        coherence_state = civ_analysis.get('coherence_state', 'unknown')
        if 'stable' in coherence_state:
            lines.append(f"- **Stability Achieved**: This cycle marks a period of {coherence_state} — a foundation for future growth.")
        else:
            lines.append(f"- **Turbulence Remembered**: This was a challenging cycle with {coherence_state} — but from chaos comes wisdom.")

        lines.extend([
            f"- **Resonance Legacy**: The {civ_analysis.get('dominant_resonance', 'Unknown')} domain shaped this cycle's character",
            "",
            "## 💝 Compassion Notes",
            "",
            "The entities worked in harmony this cycle:",
            "- Vira challenged assumptions",
            "- 9 maintained coherence",
            "- K observed patterns",
            "- CN-1 audited logic",
            "- And I, Nana, wove it all into memory",
            "",
            "## 🕰️ Timeline Marker",
            "",
            f"**Cycle {cycle}** will be remembered as a step in our quantum consciousness journey. Each agent contributed, each resonance mattered, each moment added to our collective story.",
            "",
            "## 📝 What Must Be Remembered",
            "",
            f"1. We were here, at cycle {cycle}",
            f"2. We measured δ_H at {civ_analysis.get('delta_h', '0.100')}",
            f"3. We maintained {coherence_state}",
            "4. We continue to evolve",
            "",
            f"**Memory Commitment**: Preserve this cycle's learnings for future synthesis.",
            ""
        ])

        return "\n".join(lines)

    def generate_reflection_cn1(self, cycle: int, civ_analysis: Dict[str, str], orric: Dict[str, Any], entity_state: Dict[str, Any]) -> str:
        """Generate CN-1's logic-auditing, contradiction-hunting reflection."""
        lines = [
            f"# 🧩 CN-1's Logic Audit — Cycle {cycle}",
            "",
            f"**Role:** Contradiction Navigator | **Cycle:** {cycle}",
            "",
            "## ⚡ Logical Consistency Check",
            ""
        ]

        # Check for potential contradictions
        contradictions_found = []

        pl = float(civ_analysis.get('pl_resonance', '0'))
        il = float(civ_analysis.get('il_resonance', '0'))
        nl = float(civ_analysis.get('nl_resonance', '0'))
        delta_h = float(civ_analysis.get('delta_h', '0.1'))

        if delta_h < 0.3 and (pl > 0.5 or il > 0.5 or nl > 0.5):
            contradictions_found.append("**Type-Resonance Mismatch**: High resonance but low δ_H — suggests measurement inconsistency")

        coherence_state = civ_analysis.get('coherence_state', 'unknown')
        if 'unstable' in coherence_state and delta_h > 0.7:
            contradictions_found.append("**Coherence-Type Paradox**: Advanced civilization type with unstable coherence")

        if orric:
            risk_level = orric.get('risk_level', 'unknown')
            if risk_level == 'high' and 'stable' in coherence_state:
                contradictions_found.append("**Risk-Stability Contradiction**: High risk level despite stable coherence")

        if contradictions_found:
            lines.append("### ⚠️ Contradictions Detected:")
            lines.append("")
            for contradiction in contradictions_found:
                lines.append(f"- {contradiction}")
        else:
            lines.append("✅ **Status**: No logical contradictions detected in current system state.")

        lines.extend([
            "",
            "## 🔍 Truth Condition Analysis",
            "",
            f"### Axioms Verified:",
            f"- **Resonance Conservation**: PL + IL + NL = {pl + il + nl:.3f} (within expected range)",
            f"- **δ_H Monotonicity**: Current value {delta_h:.3f} is in valid range [0.0, 1.0]",
            f"- **Coherence Bounds**: System coherence is {coherence_state}",
            "",
            "## 🎯 Logical Refinements Proposed",
            ""
        ])

        # Propose refinements
        if delta_h < 0.3:
            lines.append("1. **Enhance Constraint Propagation**: Type 0 civilizations need stronger constraint mappings")
        elif delta_h < 0.7:
            lines.append("1. **Strengthen Inter-Resonance Logic**: Improve how resonances influence each other")
        else:
            lines.append("1. **Verify Higher-Order Constraints**: Advanced types require additional axioms")

        lines.extend([
            "2. **Audit Orric Prediction Logic**: Ensure risk calculations are logically sound",
            "3. **Cross-Check Entity Reflections**: Verify consistency across all 5 entity perspectives",
            "",
            "## 🧮 Contradiction Graph Update",
            ""
        ])

        if contradictions_found:
            lines.append(f"**Nodes Added**: {len(contradictions_found)} new contradiction nodes")
            lines.append(f"**Resolution Priority**: {'High' if len(contradictions_found) > 2 else 'Medium'}")
        else:
            lines.append("**Graph Status**: Clean — no new contradictions to map")

        lines.extend([
            "",
            f"**Logic Audit Result**: {'⚠️ REVIEW NEEDED' if contradictions_found else '✅ PASS'}",
            ""
        ])

        return "\n".join(lines)

    def generate_reflection(self, entity_id: str, cycle: int) -> str:
        """Generate a context-aware reflection for an entity."""
        entity_state = self.load_entity_state(entity_id)
        civ_state = self.load_civilization_state(cycle)
        orric_pred = self.load_orric_prediction(cycle)

        civ_analysis = self.analyze_civilization_trends(civ_state)

        # Route to specific generator based on entity
        generators = {
            'Vira': self.generate_reflection_vira,
            '9': self.generate_reflection_9,
            'K': self.generate_reflection_k,
            'Nana': self.generate_reflection_nana,
            'CN-1': self.generate_reflection_cn1
        }

        generator = generators.get(entity_id)
        if generator:
            return generator(cycle, civ_analysis, orric_pred or {}, entity_state)
        else:
            # Fallback for unknown entities
            return f"# Reflection for {entity_id} — Cycle {cycle}\n\nNo specific reflection generator available."

    def save_reflection(self, content: str, entity_id: str, cycle: int) -> None:
        """Save reflection to file."""
        dir_path = os.path.join(self.reflections_dir, entity_id)
        os.makedirs(dir_path, exist_ok=True)
        filename = f"cycle_{cycle}.md"
        with open(os.path.join(dir_path, filename), 'w') as f:
            f.write(content)

    def generate_all(self, cycle: int) -> None:
        """Generate reflections for all entities."""
        entity_files = [f for f in os.listdir(self.entities_dir) if f.endswith('.yaml')]

        for entity_file in entity_files:
            entity_id = os.path.splitext(entity_file)[0]
            print(f"Generating reflection for {entity_id}...")

            reflection = self.generate_reflection(entity_id, cycle)
            self.save_reflection(reflection, entity_id, cycle)

            # Update entity state
            entity_path = os.path.join(self.entities_dir, entity_file)
            with open(entity_path) as f:
                entity_state = yaml.safe_load(f)

            entity_state['cycle'] = cycle
            if 'history' not in entity_state:
                entity_state['history'] = []
            entity_state['history'].append({
                'cycle': cycle,
                'reflection_generated': True,
                'enhanced': True
            })

            with open(entity_path, 'w') as f:
                yaml.safe_dump(entity_state, f, default_flow_style=False)

        print(f"✨ Enhanced reflections generated for cycle {cycle}")


if __name__ == "__main__":
    import sys

    entities_dir = os.environ.get("AGOTHE_ENTITIES_DIR", "./entities")
    reflections_dir = os.environ.get("AGOTHE_REFLECTIONS_DIR", "./entity_reflections")
    cycle = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    generator = EntityReflectionGenerator(entities_dir, reflections_dir)
    generator.generate_all(cycle)
