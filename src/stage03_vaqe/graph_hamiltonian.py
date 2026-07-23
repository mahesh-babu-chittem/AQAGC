"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Graph Hamiltonian

==============================================================
"""

import numpy as np
import networkx as nx

from config import PROPAGATION_COEFFICIENT

from io_utils import (
    save_adjacency_matrix,
    save_hamiltonian,
)


class GraphHamiltonian:

    """
    Equation (30)

    H = ηA
    """

    def __init__(self, graph):

        self.graph = graph

        self.nodes = None

        self.adjacency = None

        self.hamiltonian = None

    # ----------------------------------------------------------

    def ordered_nodes(self):

        self.nodes = sorted(
            list(self.graph.nodes())
        )

    # ----------------------------------------------------------

    def adjacency_matrix(self):

        self.adjacency = nx.to_numpy_array(

            self.graph,

            nodelist=self.nodes,

            weight="weight",

            dtype=np.float64

        )

        save_adjacency_matrix(
            self.adjacency
        )

    # ----------------------------------------------------------
    # Equation (30)
    # ----------------------------------------------------------

    def build_hamiltonian(self):

        self.hamiltonian = (

            PROPAGATION_COEFFICIENT *

            self.adjacency

        )

        save_hamiltonian(
            self.hamiltonian
        )

    # ----------------------------------------------------------

    def run(self):

        self.ordered_nodes()

        self.adjacency_matrix()

        self.build_hamiltonian()

        return self.hamiltonian