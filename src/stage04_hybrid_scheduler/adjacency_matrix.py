"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Adjacency Matrix Builder

==============================================================
"""

from __future__ import annotations

import networkx as nx
import numpy as np

from io_utils import (
    save_adjacency_matrix,
)


class AdjacencyMatrix:
    """
    Builds the weighted adjacency matrix used by
    both DTQW and CTQW.
    """

    def __init__(

        self,

        graph: nx.DiGraph,

    ):

        self.graph = graph

    ####################################################################
    # Build Matrix
    ####################################################################

    def build(self):

        matrix = nx.to_numpy_array(

            self.graph,

            dtype=np.float64,

            weight="weight",

        )

        save_adjacency_matrix(

            matrix

        )

        return matrix

    ####################################################################
    # Number of Nodes
    ####################################################################

    def number_of_nodes(self):

        return self.graph.number_of_nodes()

    ####################################################################
    # Shape
    ####################################################################

    def shape(self):

        return (

            self.number_of_nodes(),

            self.number_of_nodes(),

        )

    ####################################################################
    # Degree Vector
    ####################################################################

    def degree_vector(self):

        matrix = self.build()

        return np.sum(

            matrix,

            axis=1,

        )

    ####################################################################
    # Degree Matrix
    ####################################################################

    def degree_matrix(self):

        degree = self.degree_vector()

        return np.diag(

            degree

        )

    ####################################################################
    # Is Symmetric
    ####################################################################

    def is_symmetric(self):

        matrix = self.build()

        return np.allclose(

            matrix,

            matrix.T,

        )

    ####################################################################
    # Sparsity
    ####################################################################

    def sparsity(self):

        matrix = self.build()

        total = matrix.size

        nonzero = np.count_nonzero(

            matrix

        )

        return float(

            1.0 -

            (nonzero / total)

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        matrix = self.build()

        return {

            "shape": matrix.shape,

            "nodes": self.number_of_nodes(),

            "symmetric": self.is_symmetric(),

            "sparsity": self.sparsity(),

        }