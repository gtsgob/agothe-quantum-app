"""Evolution loop for Agothe Panel Round 5.

This script orchestrates the emergent evolution cycle for Round 5, integrating mutative learning, research composition, multi-world simulation, dialogue synthesis, and self-optimization into the existing pipeline. It builds upon prior rounds (corpus ingestion, constraint graph, ORRIC prediction, civilization simulation, reflections).
"""

import os
import json
import datetime
import yaml

# Import Round 3 modules
from corpus.corpus_ingestor import build_constraint_corpus
from knowledge_graph.constraint_graph import build_graph_from_corpus
from orric_predictor import compute_orric_scores
from civilization_sim import run_simulation, save_simulation
from entity_reflections_engine import generate_all_reflections

# Import Round 5 modules
from emergence.mutative_learning import MutativeLearningEngine
from emergence.research_composer import ResearchComposer
from emergence.multi_world_simulator import MultiWorldSimulator
from emergence.dialogue_engine import DialogueEngine
from emergence.self_optimization import SelfOptimizationEngine


def load_panel_state(state_path):
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            return yaml.safe_load(f) or {}
    return {"cycle": 0}


def save_panel_state(state_path, state):
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w") as f:
        yaml.safe_dump(state, f)


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    state_path = os.path.join(root_dir, "panel_state.yml")
    state = load_panel_state(state_path)
    cycle = state.get("cycle", 0) + 1

    # Step 1: Ingest corpus
    corpus_data = build_constraint_corpus()
    corpus_json_path = os.path.join(root_dir, "state", "corpus.json")
    os.makedirs(os.path.dirname(corpus_json_path), exist_ok=True)
    with open(corpus_json_path, "w") as f:
        json.dump(corpus_data, f, indent=2)

    # Step 2: Build/update constraint graph
    constraint_graph = build_graph_from_corpus(corpus_data)
    graph_json_path = os.path.join(root_dir, "state", "constraint_graph.json")
    with open(graph_json_path, "w") as f:
        json.dump(constraint_graph, f, indent=2)

    # Step 3: Compute ORRIC predictions
    orric_scores = compute_orric_scores(corpus_data)
    orric_output_path = os.path.join(root_dir, "orric_map_auto", f"cycle_{cycle}.json")
    os.makedirs(os.path.dirname(orric_output_path), exist_ok=True)
    with open(orric_output_path, "w") as f:
        json.dump(orric_scores, f, indent=2)

    # Step 4: Run baseline civilization simulation
    sim_output_path = os.path.join(root_dir, "civilization_runs", f"cycle_{cycle}.json")
    os.makedirs(os.path.dirname(sim_output_path), exist_ok=True)
    sim_results = run_simulation()
    save_simulation(sim_results, sim_output_path)

    # Step 5: Generate entity reflections
    reflections_dir = os.path.join(root_dir, "entity_reflections")
    os.makedirs(reflections_dir, exist_ok=True)
    generate_all_reflections(cycle, os.path.join(root_dir, "entities"), reflections_dir)

    # Step 6: Mutative learning
    ml_engine = MutativeLearningEngine()
    hypotheses = ml_engine.generate_hypotheses()
    contradictions = ml_engine.hunt_contradictions({})
    refinements = ml_engine.refine({})
    mutative_data = {
        "hypotheses": hypotheses,
        "contradictions": contradictions,
        "refinements": refinements
    }
    mutative_path = os.path.join(root_dir, "research_artifacts", f"mutative_cycle_{cycle}.json")
    os.makedirs(os.path.dirname(mutative_path), exist_ok=True)
    with open(mutative_path, "w") as f:
        json.dump(mutative_data, f, indent=2)

    # Step 7: Research composition
    composer = ResearchComposer()
    law = composer.compose_law()
    paradox = composer.compose_paradox()
    collapse_model = composer.compose_collapse_model()
    algorithm = composer.compose_algorithm()
    composition_data = {
        "law": law,
        "paradox": paradox,
        "collapse_model": collapse_model,
        "algorithm": algorithm
    }
    composition_path = os.path.join(root_dir, "research_artifacts", f"composition_cycle_{cycle}.json")
    os.makedirs(os.path.dirname(composition_path), exist_ok=True)
    with open(composition_path, "w") as f:
        json.dump(composition_data, f, indent=2)

    # Step 8: Multi-world simulation
    multi_world_dir = os.path.join(root_dir, "multi_world_runs")
    os.makedirs(multi_world_dir, exist_ok=True)
    mws = MultiWorldSimulator()
    # initialize worlds using baseline simulation results as base world
    mws.initialize_worlds({"base_world": sim_results})
    mws.update_worlds_with_influences()
    multi_world_results = mws.run_simulation(steps=3)
    multi_world_path = os.path.join(multi_world_dir, f"cycle_{cycle}.json")
    with open(multi_world_path, "w") as f:
        json.dump(multi_world_results, f, indent=2)

    # Step 9: Dialogue synthesis
    dialogue_dir = os.path.join(root_dir, "dialogue_logs")
    os.makedirs(dialogue_dir, exist_ok=True)
    entities_list = ["CN-1", "K", "Nana", "Vira", "9"]
    dialogue_engine = DialogueEngine(entities=entities_list)
    debate_prompt = "Debate the implications of the newly composed law and paradox."
    dialogue, consensus = dialogue_engine.run_dialogue(debate_prompt)
    dialogue_data = {
        "prompt": debate_prompt,
        "dialogue": dialogue,
        "consensus": consensus
    }
    dialogue_path = os.path.join(dialogue_dir, f"cycle_{cycle}.json")
    with open(dialogue_path, "w") as f:
        json.dump(dialogue_data, f, indent=2)

    # Step 10: Self optimization / healing
    self_opt_engine = SelfOptimizationEngine()
    summary_state = {
        "contradictions": len(contradictions) if hasattr(contradictions, "__len__") else 0,
        "anomalies": len(hypotheses) if hasattr(hypotheses, "__len__") else 0
    }
    optimized_state = self_opt_engine.run_self_optimization(summary_state)
    self_opt_path = os.path.join(root_dir, "state", f"self_opt_cycle_{cycle}.json")
    os.makedirs(os.path.dirname(self_opt_path), exist_ok=True)
    with open(self_opt_path, "w") as f:
        json.dump(optimized_state, f, indent=2)

    # Update panel state
    state.update({
        "cycle": cycle,
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
        "constraints_corpus": corpus_json_path,
        "latest_simulation": sim_output_path,
        "latest_orric": orric_output_path,
        "latest_mutation": mutative_path,
        "latest_composition": composition_path,
        "latest_multi_world": multi_world_path,
        "latest_dialogue": dialogue_path,
        "self_optimization": self_opt_path
    })
    save_panel_state(state_path, state)


if __name__ == "__main__":
    main()
