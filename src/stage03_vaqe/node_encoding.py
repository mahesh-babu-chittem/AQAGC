"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Node Encoding

==============================================================
"""

import numpy as np
import pandas as pd
import networkx as nx

from config import LAMBDA
from io_utils import save_node_encodings


class NodeEncoder:

    """
    Equation (31)

    Combines

    • Vulnerability Risk
    • Graph Centrality

    into a unified node encoding score.
    """

    def __init__(self, graph, nodes):

        self.graph = graph

        self.nodes = nodes.copy()

        self.risk_column = None

    # ----------------------------------------------------------

    def detect_risk_column(self):

        candidates = [

            "Risk_Score",
            "risk_score",
            "Risk",
            "risk",
            "Node_Risk",
            "Severity",
            "severity"

        ]

        for column in candidates:

            if column in self.nodes.columns:

                self.risk_column = column
                return

        raise ValueError(
            "Risk column not found."
        )

    # ----------------------------------------------------------

    def detect_node_column(self):

        candidates = [

            "Node_ID",
            "Node",
            "node",
            "id",
            "ID"

        ]

        for column in candidates:

            if column in self.nodes.columns:

                return column

        raise ValueError(
            "Node identifier column not found."
        )

    # ----------------------------------------------------------

    def compute_centrality(self):

        centrality = nx.degree_centrality(
            self.graph
        )

        return centrality

    # ----------------------------------------------------------

    def normalize(self, values):

        values = np.asarray(values)

        minimum = values.min()

        maximum = values.max()

        if maximum - minimum == 0:

            return np.ones_like(values)

        return (values - minimum) / (maximum - minimum)

    # ----------------------------------------------------------
    # Equation (31)
    # ----------------------------------------------------------

    def compute_scores(self):

        self.detect_risk_column()

        node_column = self.detect_node_column()

        centrality = self.compute_centrality()

        risks = self.nodes[
            self.risk_column
        ].astype(float).to_numpy()

        risks = self.normalize(risks)

        centrality_scores = []

        for node in self.nodes[node_column]:

            centrality_scores.append(

                centrality.get(
                    str(node),
                    0.0
                )

            )

        centrality_scores = self.normalize(
            centrality_scores
        )

        encoding = (

            LAMBDA * risks +

            (1 - LAMBDA) *

            centrality_scores

        )

        self.nodes["Centrality"] = centrality_scores

        self.nodes["Normalized_Risk"] = risks

        self.nodes["Node_Encoding"] = encoding

        save_node_encodings(
            self.nodes
        )

        return self.nodes

    # ----------------------------------------------------------

    def run(self):

        return self.compute_scores()