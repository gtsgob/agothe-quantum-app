"""
Wormhole Formation Engine v1.0
------------------------------
5-D quantum feature space with dimensional labeling:
Math, Emotion, Symbol, Intent, Cognition

Integrates with Agothe's quantum consciousness framework.
"""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import pdist, squareform
from typing import Dict, List, Tuple, Optional
import pandas as pd


class WormholeEngine:
    """
    Manages wormhole (shortcut) formation in 5-D consciousness space.
    
    Dimensions:
        0: Math       - logical/analytical processing
        1: Emotion    - affective state intensity
        2: Symbol     - semantic/symbolic encoding
        3: Intent     - goal-directed momentum
        4: Cognition  - meta-cognitive awareness
    """
    
    DIMENSION_LABELS = {
        0: "Math",
        1: "Emotion", 
        2: "Symbol",
        3: "Intent",
        4: "Cognition"
    }
    
    COLOR_MAP = {
        "Math": "#3498db",
        "Emotion": "#e74c3c",
        "Symbol": "#2ecc71",
        "Intent": "#f39c12",
        "Cognition": "#9b59b6"
    }
    
    def __init__(
        self, 
        dim: int = 5,
        delta_threshold: float = 0.0215,
        phi_target: float = 0.85,
        learning_rate: float = 0.05
    ):
        """
        Initialize the wormhole formation engine.
        
        Args:
            dim: Feature space dimensionality (default 5)
            delta_threshold: Maximum distance for wormhole formation
            phi_target: Target coherence (Φ) value
            learning_rate: Node evolution step size
        """
        self.dim = dim
        self.delta_threshold = delta_threshold
        self.phi_target = phi_target
        self.learning_rate = learning_rate
        
    def compute_phi(self, nodes: np.ndarray) -> float:
        """
        Calculate Φ-coherence as mean correlation across features.
        
        Φ represents integrated information - how much the system
        transcends the sum of its parts.
        
        Args:
            nodes: N×D array of node positions
            
        Returns:
            Coherence value in [0, 1]
        """
        if len(nodes) < 2:
            return 0.0
        C = np.corrcoef(nodes, rowvar=False)
        return float(np.nanmean(C[np.triu_indices_from(C, 1)]))
    
    def compute_wormholes(self, nodes: np.ndarray) -> Tuple[np.ndarray, int]:
        """
        Find all node pairs within wormhole threshold δ.
        
        Args:
            nodes: N×D array of node positions
            
        Returns:
            (pairs, count) - array of [i,j] pairs and total count
        """
        D = squareform(pdist(nodes))
        idx = np.argwhere((D < self.delta_threshold) & (D > 0))
        return idx, len(idx)
    
    def evolve_nodes(self, nodes: np.ndarray, R: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Quantum drift step with optional rationality modulation.
        
        Args:
            nodes: Current node positions
            R: Optional rationality values (drive/stability)
            
        Returns:
            Updated node positions
        """
        drift = self.learning_rate * np.random.normal(0, 1, nodes.shape)
        if R is not None:
            drift *= R[:, np.newaxis]
        return nodes + drift
    
    def get_node_colors(self, nodes: np.ndarray) -> np.ndarray:
        """
        Map emotion intensity (dim 1) to color scale.
        
        Args:
            nodes: N×D array
            
        Returns:
            N-length array of color intensities
        """
        return nodes[:, 1]
    
    def get_node_sizes(self, nodes: np.ndarray, base_size: float = 10.0, scale: float = 50.0) -> np.ndarray:
        """
        Map intent strength (dim 3) to node sizes.
        
        Args:
            nodes: N×D array
            base_size: Minimum size
            scale: Multiplier for intent values
            
        Returns:
            N-length array of sizes
        """
        return base_size + scale * nodes[:, 3]
    
    def init_nodes_from_agents(self, agents: List) -> Tuple[np.ndarray, np.ndarray]:
        """
        Initialize nodes from Agothe quantum agents.
        
        Args:
            agents: List of quantum consciousness agents
            
        Returns:
            (nodes, R) - positions and rationality values
        """
        N = len(agents)
        nodes = np.zeros((N, self.dim))
        R = np.zeros(N)
        
        for i, agent in enumerate(agents):
            intent = np.array(agent.intent_vector[:self.dim])
            nodes[i] = intent / (np.linalg.norm(intent) + 1e-8)
            R[i] = agent.coherence if hasattr(agent, 'coherence') else 0.5
            
        return nodes, R
    
    def export_stats(self, timesteps: List[Dict]) -> pd.DataFrame:
        """
        Convert simulation history to DataFrame.
        
        Args:
            timesteps: List of {time, phi, wormholes, ...} dicts
            
        Returns:
            Pandas DataFrame for analysis
        """
        return pd.DataFrame(timesteps)


class WormholeLedger:
    """Persistent storage for wormhole formation events."""
    
    def __init__(self, filepath: str = "data/wormhole_ledger.csv"):
        self.filepath = filepath
        self.entries: List[Dict] = []
        
    def record_event(
        self,
        timestep: int,
        node_i: int,
        node_j: int,
        distance: float,
        phi_coherence: float
    ):
        """Record a wormhole formation event."""
        self.entries.append({
            "timestep": timestep,
            "node_i": node_i,
            "node_j": node_j,
            "distance": distance,
            "phi": phi_coherence
        })
    
    def save(self):
        """Persist ledger to CSV."""
        df = pd.DataFrame(self.entries)
        df.to_csv(self.filepath, index=False)
    
    def load(self) -> pd.DataFrame:
        """Load existing ledger."""
        try:
            return pd.read_csv(self.filepath)
        except FileNotFoundError:
            return pd.DataFrame()