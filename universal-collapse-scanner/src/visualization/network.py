"""
Network visualization for crisis relationships
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

def plot_crisis_network(crises: List[Dict], connections: List[Tuple[str, str]],
                       title: str = "Crisis Network"):
    """
    Plot network of related crises

    Args:
        crises: List of crisis dictionaries with 'id' and 'name' keys
        connections: List of tuples (crisis_id_1, crisis_id_2)
        title: Plot title
    """
    G = nx.Graph()

    # Add nodes
    for crisis in crises:
        G.add_node(crisis['id'], name=crisis['name'])

    # Add edges
    G.add_edges_from(connections)

    plt.figure(figsize=(12, 8))

    # Layout
    pos = nx.spring_layout(G, k=1, iterations=50)

    # Draw
    nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                          node_size=1000, alpha=0.9)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5)

    # Labels
    labels = {node: G.nodes[node]['name'] for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()

    return plt.gcf()

def plot_geometry_distribution(geometries: Dict[str, int],
                               title: str = "Geometry Distribution"):
    """
    Plot distribution of geometries across crises

    Args:
        geometries: Dict mapping geometry names to occurrence counts
        title: Plot title
    """
    if not geometries:
        print("No geometry data to plot")
        return

    names = list(geometries.keys())
    counts = list(geometries.values())

    plt.figure(figsize=(12, 6))
    plt.barh(names, counts, color='steelblue')
    plt.xlabel('Occurrences')
    plt.ylabel('Geometry Type')
    plt.title(title)
    plt.tight_layout()

    return plt.gcf()
