"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Graph Loader

==============================================================
"""

from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd

from io_utils import (
    load_attack_graph,
    load_nodes,
    load_edges,
)


class GraphLoader:
    """
    Loads and validates the Stage-04 attack graph.
    """

    def __init__(self):

        self.graph = load_attack_graph()

        self.nodes = load_nodes()

        self.edges = load_edges()

    ####################################################################
    # Graph
    ####################################################################

    def get_graph(self):

        return self.graph

    ####################################################################
    # Nodes
    ####################################################################

    def get_nodes(self):

        return self.nodes.copy()

    ####################################################################
    # Edges
    ####################################################################

    def get_edges(self):

        return self.edges.copy()

    ####################################################################
    # Basic Statistics
    ####################################################################

    def number_of_nodes(self):

        return self.graph.number_of_nodes()

    def number_of_edges(self):

        return self.graph.number_of_edges()

    ####################################################################
    # Degree Information
    ####################################################################

    def degree_vector(self):

        degrees = []

        for node in self.graph.nodes():

            degrees.append(

                self.graph.degree(node)

            )

        return np.asarray(

            degrees,

            dtype=np.int32,

        )

    ####################################################################
    # Density
    ####################################################################

    def density(self):

        return nx.density(

            self.graph

        )

    ####################################################################
    # Connected Components
    ####################################################################

    def connected_components(self):

        if self.graph.is_directed():

            components = list(

                nx.weakly_connected_components(

                    self.graph

                )

            )

        else:

            components = list(

                nx.connected_components(

                    self.graph

                )

            )

        return components

    ####################################################################
    # Largest Component
    ####################################################################

    def largest_component(self):

        components = self.connected_components()

        largest = max(

            components,

            key=len,

        )

        return largest

    ####################################################################
    # Adjacency Matrix
    ####################################################################

    def adjacency_matrix(self):

        return nx.to_numpy_array(

            self.graph,

            dtype=np.float64,

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        return {

            "number_of_nodes":

                self.number_of_nodes(),

            "number_of_edges":

                self.number_of_edges(),

            "density":

                float(

                    self.density()

                ),

            "connected_components":

                len(

                    self.connected_components()

                ),

            "largest_component_size":

                len(

                    self.largest_component()

                ),

        }