"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Attack Path Extractor

Extracts high-risk attack paths using the
propagated hybrid quantum probabilities.

==============================================================
"""

from __future__ import annotations

import networkx as nx
import numpy as np

from io_utils import save_attack_paths


class AttackPathExtractor:
    """
    Extracts probable attack paths from the
    propagated hybrid probability distribution.
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
    # Node Score
    ####################################################################

    def node_score(
        self,
        node,
        probability,
    ):

        idx = self.node_index[node]

        return float(probability[idx])

    ####################################################################
    # Path Score
    ####################################################################

    def path_score(
        self,
        path,
        probability,
    ):

        score = 0.0

        for node in path:

            score += self.node_score(

                node,

                probability,

            )

        return score / len(path)

    ####################################################################
    # Extract Paths
    ####################################################################

    def extract(
        self,
        probability,
        max_length=5,
    ):

        probability = np.asarray(

            probability,

            dtype=np.float64,

        )

        attack_paths = []

        for source in self.nodes:

            for target in self.nodes:

                if source == target:

                    continue

                try:

                    paths = nx.all_simple_paths(

                        self.graph,

                        source,

                        target,

                        cutoff=max_length,

                    )

                    for path in paths:

                        attack_paths.append(

                            {

                                "source": source,

                                "target": target,

                                "path": path,

                                "length": len(path),

                                "score": self.path_score(

                                    path,

                                    probability,

                                ),

                            }

                        )

                except nx.NetworkXNoPath:

                    continue

        attack_paths.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        return attack_paths

    ####################################################################
    # Top-K Paths
    ####################################################################

    def top_paths(
        self,
        attack_paths,
        k=20,
    ):

        return attack_paths[:k]

    ####################################################################
    # Save
    ####################################################################

    def save(
        self,
        attack_paths,
    ):

        save_attack_paths(

            attack_paths,

        )

    ####################################################################
    # Execute
    ####################################################################

    def run(
        self,
        probability,
        max_length=5,
        top_k=20,
    ):

        paths = self.extract(

            probability,

            max_length,

        )

        paths = self.top_paths(

            paths,

            top_k,

        )

        self.save(

            paths,

        )

        return paths

    ####################################################################
    # Summary
    ####################################################################

    def summary(
        self,
        attack_paths,
    ):

        if len(attack_paths) == 0:

            return {

                "total_paths": 0,

                "best_score": 0.0,

            }

        return {

            "total_paths": len(

                attack_paths

            ),

            "best_score": float(

                attack_paths[0]["score"]

            ),

            "average_score": float(

                np.mean(

                    [

                        p["score"]

                        for p in attack_paths

                    ]

                )

            ),

        }