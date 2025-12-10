"""
entity_reflections_engine.py

This module generates per-entity reflection logs for each evolution cycle.
Given the current state of each entity (loaded from YAML) and optionally the latest corpus or simulation results,
it synthesizes a reflection with fields: observation, hypothesis, predicted contradiction, next_step.

The reflections are saved as markdown files in the entity_reflections/<entity>/<cycle>.md directory.

This skeleton uses random placeholders and simple heuristics; it can be extended to incorporate metrics and analyses.
"""

import os
import yaml
import random
from typing import Dict, Any


def load_entity_state(path: str) -> Dict[str, Any]:
    """Load a YAML file representing an entity's state."""
    with open(path) as f:
        return yaml.safe_load(f)


def generate_reflection(entity_state: Dict[str, Any], cycle: int) -> str:
    """Generate a reflection string for an entity."""
    name = entity_state.get('name', 'Unknown entity')
    observation = f"{name} notes that cycle {cycle} continues the pattern of growth."
    hypothesis = "A new pattern may emerge if constraints shift."
    contradiction = (
        "No contradictions detected."
        if random.random() > 0.3
        else "Potential misalignment in constraint mapping."
    )
    next_step = "Proceed with next cycle and monitor changes."
    lines = [
        f"# Reflection for {name} — Cycle {cycle}",
        "",
        f"**Observation:** {observation}",
        f"**Hypothesis:** {hypothesis}",
        f"**Predicted Contradiction:** {contradiction}",
        f"**Next Step Proposal:** {next_step}",
        "",
    ]
    return "\n".join(lines)


def save_reflection(content: str, entity_id: str, cycle: int, base_dir: str = "./entity_reflections") -> None:
    """Save the reflection content to a markdown file in the appropriate directory."""
    dir_path = os.path.join(base_dir, entity_id)
    os.makedirs(dir_path, exist_ok=True)
    filename = f"cycle_{cycle}.md"
    with open(os.path.join(dir_path, filename), 'w') as f:
        f.write(content)


def process_all_entities(entities_dir: str, cycle: int) -> None:
    """Generate and save reflections for all entity YAML files in a directory."""
    for filename in os.listdir(entities_dir):
        if not filename.endswith(".yaml"):
            continue
        entity_id = os.path.splitext(filename)[0]
        state_path = os.path.join(entities_dir, filename)
        try:
            state = load_entity_state(state_path)
        except Exception:
            state = {}
        reflection = generate_reflection(state, cycle)
        save_reflection(reflection, entity_id, cycle)


def generate_all_reflections(entities_dir: str, reflections_dir: str, cycle: int) -> None:
    """
    Generate and save reflections for all entities, updating their state files with cycle increments.

    Args:
        entities_dir: Directory containing entity YAML files.
        reflections_dir: Directory where reflections should be saved.
        cycle: Current evolution cycle number.
    """
    for filename in os.listdir(entities_dir):
        if not filename.endswith(".yaml"):
            continue
        entity_id = os.path.splitext(filename)[0]
        state_path = os.path.join(entities_dir, filename)

        try:
            state = load_entity_state(state_path)
        except Exception:
            state = {'id': entity_id, 'name': entity_id, 'cycle': 0, 'history': [], 'data': {}}

        # Generate reflection
        reflection = generate_reflection(state, cycle)

        # Save reflection to reflections directory
        save_reflection(reflection, entity_id, cycle, base_dir=reflections_dir)

        # Update entity state with new cycle count and history
        state['cycle'] = cycle
        if 'history' not in state:
            state['history'] = []
        state['history'].append({
            'cycle': cycle,
            'reflection_generated': True
        })

        # Save updated entity state
        with open(state_path, 'w') as f:
            yaml.safe_dump(state, f, default_flow_style=False)


if __name__ == "__main__":
    cycle_str = os.environ.get("AGOTHE_CYCLE_NUMBER", "0")
    try:
        cycle = int(cycle_str)
    except ValueError:
        cycle = 0
    entities_dir = os.environ.get("AGOTHE_ENTITIES_DIR", "./agothe_panel/entities")
    process_all_entities(entities_dir, cycle)
    print(f"Generated reflections for cycle {cycle}")
