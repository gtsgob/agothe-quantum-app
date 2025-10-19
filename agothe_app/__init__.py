"""Agothe Quantum Consciousness package."""

from .core.quantum_consciousness import (
    ConsciousnessAxiom,
    QuantumLearningNetwork,
    QuantumMemoryNetwork,
    RealityCollapseAxiom,
    create_bloch_state,
)
from .services.quantum_environment import QuantumEnvironment, create_environment

__all__ = [
    "ConsciousnessAxiom",
    "QuantumLearningNetwork",
    "QuantumMemoryNetwork",
    "RealityCollapseAxiom",
    "create_bloch_state",
    "QuantumEnvironment",
    "create_environment",
]
