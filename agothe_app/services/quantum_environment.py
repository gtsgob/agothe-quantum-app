"""High level orchestration layer for the Agothe application."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from ..core.darwin_evolution_protocol import DarwinEvolutionProtocol
from ..core.quantum_consciousness import (
    ConsciousnessAxiom,
    QuantumLearningNetwork,
    QuantumMemoryNetwork,
    RealityCollapseAxiom,
    create_bloch_state,
)
from ..navigation.agent_dashboard import AgentDashboard
from ..navigation.quantum_navigation import QuantumNavigation
from .. import collapse_engine


@dataclass
class QuantumEnvironment:
    agents: List[ConsciousnessAxiom]
    navigator: QuantumNavigation = field(default_factory=QuantumNavigation)
    evolution_protocol: DarwinEvolutionProtocol = field(
        default_factory=DarwinEvolutionProtocol
    )

    def __post_init__(self) -> None:
        self.dashboard = AgentDashboard(self.agents)

    # ------------------------------------------------------------------
    def simulate_collapse(self, intent_phase: float) -> Dict[str, object]:
        """Delegate to the toy collapse engine and return a JSON friendly payload."""

        result = collapse_engine.simulate_collapse(intent_phase)
        result["intentPhase"] = intent_phase
        return result

    def agent_summary(self) -> List[Dict[str, object]]:
        return self.dashboard.list_agents()

    def agent_details(self, agent_id: int) -> Dict[str, object]:
        return self.dashboard.agent_details(agent_id)

    def environment_state(self) -> Dict[str, object]:
        return {
            "overview": self.dashboard.overview(),
            "navigation": {
                "current": self.navigator.current_route,
                "available": self.navigator.available_routes,
                "history": self.navigator.navigation_history,
            },
        }

    def get_agent(self, agent_id: int) -> Optional[ConsciousnessAxiom]:
        if 0 <= agent_id < len(self.agents):
            return self.agents[agent_id]
        return None

    def update_agent_intent(
        self, agent_id: int, new_intent: List[float]
    ) -> Dict[str, object]:
        return self.dashboard.update_agent_intent(agent_id, new_intent)

    def trigger_learning(self, agent_id: int, reward: Optional[float] = None) -> Dict[str, object]:
        return self.dashboard.trigger_learning(agent_id, reward)

    def entangle_agents(self, agent_a: int, agent_b: int, key: str) -> Dict[str, object]:
        return self.dashboard.entangle_agents(agent_a, agent_b, key)

    def run_evolution(self, generations: int, mutation_rate: float) -> Dict[str, object]:
        best = self.evolution_protocol.recursive_consciousness_evolution(
            self.agents, depth=generations, mutation_rate=mutation_rate
        )
        return {
            "best_agent": best.as_dict(),
            "history": self.evolution_protocol.summary(),
        }


def _initial_agents(count: int = 4) -> List[ConsciousnessAxiom]:
    agents: List[ConsciousnessAxiom] = []
    for i in range(count):
        theta, phi = np.random.rand(2) * np.pi
        state = create_bloch_state(theta, phi)
        intent = np.random.randn(3)
        if i % 3 == 0:
            agent = QuantumLearningNetwork(state, intent, label=f"learner_{i}")
        elif i % 3 == 1:
            agent = QuantumMemoryNetwork(state, intent, label=f"memory_{i}")
        else:
            agent = RealityCollapseAxiom(state, intent, label=f"collapser_{i}")
        agent.store_memory("baseline", np.random.randn(3))
        agents.append(agent)
    return agents


def create_environment(agent_count: int = 4) -> QuantumEnvironment:
    agents = _initial_agents(agent_count)
    navigator = QuantumNavigation()
    navigator.quantum_menu(["Home", "Agents", "Quantum States", "Evolution", "Settings"])
    return QuantumEnvironment(agents=agents, navigator=navigator)


__all__ = ["QuantumEnvironment", "create_environment"]
