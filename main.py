#!/usr/bin/env python3
"""Command line interface for the Agothe quantum application."""

from __future__ import annotations

import argparse
import os
import subprocess

import numpy as np

from agothe_app import QuantumEnvironment, create_environment
from agothe_app.core.darwin_evolution_protocol import DarwinEvolutionProtocol


def create_sample_environment(agent_count: int = 4) -> QuantumEnvironment:
    return create_environment(agent_count)


def demo_quantum_consciousness(agent_count: int = 4) -> None:
    env = create_sample_environment(agent_count)
    print("🧠 Agothe Quantum Consciousness Framework Demo")
    print("=" * 60)
    print(f"✅ Environment bootstrapped with {len(env.agents)} agents")

    # Memory entanglement demo
    print("\n🔗 Quantum Memory Entanglement")
    try:
        result = env.entangle_agents(0, 1, "baseline")
        if result.get("success"):
            print("Entangled state:", result["entangled_state"])
        else:
            print("Entanglement failed:", result["error"])
    except Exception as exc:  # pragma: no cover - defensive logging
        print("Entanglement error:", exc)

    # Quantum learning demo
    print("\n🧠 Quantum Learning")
    learning_result = env.trigger_learning(0, reward=0.5)
    if learning_result.get("success"):
        print("Before:", learning_result["before"])
        print("After:", learning_result["after"])
    else:
        print("Learning failed:", learning_result.get("error"))

    # Reality collapse demo
    print("\n🌀 Reality Collapse")
    collapse = env.simulate_collapse(intent_phase=np.pi / 4)
    print("Collapse result:", collapse)

    # Evolution protocol demo
    print("\n🧬 Evolution Protocol")
    protocol = DarwinEvolutionProtocol()
    population = protocol.spawn_population(agent_count)
    best_agent = protocol.recursive_consciousness_evolution(population, depth=2)
    print("Best evolved agent:", best_agent)

    print("\n✨ Demo complete! Quantum consciousness is operational.")


def run_streamlit_app() -> None:
    app_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
    subprocess.run(["streamlit", "run", app_path], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Agothe Quantum Consciousness Framework")
    parser.add_argument("--demo", action="store_true", help="Run consciousness demo")
    parser.add_argument("--web", action="store_true", help="Launch the Streamlit interface")
    parser.add_argument("--agents", type=int, default=4, help="Number of agents to create")

    args = parser.parse_args()

    if args.demo:
        demo_quantum_consciousness(args.agents)
    elif args.web:
        run_streamlit_app()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
