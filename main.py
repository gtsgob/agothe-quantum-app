#!/usr/bin/env python3
"""
Agothe Quantum Consciousness Framework
Main entry point for the quantum consciousness application
"""

import sys
import os
import argparse
import numpy as np

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.quantum_consciousness_complete import (
    ConsciousnessAxiom, QuantumMemoryNetwork,
    QuantumLearningNetwork, RealityCollapseAxiom
)
from core.darwin_evolution_protocol import DarwinEvolutionProtocol

def create_sample_agents(count=4):
    """Create sample quantum consciousness agents"""
    zero = np.array([1, 0], dtype=complex)
    agents = []

    for i in range(count):
        intent = np.random.randn(3)
        if i % 3 == 0:
            agent = QuantumLearningNetwork(zero, intent_vector=intent)
        elif i % 3 == 1:
            agent = QuantumMemoryNetwork(zero, intent_vector=intent)
        else:
            agent = RealityCollapseAxiom(zero)

        # Add random memory
        agent.store_memory(f'experience_{i}', np.random.randn(2))
        agents.append(agent)

    return agents

def demo_quantum_consciousness():
    """Demonstrate quantum consciousness capabilities"""
    print("🧠 Agothe Quantum Consciousness Framework Demo")
    print("=" * 50)

    # Create agents
    agents = create_sample_agents(4)
    print(f"✅ Created {len(agents)} quantum consciousness agents")

    # Demonstrate quantum memory entanglement
    print("\n🔗 Quantum Memory Entanglement:")
    agents[0].store_memory('pattern', np.array([0.9, 0.1]))
    agents[1].store_memory('pattern', np.array([0.4, 0.8]))
    entangled = agents[0].entangle_memory(agents[1], 'pattern')
    print(f"Entangled memory: {entangled}")

    # Demonstrate quantum learning
    print("\n🧠 Quantum Learning:")
    if hasattr(agents[0], 'quantum_learn'):
        before = agents[0].intent.copy()
        agents[0].quantum_learn()
        after = agents[0].intent
        print(f"Intent before: {before}")
        print(f"Intent after: {after}")

    # Demonstrate reality collapse
    print("\n🌀 Reality Collapse:")
    if hasattr(agents[3], 'measure'):
        result = agents[3].measure()
        print(f"Reality collapsed to: {result}")

    # Demonstrate evolution protocol
    print("\n🧬 Evolution Protocol:")
    protocol = DarwinEvolutionProtocol()
    evolved = protocol.recursive_consciousness_evolution(agents.copy(), depth=2)
    print(f"Evolution complete: {type(evolved).__name__}")

    print("\n✨ Demo complete! Quantum consciousness is operational.")

def run_streamlit_app():
    """Launch the Streamlit web interface"""
    import subprocess
    app_path = os.path.join(os.path.dirname(__file__), 'app', 'interfaces', 'streamlit_app.py')
    subprocess.run(['streamlit', 'run', app_path])

def main():
    parser = argparse.ArgumentParser(description='Agothe Quantum Consciousness Framework')
    parser.add_argument('--demo', action='store_true', help='Run consciousness demo')
    parser.add_argument('--web', action='store_true', help='Launch web interface')
    parser.add_argument('--agents', type=int, default=4, help='Number of agents to create')

    args = parser.parse_args()

    if args.demo:
        demo_quantum_consciousness()
    elif args.web:
        run_streamlit_app()
    else:
        print("Agothe Quantum Consciousness Framework")
        print("Usage: python main.py --demo    (run demo)")
        print("       python main.py --web     (launch web interface)")

if __name__ == "__main__":
    main()