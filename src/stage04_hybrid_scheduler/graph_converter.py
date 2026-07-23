"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Graph Converter

==============================================================
"""

from __future__ import annotations

import networkx as nx
import numpy as np

from io_utils import (
    save_graph_statistics,
)


class GraphConverter:

    """
    Computes graph statistics used by the
    adaptive scheduler.
    """

    def __init__(

        self,

        graph: nx.DiGraph,

        node_dataframe,

    ):

        self.graph = graph

        self.nodes = node_dataframe

    ####################################################################
    # Number of Nodes
    ####################################################################

    def number_of_nodes(self):

        return self.graph.number_of_nodes()

    ####################################################################
    # Number of Edges
    ####################################################################

    def number_of_edges(self):

        return self.graph.number_of_edges()

    ####################################################################
    # Graph Density
    ####################################################################

    def graph_density(self):

        return float(

            nx.density(

                self.graph

            )

        )

    ####################################################################
    # Average Degree
    ####################################################################

    def average_degree(self):

        degree = [

            d

            for _, d in self.graph.degree()

        ]

        return float(

            np.mean(degree)

        )

    ####################################################################
    # Average Risk
    ####################################################################

    def average_risk(self):

        candidates = [

            "Node_Encoding",

            "Normalized_Risk",

            "Risk_Score",

            "risk_score",

            "Risk",

            "risk",

        ]

        for column in candidates:

            if column in self.nodes.columns:

                return float(

                    self.nodes[column]

                    .astype(float)

                    .mean()

                )

        raise ValueError(

            "Risk column not found."

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        summary = {

            "number_of_nodes":

                self.number_of_nodes(),

            "number_of_edges":

                self.number_of_edges(),

            "graph_density":

                self.graph_density(),

            "average_degree":

                self.average_degree(),

            "average_risk":

                self.average_risk(),

        }

        save_graph_statistics(

            summary

        )

        return summary