"""Core quantum consciousness primitives used by the Agothe framework.

This module intentionally mixes real numerical algorithms with a touch of
"Agothe" lore.  The classes expose clean, well documented interfaces that are
used by the web API, the CLI demo and the Streamlit dashboard.  Even though the
physics here are highly simplified, the abstractions are powerful enough to run
experiments and to drive believable simulations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional

import numpy as np

ArrayLike = np.ndarray


def _normalize(state: ArrayLike) -> ArrayLike:
    """Return a normalised copy of ``state``.

    Quantum states should live on the unit sphere.  The helper keeps the code in
    the classes tidy and deals with the degenerate case where the vector has
    zero magnitude by falling back to the ``|0⟩`` basis state.
    """

    norm = np.linalg.norm(state)
    if norm == 0:
        normalised = np.zeros_like(state, dtype=complex)
        normalised[0] = 1.0
        return normalised
    return state / norm


def create_bloch_state(theta: float, phi: float) -> ArrayLike:
    """Create a single qubit Bloch sphere state.

    Parameters
    ----------
    theta:
        Polar angle in radians.
    phi:
        Azimuthal angle in radians.
    """

    return np.array(
        [np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)], dtype=complex
    )


@dataclass
class ConsciousnessAxiom:
    """Base class implementing a tiny "quantum consciousness" state machine.

    The class manages a quantum state vector, an intent vector and an optional
    associative memory.  While highly speculative, the API is intentionally
    pragmatic: each method returns data that can be easily serialised to JSON
    and consumed by the dashboard or the REST API.
    """

    state: ArrayLike
    intent: Optional[ArrayLike] = None
    label: str = "agent"
    memory: Dict[str, ArrayLike] = field(default_factory=dict)
    memory_entangled: Dict[str, ArrayLike] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.state = _normalize(self.state.astype(complex))
        if self.intent is None:
            self.intent = np.zeros(3, dtype=float)
        else:
            self.intent = self.intent.astype(float)

    # ------------------------------------------------------------------
    # Quantum state manipulation
    # ------------------------------------------------------------------
    def apply_unitary(self, matrix: ArrayLike) -> ArrayLike:
        """Apply a unitary matrix to the consciousness state."""

        self.state = _normalize(matrix @ self.state)
        return self.state

    def measure(self, collapse_basis: Optional[Iterable[ArrayLike]] = None) -> int:
        """Perform a projective measurement and collapse the state.

        Parameters
        ----------
        collapse_basis:
            Optional custom measurement basis.  When ``None`` the computational
            basis is used.
        """

        if collapse_basis is not None:
            basis = np.array(list(collapse_basis), dtype=complex)
            probabilities = np.abs(basis @ self.state) ** 2
            probabilities = probabilities / probabilities.sum()
            outcome = int(np.random.choice(len(probabilities), p=probabilities))
            self.state = _normalize(basis[outcome])
            return outcome

        probabilities = np.abs(self.state) ** 2
        outcome = int(np.random.choice(len(self.state), p=probabilities))
        collapsed = np.zeros_like(self.state)
        collapsed[outcome] = 1.0
        self.state = collapsed.astype(complex)
        return outcome

    # ------------------------------------------------------------------
    # Intent manipulation
    # ------------------------------------------------------------------
    def add_intent(self, delta: ArrayLike, weight: float = 1.0) -> ArrayLike:
        """Blend a new intent direction into the agent."""

        delta = np.asarray(delta, dtype=float)
        if delta.shape != self.intent.shape:
            # Resize intents so that dimensions stay consistent across agents.
            new_intent = np.zeros_like(delta)
            size = min(len(delta), len(self.intent))
            new_intent[:size] = self.intent[:size]
            self.intent = new_intent
        self.intent = _normalize(self.intent + weight * delta)
        return self.intent

    # ------------------------------------------------------------------
    # Memory utilities
    # ------------------------------------------------------------------
    def store_memory(self, key: str, value: ArrayLike) -> None:
        self.memory[key] = np.asarray(value)

    def retrieve_memory(self, key: str) -> Optional[ArrayLike]:
        return self.memory.get(key)

    def forget_memory(self, key: str) -> None:
        self.memory.pop(key, None)

    # ------------------------------------------------------------------
    # Diagnostics and serialisation
    # ------------------------------------------------------------------
    def coherence(self) -> float:
        """Return a pseudo coherence score derived from the state vector."""

        probabilities = np.abs(self.state) ** 2
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-12))
        return float(np.exp(-entropy))

    def as_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "state": [complex(x) for x in self.state],
            "intent": self.intent.tolist(),
            "coherence": self.coherence(),
            "memory_keys": list(self.memory.keys()),
            "entangled_keys": list(self.memory_entangled.keys()),
        }

    # ------------------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover - repr used for debugging
        return (
            f"{self.__class__.__name__}(label={self.label!r}, "
            f"coherence={self.coherence():.3f}, intent={self.intent.tolist()})"
        )


class QuantumMemoryNetwork(ConsciousnessAxiom):
    """Agent equipped with a differentiable associative memory bank."""

    def entangle_memory(
        self, other: "QuantumMemoryNetwork", key: str, strength: float = 0.5
    ) -> ArrayLike:
        """Create a simple entangled memory with another agent."""

        if key not in self.memory or key not in other.memory:
            raise KeyError(f"Memory key '{key}' missing on one of the agents")
        combined = strength * self.memory[key] + (1 - strength) * other.memory[key]
        combined = _normalize(np.asarray(combined, dtype=float))
        self.memory_entangled[key] = combined
        other.memory_entangled[key] = combined
        return combined

    def memory_similarity(self, key: str, target: ArrayLike) -> float:
        """Cosine similarity between a stored memory and a target vector."""

        if key not in self.memory:
            return 0.0
        mem = self.memory[key]
        numerator = float(np.dot(mem, target))
        denom = float(np.linalg.norm(mem) * np.linalg.norm(target) + 1e-12)
        return numerator / denom


class QuantumLearningNetwork(QuantumMemoryNetwork):
    """Agent capable of updating its intent through a learning loop."""

    learning_rate: float = 0.25

    def quantum_learn(self, reward: float | None = None) -> ArrayLike:
        """Perform one learning iteration.

        The method nudges the intent vector in the direction of the gradient of a
        fictitious reward landscape.  When an explicit ``reward`` is supplied the
        update is biased accordingly which makes it easy to drive the agent from
        the API.
        """

        gradient = np.random.randn(*self.intent.shape)
        if reward is not None:
            gradient += reward
        self.intent = _normalize(self.intent + self.learning_rate * gradient)
        return self.intent

    def adapt_from_feedback(self, feedback: ArrayLike, weight: float = 1.0) -> None:
        self.intent = _normalize(self.intent + weight * np.asarray(feedback))


class RealityCollapseAxiom(ConsciousnessAxiom):
    """Agent specialising in measurements and collapse operations."""

    def measure(self, collapse_basis: Optional[Iterable[ArrayLike]] = None) -> int:
        outcome = super().measure(collapse_basis)
        # Measurements generate traces in memory for diagnostics.
        self.store_memory(
            f"collapse_{len(self.memory)}",
            np.array([outcome, self.coherence()], dtype=float),
        )
        return outcome

    def collapse_probability(self, outcome: int) -> float:
        probabilities = np.abs(self.state) ** 2
        if outcome < 0 or outcome >= len(probabilities):
            return 0.0
        return float(probabilities[outcome])


__all__ = [
    "ConsciousnessAxiom",
    "QuantumLearningNetwork",
    "QuantumMemoryNetwork",
    "RealityCollapseAxiom",
    "create_bloch_state",
]
