import os
import json
import datetime
import yaml

# Import modules from Agothe Panel
from corpus.corpus_ingestor import build_constraint_corpus
from knowledge_graph.constraint_graph import build_graph_from_corpus
from orric_predictor import predict_orric_metrics, save_prediction
from civilization_sim import run_simulation, save_simulation
from entity_reflections_engine import generate_all_reflections

def load_panel_state(state_path):
    """Load panel state from YAML file if it exists."""
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            return yaml.safe_load(f)
    return {"cycle": 0}

def save_panel_state(state_path, state):
    """Save panel state back to YAML file."""
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w") as f:
        yaml.safe_dump(state, f)

def main():
    """
    Execute one evolution cycle:
    - Ingest corpus from project documents.
    - Build or update constraint graph.
    - Predict Orric metrics.
    - Run civilization simulation.
    - Generate reflections for each entity.
    - Update panel state metadata.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    state_path = os.path.join(root_dir, "panel_state.yaml")

    # Load previous state
    state = load_panel_state(state_path)
    cycle = state.get("cycle", 0) + 1

    # Step 1: ingest corpus from documents
    corpus_data = build_constraint_corpus()
    # Save corpus
    corpus_json_path = os.path.join(root_dir, "state", "corpus.json")
    os.makedirs(os.path.dirname(corpus_json_path), exist_ok=True)
    with open(corpus_json_path, "w") as f:
        json.dump(corpus_data, f, indent=2)

    # Step 2: build constraint graph
    graph = build_graph_from_corpus(corpus_data)
    graph_path = os.path.join(root_dir, "knowledge_graph", "constraint_graph.json")
    os.makedirs(os.path.dirname(graph_path), exist_ok=True)
    graph.save(graph_path)

    # Step 3: predict Orric tensions
    orric_output_path = os.path.join(root_dir, "orric_map_auto", f"cycle_{cycle}.json")
    os.makedirs(os.path.dirname(orric_output_path), exist_ok=True)
    constraints = []
    for entries in corpus_data.values():
        constraints.extend(entry.get("content", "") for entry in entries)

    orric_prediction = predict_orric_metrics(constraints)
    save_prediction(orric_prediction, orric_output_path)

    # Step 4: run civilization simulation
    sim_results = run_simulation(num_cycles=1)
    sim_output_path = os.path.join(root_dir, "civilization_runs", f"cycle_{cycle}.json")
    os.makedirs(os.path.dirname(sim_output_path), exist_ok=True)
    save_simulation(sim_results, sim_output_path)

    # Step 5: generate entity reflections
    entities_dir = os.path.join(root_dir, "entities")
    reflections_dir = os.path.join(root_dir, "entity_reflections")
    os.makedirs(reflections_dir, exist_ok=True)
    generate_all_reflections(entities_dir, reflections_dir, cycle)

    # Update panel state metadata
    state["cycle"] = cycle
    state["last_updated"] = datetime.datetime.utcnow().isoformat() + "Z"
    state["latest_corpus"] = os.path.relpath(corpus_json_path, root_dir)
    state["latest_graph"] = os.path.relpath(graph_path, root_dir)
    state["latest_orric"] = os.path.relpath(orric_output_path, root_dir)
    state["latest_simulation"] = os.path.relpath(sim_output_path, root_dir)

    save_panel_state(state_path, state)

if __name__ == "__main__":
    main()
