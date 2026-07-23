"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Probability Propagator

Propagates hybrid quantum probabilities over
the attack graph.

==============================================================
"""

from __future__ import annotations

import numpy as np
import networkx as nx

from io_utils import (
    save_propagated_risk,
)


class ProbabilityPropagator:
    """
    Propagates hybrid quantum probabilities
    throughout the attack graph.
    """

    def __init__(

        self,

        graph: nx.Graph,

    ):

        self.graph = graph

        self.nodes = list(graph.nodes())

        self.node_index = {

            node: idx

            for idx, node in enumerate(self.nodes)

        }

    ####################################################################
    # Normalize
    ####################################################################

    @staticmethod
    def normalize(

        probability,

    ):

        probability = np.asarray(

            probability,

            dtype=np.float64,

        )

        total = probability.sum()

        if total > 0:

            probability /= total

        return probability

    ####################################################################
    # Single Propagation
    ####################################################################

    def propagate_once(

        self,

        probability,

    ):

        probability = self.normalize(

            probability,

        )

        propagated = np.zeros_like(

            probability,

        )

        for node in self.nodes:

            idx = self.node_index[node]

            neighbors = list(

                self.graph.neighbors(node)

            )

            if len(neighbors) == 0:

                propagated[idx] += probability[idx]

                continue

            share = probability[idx] / len(neighbors)

            for neighbor in neighbors:

                neighbor_idx = self.node_index[neighbor]

                propagated[neighbor_idx] += share

        return self.normalize(

            propagated,

        )

    ####################################################################
    # Multi-Step Propagation
    ####################################################################

    def propagate(

        self,

        probability,

        iterations=5,

    ):

        propagated = np.asarray(

            probability,

            dtype=np.float64,

        )

        for _ in range(iterations):

            propagated = self.propagate_once(

                propagated,

            )

        return propagated

    ####################################################################
    # Save Results
    ####################################################################

    def save(

        self,

        propagated_probability,

    ):

        save_propagated_risk(

            propagated_probability,

        )

    ####################################################################
    # Top Ranked Nodes
    ####################################################################

    def top_nodes(

        self,

        propagated_probability,

        k=10,

    ):

        propagated_probability = self.normalize(

            propagated_probability,

        )

        ranking = np.argsort(

            propagated_probability

        )[::-1]

        results = []

        for idx in ranking[:k]:

            results.append(

                {

                    "node": self.nodes[idx],

                    "score": float(

                        propagated_probability[idx]

                    ),

                }

            )

        return results

    ####################################################################
    # Execute
    ####################################################################

    def run(

        self,

        hybrid_probability,

        iterations=5,

    ):

        propagated = self.propagate(

            hybrid_probability,

            iterations,

        )

        self.save(

            propagated,

        )

        return propagated

    ####################################################################
    # Summary
    ####################################################################

    def summary(

        self,

        propagated_probability,

    ):

        propagated_probability = self.normalize(

            propagated_probability,

        )

        return {

            "num_nodes": len(self.nodes),

            "probability_sum": float(

                propagated_probability.sum()

            ),

            "maximum_probability": float(

                propagated_probability.max()

            ),

            "minimum_probability": float(

                propagated_probability.min()

            ),

            "mean_probability": float(

                propagated_probability.mean()

            ),

        }