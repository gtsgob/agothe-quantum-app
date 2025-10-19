"""Dashboard models used by the Streamlit interface and API."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import numpy as np

from ..core.quantum_consciousness import (
    ConsciousnessAxiom,
    QuantumLearningNetwork,
    QuantumMemoryNetwork,
)


@dataclass
class AgentDashboard:
    agents: List[ConsciousnessAxiom]
    active_agents: set[int] = field(default_factory=set)
    state: str = "monitoring"
    last_update: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if not self.active_agents:
            self.active_agents = set(range(len(self.agents)))

    # ------------------------------------------------------------------
    def overview(self) -> Dict[str, Any]:
        coherence = float(np.mean([agent.coherence() for agent in self.agents]))
        entangled = sum(1 for agent in self.agents if agent.memory_entangled)
        return {
            "total_agents": len(self.agents),
            "active_agents": len(self.active_agents),
            "quantum_entangled": entangled,
            "consciousness_coherence": coherence,
            "last_update": self.last_update.isoformat(),
            "dashboard_state": self.state,
        }

    def list_agents(self) -> List[Dict[str, Any]]:
        payload: List[Dict[str, Any]] = []
        for index, agent in enumerate(self.agents):
            payload.append(
                {
                    "id": index,
                    "label": agent.label,
                    "type": type(agent).__name__,
                    "active": index in self.active_agents,
                    "coherence": agent.coherence(),
                    "intent": agent.intent.tolist(),
                    "memory_keys": list(agent.memory.keys()),
                }
            )
        return payload

    def agent_details(self, agent_id: int) -> Dict[str, Any]:
        if 0 <= agent_id < len(self.agents):
            agent = self.agents[agent_id]
            return {
                "id": agent_id,
                "label": agent.label,
                "state_vector": [complex(x) for x in agent.state],
                "intent": agent.intent.tolist(),
                "memory_bank": {k: v.tolist() for k, v in agent.memory.items()},
                "entangled": {k: v.tolist() for k, v in agent.memory_entangled.items()},
                "coherence": agent.coherence(),
            }
        return {"error": "Agent ID out of range"}

    def update_agent_intent(self, agent_id: int, new_intent: Iterable[float]) -> Dict[str, Any]:
        if 0 <= agent_id < len(self.agents):
            agent = self.agents[agent_id]
            previous = agent.intent.copy()
            agent.add_intent(np.asarray(new_intent))
            self.last_update = datetime.utcnow()
            return {
                "success": True,
                "message": f"Agent {agent_id} intent updated",
                "old_intent": previous.tolist(),
                "new_intent": agent.intent.tolist(),
                "timestamp": self.last_update.isoformat(),
            }
        return {"success": False, "error": "Agent ID out of range"}

    def trigger_learning(self, agent_id: int, reward: Optional[float] = None) -> Dict[str, Any]:
        if 0 <= agent_id < len(self.agents):
            agent = self.agents[agent_id]
            if isinstance(agent, QuantumLearningNetwork):
                before = agent.intent.copy()
                agent.quantum_learn(reward)
                self.last_update = datetime.utcnow()
                return {
                    "success": True,
                    "message": f"Learning executed for agent {agent_id}",
                    "before": before.tolist(),
                    "after": agent.intent.tolist(),
                    "timestamp": self.last_update.isoformat(),
                }
            return {"success": False, "error": "Agent does not support learning"}
        return {"success": False, "error": "Agent ID out of range"}

    def entangle_agents(self, agent_a: int, agent_b: int, key: str) -> Dict[str, Any]:
        if agent_a == agent_b:
            return {"success": False, "error": "Cannot entangle an agent with itself"}
        if 0 <= agent_a < len(self.agents) and 0 <= agent_b < len(self.agents):
            first = self.agents[agent_a]
            second = self.agents[agent_b]
            if isinstance(first, QuantumMemoryNetwork) and isinstance(
                second, QuantumMemoryNetwork
            ):
                try:
                    entangled = first.entangle_memory(second, key)
                except KeyError as exc:
                    return {"success": False, "error": str(exc)}
                self.last_update = datetime.utcnow()
                return {
                    "success": True,
                    "message": f"Agents {agent_a} and {agent_b} entangled via '{key}'",
                    "entangled_state": entangled.tolist(),
                    "timestamp": self.last_update.isoformat(),
                }
            return {"success": False, "error": "Both agents must support entanglement"}
        return {"success": False, "error": "Agent ID out of range"}

    def deactivate_agent(self, agent_id: int) -> None:
        self.active_agents.discard(agent_id)
        self.last_update = datetime.utcnow()

    def activate_agent(self, agent_id: int) -> None:
        self.active_agents.add(agent_id)
        self.last_update = datetime.utcnow()


__all__ = ["AgentDashboard"]
