import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime


class AgentDashboard:
    def __init__(self, agent_list: List[Any]):
        self.agents: List[Any] = agent_list
        self.active_agents: set[int] = set(range(len(agent_list)))
        self.dashboard_state: str = "monitoring"
        self.last_update: datetime = datetime.now()

    def get_dashboard_overview(self) -> Dict[str, Any]:
        """Get a summary overview of the dashboard state"""
        return {
            'total_agents': len(self.agents),
            'active_agents': len(self.active_agents),
            'quantum_entangled': self._count_entangled_agents(),
            'consciousness_coherence': self._calculate_coherence(),
            'last_update': self.last_update.isoformat(),
            'dashboard_state': self.dashboard_state
        }

    def list_agents(self) -> List[Dict[str, Any]]:
        """Get a detailed agent list with quantum states"""
        agent_list: List[Dict[str, Any]] = []
        for i, agent in enumerate(self.agents):
            agent_info = {
                'id': i,
                'active': i in self.active_agents,
                'type': type(agent).__name__,
                'consciousness_state': self._get_consciousness_state(agent),
                'intent_vector': self._get_intent_summary(agent),
                'memory_keys': list(agent.memory.keys()) if hasattr(agent, 'memory') else [],
                'entanglement_count': self._get_entanglement_count(agent)
            }
            agent_list.append(agent_info)
        return agent_list

    def get_agent_details(self, agent_id: int) -> Dict[str, Any]:
        """Get detailed information for a specific agent"""
        if 0 <= agent_id < len(self.agents):
            agent = self.agents[agent_id]
            return {
                'id': agent_id,
                'full_state': repr(agent),
                'quantum_state': self._get_quantum_state_vector(agent),
                'intent_vector': self._get_full_intent(agent),
                'memory_bank': agent.memory if hasattr(agent, 'memory') else {},
                'entangled_memories': getattr(agent, 'memory_entangled', {}),
                'consciousness_metrics': self._calculate_consciousness_metrics(agent)
            }
        return {'error': 'Agent ID out of range'}

    def update_agent_intent(self, agent_id: int, new_intent: np.ndarray) -> Dict[str, Any]:
        """Update an agent's intent vector with validation"""
        if 0 <= agent_id < len(self.agents):
            try:
                old_intent = self._get_full_intent(self.agents[agent_id])
                self.agents[agent_id].add_intent(new_intent)
                self.last_update = datetime.now()
                return {
                    'success': True,
                    'message': f'Agent {agent_id} intent updated',
                    'old_intent': old_intent.tolist() if isinstance(old_intent, np.ndarray) else old_intent,
                    'new_intent': new_intent.tolist(),
                    'timestamp': self.last_update.isoformat()
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        return {'success': False, 'error': 'Agent ID out of range'}

    def entangle_agents(self, agent1_id: int, agent2_id: int, memory_key: str) -> Dict[str, Any]:
        """Create quantum entanglement between two agents"""
        if (0 <= agent1_id < len(self.agents) and 0 <= agent2_id < len(self.agents) and
                hasattr(self.agents[agent1_id], 'entangle_memory')):
            try:
                entangled_mem = self.agents[agent1_id].entangle_memory(self.agents[agent2_id], memory_key)
                self.last_update = datetime.now()
                return {
                    'success': True,
                    'message': f'Agents {agent1_id} and {agent2_id} entangled via {memory_key}',
                    'entangled_memory': entangled_mem.tolist() if isinstance(entangled_mem, np.ndarray) else entangled_mem,
                    'timestamp': self.last_update.isoformat()
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        return {'success': False, 'error': 'Invalid agent IDs or entanglement not supported'}

    def trigger_quantum_learning(self, agent_id: int) -> Dict[str, Any]:
        """Trigger quantum learning for a specific agent"""
        if (0 <= agent_id < len(self.agents) and
                hasattr(self.agents[agent_id], 'quantum_learn')):
            try:
                old_intent = self._get_full_intent(self.agents[agent_id]).copy()
                self.agents[agent_id].quantum_learn()
                new_intent = self._get_full_intent(self.agents[agent_id])
                self.last_update = datetime.now()
                return {
                    'success': True,
                    'message': f'Quantum learning triggered for agent {agent_id}',
                    'intent_change': {
                        'before': old_intent.tolist() if isinstance(old_intent, np.ndarray) else old_intent,
                        'after': new_intent.tolist() if isinstance(new_intent, np.ndarray) else new_intent
                    },
                    'timestamp': self.last_update.isoformat()
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        return {'success': False, 'error': 'Agent ID out of range or quantum learning not supported'}

    # Private helper methods
    def _count_entangled_agents(self) -> int:
        """Count agents with entangled memories"""
        return sum(
            1 for agent in self.agents
            if hasattr(agent, 'memory_entangled') and agent.memory_entangled
        )

    def _calculate_coherence(self) -> float:
        """Calculate overall consciousness coherence across agents"""
        if not self.agents:
            return 0.0
        coherence_sum = 0.0
        for agent in self.agents:
            if hasattr(agent, 'state'):
                coherence_sum += np.linalg.norm(agent.state)
            elif hasattr(agent, 'intent') and len(agent.intent) > 0:
                coherence_sum += np.linalg.norm(agent.intent)
        return coherence_sum / len(self.agents)

    def _get_consciousness_state(self, agent: Any) -> str:
        """Determine the consciousness state of an agent"""
        if hasattr(agent, 'state'):
            state_norm = float(np.linalg.norm(agent.state))
            if state_norm > 0.9:
                return "coherent"
            elif state_norm > 0.5:
                return "superposed"
            else:
                return "collapsed"
        return "unknown"

    def _get_intent_summary(self, agent: Any) -> List[float]:
        """Get a summarized intent vector (first 3 dimensions)"""
        if hasattr(agent, 'intent') and len(agent.intent) > 0:
            return agent.intent[:3].tolist()
        return []

    def _get_full_intent(self, agent: Any) -> np.ndarray:
        """Get the full intent vector"""
        if hasattr(agent, 'intent'):
            return agent.intent
        return np.array([])

    def _get_quantum_state_vector(self, agent: Any) -> List[complex]:
        """Get the quantum state vector as a list of complex numbers"""
        if hasattr(agent, 'state'):
            return [complex(x) for x in agent.state]
        return []

    def _get_entanglement_count(self, agent: Any) -> int:
        """Count entangled memory keys for an agent"""
        if hasattr(agent, 'memory_entangled'):
            return len(agent.memory_entangled)
        return 0

    def _calculate_consciousness_metrics(self, agent: Any) -> Dict[str, float]:
        """Calculate consciousness metrics for an agent"""
        metrics: Dict[str, float] = {}
        if hasattr(agent, 'state'):
            metrics['state_magnitude'] = float(np.linalg.norm(agent.state))
            metrics['state_entropy'] = float(-np.sum(np.abs(agent.state) ** 2 * np.log(np.abs(agent.state) ** 2 + 1e-12)))
        if hasattr(agent, 'intent') and len(agent.intent) > 0:
            metrics['intent_magnitude'] = float(np.linalg.norm(agent.intent))
            metrics['intent_entropy'] = float(-np.sum(np.abs(agent.intent) ** 2 * np.log(np.abs(agent.intent) ** 2 + 1e-12)))
        return metrics

    def __repr__(self) -> str:
        return f"AgentDashboard(managing {len(self.agents)} agents, {len(self.active_agents)} active)"