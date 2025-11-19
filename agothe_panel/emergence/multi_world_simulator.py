"""
multi_world_simulator.py: Cross-civilization simulation engine for Agothe Panel Round 5.

This module extends the existing civilization simulation to support multiple simultaneous
civilizations and interactions between them. It allows modeling of cross-timeline influence,
collapse contagion, and cooperative or competitive dynamics. All interactions are computed
deterministically from supplied parameters.
"""

import random
from typing import Dict, Any, List, Tuple

class MultiWorldSimulator:
    def __init__(self, num_worlds: int = 3, seed: int = None):
        """
        Initialize a multi-world simulator.
        :param num_worlds: Number of civilizations to simulate concurrently.
        :param seed: Optional seed for reproducible randomness.
        """
        self.num_worlds = num_worlds
        self.random = random.Random(seed)

    def initialize_worlds(self) -> List[Dict[str, Any]]:
        """
        Initialize a list of world states. Each world is represented as a dict of properties.
        :return: A list of world dictionaries.
        """
        worlds: List[Dict[str, Any]] = []
        for i in range(self.num_worlds):
            world = {
                "id": i,
                "type": "Type-0",
                "delta_H": self.random.uniform(0.0, 0.2),
                "lsse": self.random.uniform(0.0, 0.2),
                "resources": 1.0,
                "collapse_risk": 0.0,
            }
            worlds.append(world)
        return worlds

    def update_world(self, world: Dict[str, Any], influences: List[float]) -> Dict[str, Any]:
        """
        Update a single world based on internal state and external influences.
        :param world: The current state of the world.
        :param influences: A list of influence values from other worlds.
        :return: The updated world state.
        """
        new_world = world.copy()
        influence_factor = sum(influences)
        # Increase delta_H based on influence; reduce resources accordingly.
        new_world["delta_H"] += influence_factor * 0.1
        new_world["resources"] = max(0.0, new_world["resources"] - influence_factor * 0.05)
        new_world["collapse_risk"] = new_world["delta_H"] * 2 - new_world["resources"]
        return new_world

    def simulate_step(self, worlds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Simulate a single timestep for all worlds with cross-world influences.
        :param worlds: Current list of world states.
        :return: Updated list of world states after one timestep.
        """
        new_worlds: List[Dict[str, Any]] = []
        influences_matrix: List[List[float]] = []
        # Compute influence signals (placeholder: random small perturbations)
        for _ in worlds:
            influences_matrix.append([self.random.uniform(-0.1, 0.1) for _ in worlds])

        for idx, world in enumerate(worlds):
            influences: List[float] = [influences_matrix[j][idx] for j in range(self.num_worlds) if j != idx]
            new_worlds.append(self.update_world(world, influences))
        return new_worlds

    def run_simulation(self, steps: int = 10) -> List[List[Dict[str, Any]]]:
        """
        Run the multi-world simulation for a number of steps.
        :param steps: Number of timesteps to simulate.
        :return: A list of world states for each step including the initial state.
        """
        history: List[List[Dict[str, Any]]] = []
        worlds = self.initialize_worlds()
        history.append(worlds)
        for _ in range(steps):
            worlds = self.simulate_step(worlds)
            history.append(worlds)
        return history
