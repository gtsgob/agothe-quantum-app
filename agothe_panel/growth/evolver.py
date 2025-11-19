#!/usr/bin/env python3
"""
Agothe Panel growth evolver script.
Iterates through each entity YAML and updates their state based on growth rules defined in growth/ruleset.yaml.
This script is intentionally deterministic and does not invoke external APIs or autonomous loops.
"""

import yaml
import os
 
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTITIES_DIR = os.path.join(BASE_DIR, 'entities')
GROWTH_RULESET = os.path.join(BASE_DIR, 'growth', 'ruleset.yaml')
PANEL_STATE_FILE = os.path.join(BASE_DIR, 'panel_state.yaml')

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def save_yaml(data, path):
    with open(path, 'w') as f:
        yaml.dump(data, f)

def apply_rules(entity_data, rule):
    # Simplistic update: increment cycle and append history record
    entity_data['cycle'] = entity_data.get('cycle', 0) + 1
    history = entity_data.setdefault('history', [])
    history.append({
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'action': rule['action'],
        'description': rule['description']
    })
    return entity_data

def main():
    ruleset = load_yaml(GROWTH_RULESET)
    panel_state = {'updated_at': datetime.utcnow().isoformat() + 'Z', 'entities': {}}

    for rule in ruleset.get('rules', []):
        entity_id = rule['entity']
        # map entity id to filename (9 is numeric string)
        filename = f"{entity_id}.yaml" if entity_id != '9' else '9.yaml'
        entity_path = os.path.join(ENTITIES_DIR, filename)
        if not os.path.exists(entity_path):
            continue
        entity_data = load_yaml(entity_path)
        updated_data = apply_rules(entity_data, rule)
        save_yaml(updated_data, entity_path)
        panel_state['entities'][entity_id] = updated_data['cycle']

    save_yaml(panel_state, PANEL_STATE_FILE)

if __name__ == '__main__':
    main()
