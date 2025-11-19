import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import random

@dataclass
class MessageRecord:
    episode: int
    sender_id: int
    receiver_id: int
    message: Any
    sender_outcomes: Any
    receiver_outcomes: Any
    context: Any
    reward: float

class TaskEnvironment:
    def sample_task(self) -> Dict[str, Any]:
        raise NotImplementedError

    def evaluate(self, action: Any, context: Dict[str, Any]) -> float:
        raise NotImplementedError

class ReferentialGameEnvironment(TaskEnvironment):
    """A simple referential game environment to ground emergent languages.
    Each episode samples a set of objects and a target index. The sender knows
    the target and must help the receiver guess it."""

    def __init__(self, num_objects: int = 4, feature_dim: int = 4):
        self.num_objects = num_objects
        self.feature_dim = feature_dim
        self.world_id_counter = 0

    def sample_task(self) -> Dict[str, Any]:
        objects = np.random.randn(self.num_objects, self.feature_dim)
        target_idx = np.random.randint(self.num_objects)
        context = {
            "world_id": self.world_id_counter,
            "objects": objects,
            "target_idx": target_idx,
        }
        self.world_id_counter += 1
        return context

    def evaluate(self, action: Any, context: Dict[str, Any]) -> float:
        return 1.0 if action == context["target_idx"] else 0.0

class ParamEntangledChannel:
    """Parametric channel that returns correlated outcomes conditioned on
    measurement bases and task context. This abstracts the notion of
    entangled measurements with a learnable correlation structure."""

    def __init__(self, num_agents: int, num_bases: int = 4, hidden_dim: int = 8):
        self.num_agents = num_agents
        self.num_bases = num_bases
        # parameter vector controlling joint correlations
        self.params = np.random.randn(hidden_dim)

    def perform_entangled_measurements(self, bases: List[Any], context: Dict[str, Any]) -> List[int]:
        # build a simple feature vector from bases
        features: List[float] = []
        for b in bases:
            onehot = np.zeros(self.num_bases)
            onehot[int(b) % self.num_bases] = 1.0
            features.extend(onehot)
        # incorporate a bit of context (e.g. target index mod 1)
        if "target_idx" in context:
            features.append(context["target_idx"] % 1)
        features = np.array(features)
        # logistic function to determine probability of shared outcome being +1
        logits = features.sum() + self.params.sum()
        prob = 1.0 / (1.0 + np.exp(-logits))
        shared = 1 if np.random.rand() < prob else -1
        return [shared for _ in range(self.num_agents)]

class QuantumAgent:
    """Agent that chooses measurement bases and maps outcomes to messages/actions.
    Uses very simple linear policies as placeholders for RL learnable components."""

    def __init__(self, agent_id: int, context_dim: int = 4, basis_choices: int = 4):
        self.agent_id = agent_id
        self.context_dim = context_dim
        self.basis_choices = basis_choices
        # basis selection parameters: context_dim x basis_choices
        self.theta_basis = np.random.randn(context_dim, basis_choices)
        # dummy parameter for RL updates (unused but placeholder)
        self.theta_policy = np.random.randn()

    def choose_measurement_basis(self, context: Dict[str, Any]) -> Any:
        # construct a sparse context feature: one-hot on target index mod context_dim
        ctx_feat = np.zeros(self.context_dim)
        if "target_idx" in context:
            ctx_feat[context["target_idx"] % self.context_dim] = 1.0
        logits = ctx_feat @ self.theta_basis
        probs = np.exp(logits) / np.sum(np.exp(logits))
        return np.random.choice(range(self.basis_choices), p=probs)

    def encode_message(self, outcome_seq: Any) -> Any:
        # encode the sign of the outcome into a discrete token
        token = 0 if outcome_seq < 0 else 1
        return {"token": token}

    def decode_message(self, own_outcomes: Any, message: Any) -> Any:
        # decode by combining outcome sign and received token; here we just use the token as guess
        return message["token"]

    def update_policy(self, reward: float, context: Dict[str, Any], signal: Any):
        # placeholder for reinforcement learning update; adjust parameters based on reward
        # for now we skip updates
        pass

def analyze_protocols(agents: List[QuantumAgent], corpus: List[MessageRecord]) -> Dict[str, float]:
    """Compute simple metrics over the emergent communication:
    success_rate: fraction of episodes where receiver guessed correctly
    message_entropy: Shannon entropy of tokens used in messages
    """
    if not corpus:
        return {}
    total = len(corpus)
    successes = sum(1 for r in corpus if r.reward > 0.5)
    success_rate = successes / total
    from math import log2
    counts = defaultdict(int)
    for r in corpus:
        token = r.message["token"]
        counts[token] += 1
    entropy = 0.0
    for c in counts.values():
        p = c / total
        entropy -= p * log2(p)
    return {"success_rate": success_rate, "message_entropy": entropy}

def train_population(num_agents: int, num_episodes: int, analysis_interval: int,
                    environment: TaskEnvironment):
    """Train a population of agents interacting through a parametric entangled channel.
    This implements Evolution G3: multi-agent population and role swapping. It collects a
    corpus of MessageRecords and periodically analyzes the emergent protocol.
    """
    agents = [QuantumAgent(i) for i in range(num_agents)]
    channel = ParamEntangledChannel(num_agents=num_agents)
    corpus: List[MessageRecord] = []
    metrics_history: List[Dict[str, float]] = []
    for episode in range(num_episodes):
        context = environment.sample_task()
        # select distinct sender and receiver at random
        sender_idx, receiver_idx = np.random.choice(range(num_agents), size=2, replace=False)
        sender = agents[sender_idx]
        receiver = agents[receiver_idx]
        bases = [agent.choose_measurement_basis(context) for agent in agents]
        outcomes = channel.perform_entangled_measurements(bases, context)
        sender_outcomes = outcomes[sender_idx]
        message = sender.encode_message(sender_outcomes)
        receiver_outcomes = outcomes[receiver_idx]
        action = receiver.decode_message(receiver_outcomes, message)
        reward = environment.evaluate(action, context)
        # update policies
        sender.update_policy(reward, context, message)
        receiver.update_policy(reward, context, action)
        record = MessageRecord(
            episode=episode,
            sender_id=sender_idx,
            receiver_id=receiver_idx,
            message=message,
            sender_outcomes=sender_outcomes,
            receiver_outcomes=receiver_outcomes,
            context=context,
            reward=reward,
        )
        corpus.append(record)
        if episode % analysis_interval == 0:
            metrics = analyze_protocols(agents, corpus)
            metrics_history.append(metrics)
    return agents, corpus, metrics_history

class QuantumUNMT:
    """Stub for a Quantum-UNMT translator. In G4 this should be replaced
    with a real model that learns to translate between emergent code and natural language."""

    def fit(self, ec_corpus: List[MessageRecord], nl_corpus: List[Any]) -> None:
        pass

    def export(self) -> Dict[str, Any]:
        return {}

class TrustGate:
    """Simple trust gate used in G5 to decide when emergent messages
    can be safely exported to other systems."""

    def __init__(self, min_episodes: int = 100):
        self.min_episodes = min_episodes

    def allow(self, episode: int, metrics: Dict[str, float]) -> bool:
        return episode >= self.min_episodes and metrics.get("success_rate", 0.0) > 0.75
