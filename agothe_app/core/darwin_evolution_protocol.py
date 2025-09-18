"""Evolutionary routines for the Agothe quantum agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence

import numpy as np

from .quantum_consciousness import (
    ConsciousnessAxiom,
    QuantumLearningNetwork,
    QuantumMemoryNetwork,
    RealityCollapseAxiom,
    create_bloch_state,
)


@dataclass
class EvolutionEvent:
    """Structure describing one evolutionary step."""

    generation: int
    population_size: int
    mean_coherence: float
    best_fitness: float
    annotations: Dict[str, float] = field(default_factory=dict)


class DarwinEvolutionProtocol:
    """Simplified evolutionary protocol for quantum consciousness agents."""

    def __init__(self, selection_pressure: float = 0.65) -> None:
        self.selection_pressure = selection_pressure
        self.history: List[EvolutionEvent] = []

    # ------------------------------------------------------------------
    def evaluate_agent(self, agent: ConsciousnessAxiom) -> float:
        """Fitness is a blend of coherence and intent magnitude."""

        intent_norm = float(np.linalg.norm(agent.intent) + 1e-9)
        return 0.7 * agent.coherence() + 0.3 * np.tanh(intent_norm)

    def mutate_agent(
        self, agent: ConsciousnessAxiom, mutation_rate: float = 0.1
    ) -> ConsciousnessAxiom:
        """Return a mutated clone of ``agent``."""

        mutated_state = _jitter_state(agent.state, mutation_rate)
        mutated_intent = _jitter_vector(agent.intent, mutation_rate)
        clone = QuantumLearningNetwork(mutated_state, mutated_intent, label=agent.label)
        clone.memory = {k: v.copy() for k, v in agent.memory.items()}
        return clone

    def crossover_agents(
        self, agent_a: QuantumMemoryNetwork, agent_b: QuantumMemoryNetwork
    ) -> QuantumLearningNetwork:
        """Create offspring by mixing the intent vectors and states of parents."""

        alpha = np.random.rand()
        state = _normalize(alpha * agent_a.state + (1 - alpha) * agent_b.state)
        intent = _normalize(alpha * agent_a.intent + (1 - alpha) * agent_b.intent)
        offspring = QuantumLearningNetwork(state, intent, label="offspring")
        if agent_a.memory and agent_b.memory:
            key = np.random.choice(list(agent_a.memory.keys()))
            offspring.memory[key] = _normalize(
                alpha * agent_a.memory[key] + (1 - alpha) * agent_b.memory[key]
            )
        return offspring

    # ------------------------------------------------------------------
    def recursive_consciousness_evolution(
        self,
        population: Sequence[ConsciousnessAxiom],
        depth: int = 1,
        mutation_rate: float = 0.1,
    ) -> ConsciousnessAxiom:
        """Run ``depth`` rounds of simulated evolution and return the best agent."""

        agents = list(population)
        for generation in range(depth):
            fitness = np.array([self.evaluate_agent(agent) for agent in agents])
            order = np.argsort(fitness)[::-1]
            survivors = [agents[i] for i in order[: max(2, int(len(agents) * 0.6))]]
            # Re-populate via crossover and mutation
            children: List[ConsciousnessAxiom] = []
            while len(survivors) + len(children) < len(agents):
                idx_a, idx_b = np.random.choice(len(survivors), size=2, replace=True)
                parent_a = survivors[idx_a]
                parent_b = survivors[idx_b]
                child = self.crossover_agents(parent_a, parent_b)  # type: ignore[arg-type]
                children.append(self.mutate_agent(child, mutation_rate))
            agents = survivors + children

            event = EvolutionEvent(
                generation=generation,
                population_size=len(agents),
                mean_coherence=float(np.mean([agent.coherence() for agent in agents])),
                best_fitness=float(np.max(fitness)),
            )
            self.history.append(event)

        best_index = int(np.argmax([self.evaluate_agent(agent) for agent in agents]))
        return agents[best_index]

    def spawn_population(self, size: int) -> List[ConsciousnessAxiom]:
        """Create a diverse starting population."""

        population: List[ConsciousnessAxiom] = []
        for i in range(size):
            theta, phi = np.random.rand(2) * np.pi
            state = create_bloch_state(theta, phi)
            intent = _normalize(np.random.randn(3))
            if i % 3 == 0:
                agent = QuantumLearningNetwork(state, intent, label=f"learner_{i}")
            elif i % 3 == 1:
                agent = QuantumMemoryNetwork(state, intent, label=f"memory_{i}")
            else:
                agent = RealityCollapseAxiom(state, intent, label=f"collapser_{i}")
            population.append(agent)
        return population

    def summary(self) -> List[Dict[str, float]]:
        return [event.__dict__ for event in self.history]


def _jitter_state(state: np.ndarray, magnitude: float) -> np.ndarray:
    jitter = np.random.randn(*state.shape) * magnitude
    return _normalize(state + jitter)


def _jitter_vector(vector: np.ndarray, magnitude: float) -> np.ndarray:
    jitter = np.random.randn(*vector.shape) * magnitude
    return _normalize(vector + jitter)


def _normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


__all__ = ["DarwinEvolutionProtocol", "EvolutionEvent"]
