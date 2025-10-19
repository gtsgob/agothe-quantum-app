"""Navigation utilities used by the Streamlit dashboard."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class QuantumNavigation:
    """Stateful helper that models navigation as a quantum superposition."""

    current_route: str = "Home"
    available_routes: List[str] = field(default_factory=list)
    navigation_history: List[str] = field(default_factory=list)
    amplitudes: Dict[str, float] = field(default_factory=dict)

    def quantum_menu(self, options: List[str]) -> List[str]:
        self.available_routes = options
        amplitudes = np.random.rand(len(options))
        amplitudes = amplitudes / amplitudes.sum()
        self.amplitudes = {route: float(value) for route, value in zip(options, amplitudes)}
        return self.available_routes

    def collapse_to_route(self, selection: str) -> str:
        if selection not in self.available_routes:
            return "❌ Invalid route selection"
        if self.current_route != selection:
            self.navigation_history.append(self.current_route)
            self.current_route = selection
        probability = self.amplitudes.get(selection, 0.0)
        return f"✅ Collapsed to {selection} (p={probability:.2f})"

    def quantum_breadcrumb(self, depth: int = 5) -> List[str]:
        trail = self.navigation_history[-depth:] + [self.current_route]
        return trail

    def superposition_probability(self, route: str) -> float:
        return self.amplitudes.get(route, 0.0)

    def entangle_navigation(self, other: "QuantumNavigation") -> Dict[str, float]:
        shared = set(self.available_routes) & set(other.available_routes)
        if not shared:
            return {"correlation": 0.0}
        correlation = float(np.mean([self.amplitudes[route] * other.amplitudes[route] for route in shared]))
        return {"correlation": correlation, "shared_routes": len(shared)}

    def route_config(self, route: str) -> Dict[str, Any]:
        config: Dict[str, Dict[str, Any]] = {
            "Home": {
                "components": ["dashboard", "quantum_overview"],
                "quantum_state": "stable",
            },
            "Agents": {
                "components": ["agent_list", "consciousness_monitor"],
                "quantum_state": "entangled",
            },
            "Quantum States": {
                "components": ["state_visualiser", "collapse_controls"],
                "quantum_state": "superposed",
            },
            "Evolution": {
                "components": ["darwin_protocol", "generation_tracker"],
                "quantum_state": "adaptive",
            },
            "Settings": {
                "components": ["config_panel", "quantum_parameters"],
                "quantum_state": "coherent",
            },
        }
        return config.get(route, {"components": ["default"], "quantum_state": "unknown"})

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"QuantumNavigation(route={self.current_route!r}, available={len(self.available_routes)})"


_singleton: Optional[QuantumNavigation] = None


def get_quantum_navigator() -> QuantumNavigation:
    global _singleton
    if _singleton is None:
        _singleton = QuantumNavigation()
    return _singleton


__all__ = ["QuantumNavigation", "get_quantum_navigator"]
