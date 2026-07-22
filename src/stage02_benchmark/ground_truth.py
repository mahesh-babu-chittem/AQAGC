"""
===========================================================================
AQAGC

Stage 2

Ground Truth Generator

Implements the deterministic critical attack path generation

Outputs

• Critical Paths
• Node Sequences
• Path Risk Scores
• Ground Truth CSV

===========================================================================

"""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm

class GroundTruthGenerator:

    """
    Deterministic Ground Truth Generator.

    Produces the benchmark critical attack paths
    used during evaluation.
    """

    ###################################################################

    def __init__(

        self,

        max_path_length=10,

        top_k=100,

    ):

        self.max_path_length = max_path_length

        self.top_k = top_k

    ###################################################################
    # Public API
    ###################################################################

    def generate(

        self,

        graph: nx.DiGraph,

    ):

        print("\nGenerating Ground Truth...")

        ###############################################################

        entry_nodes = self._entry_nodes(

            graph

        )

        ###############################################################

        target_nodes = self._target_nodes(

            graph

        )

        ##############################################################
# ToN-IoT scalability
##############################################################

        if graph.number_of_nodes() > 100000:

            print("\nLarge graph detected.")

            print("Reducing source/target search space...\n")

            entry_nodes = sorted(

                entry_nodes,

                key=lambda n: (

                    -graph.out_degree(n),

                    n,

                ),

            )[:25]

            target_nodes = sorted(

                target_nodes,

                key=lambda n: (

                    -graph.in_degree(n),

                    n,

                ),

            )[:200]

            print(

                f"Selected Entry Nodes : {len(entry_nodes)}"

            )

            print(

                f"Selected Target Nodes : {len(target_nodes)}"

            )

        ###############################################################

        paths = self._enumerate_paths(

            graph,

            entry_nodes,

            target_nodes,

        )

        ###############################################################

        ranked = self._rank_paths(

            graph,

            paths,

        )

        ###############################################################

        ground_truth = self._create_dataframe(

            ranked

        )

        return ground_truth
    
        ###################################################################
    # Path Risk Score
    ###################################################################

        ###################################################################
    # Entry Nodes
    ###################################################################

    def _entry_nodes(
        self,
        graph,
    ):
        """
        Determine entry nodes.

        If no node has zero in-degree, use the nodes with the
        minimum in-degree instead.
        """
        entry = [
            node
            for node in graph.nodes()
            if graph.in_degree(node) == 0
        ]
        if len(entry) > 0:
            return entry
        ########################################################
        minimum = min(
            graph.in_degree(node)
            for node in graph.nodes()
        )
        return [
            node
            for node in graph.nodes()
            if graph.in_degree(node) == minimum
        ]

    ###################################################################
    # Target Nodes
    ###################################################################

    def _target_nodes(
        self,
        graph,
    ):
        """
        Determine target nodes.

        If no node has zero out-degree, use the nodes with the
        minimum out-degree instead.
        """
        targets = [
            node
            for node in graph.nodes()
            if graph.out_degree(node) == 0
        ]
        if len(targets) > 0:
            return targets
        ########################################################
        minimum = min(
            graph.out_degree(node)
            for node in graph.nodes()
        )
        return [
            node
            for node in graph.nodes()
            if graph.out_degree(node) == minimum
        ]

    ###################################################################
    # Enumerate Candidate Paths
    ###################################################################

        ###################################################################
    # Enumerate Candidate Paths
    ###################################################################

    def _enumerate_paths(

        self,

        graph,

        entry_nodes,

        target_nodes,

    ):

        """
        Deterministically generate candidate attack paths.

        Instead of enumerating every possible simple path (which is
        computationally infeasible for dense graphs), this method keeps
        only the first few shortest simple paths for each
        source-destination pair.

        This keeps the benchmark deterministic while remaining scalable.
        """

        from itertools import islice

        paths = []

        MAX_PATHS_PER_PAIR = 20

        total_pairs = len(entry_nodes) * len(target_nodes)

        pair_counter = 0

        print(

            f"Entry Nodes  : {len(entry_nodes)}"

        )

        print(

            f"Target Nodes : {len(target_nodes)}"

        )

        print(

            f"Source-Target Pairs : {total_pairs}"

        )

        ###############################################################

        for source in tqdm(

            entry_nodes,

            desc="Enumerating Attack Paths",

        ):

            for destination in target_nodes:

                pair_counter += 1

                if source == destination:

                    continue

                try:

                    generator = nx.shortest_simple_paths(

                        graph,

                        source,

                        destination,

                    )

                    ###################################################

                    for path in islice(

                        generator,

                        MAX_PATHS_PER_PAIR,

                    ):

                        if len(path) <= self.max_path_length:

                            paths.append(path)

                except (

                    nx.NetworkXNoPath,

                    nx.NodeNotFound,

                ):

                    continue

        ###############################################################

        print(

            f"\nEnumerated {len(paths):,} candidate paths."

        )

        return paths
    
    def _path_risk_score(

        self,

        graph,

        path,

    ):

        """
        Computes the cumulative risk score of an attack path.

        The score combines

        • Node Risk Scores
        • Edge Weights

        Higher scores indicate more critical attack paths.
        """

        ###############################################################

        node_score = 0.0

        edge_score = 0.0

        ###############################################################
        # Node Contribution
        ###############################################################

        for node in path:

            attributes = graph.nodes[node]

            node_score += float(

                attributes.get(

                    "risk_score",

                    0.0,

                )

            )

        ###############################################################
        # Edge Contribution
        ###############################################################

        for source, destination in zip(

            path[:-1],

            path[1:],

        ):

            attributes = graph[source][destination]

            edge_score += float(

                attributes.get(

                    "normalized_weight",

                    attributes.get(

                        "edge_weight",

                        0.0,

                    ),

                )

            )

        ###############################################################

        return (

            node_score

            +

            edge_score

        )

    ###################################################################
    # Rank Candidate Paths
    ###################################################################

    def _rank_paths(

        self,

        graph,

        candidate_paths,

    ):

        """
        Rank candidate attack paths according to

        cumulative path risk.

        Higher risk paths receive higher priority.
        """

        ranked = []

        ###############################################################

        for path in candidate_paths:

            score = self._path_risk_score(

                graph,

                path,

            )

            ranked.append(

                {

                    "path": path,

                    "risk_score": score,

                    "path_length": len(path),

                }

            )

        ###############################################################
        # Deterministic Sorting
        ###############################################################

        ranked = sorted(

            ranked,

            key=lambda x: (

                -x["risk_score"],

                x["path_length"],

                tuple(x["path"]),

            ),

        )

        ###############################################################
        # Remove duplicate paths
        ###############################################################

        unique = []

        seen = set()

        for item in ranked:

            key = tuple(item["path"])

            if key in seen:

                continue

            seen.add(key)

            unique.append(item)

        ###############################################################
        # Keep only Top-K
        ###############################################################

        unique = unique[: self.top_k]

        print(

            f"Selected {len(unique):,} critical attack paths."

        )

        return unique
    
        ###################################################################
    # Create Ground Truth DataFrame
    ###################################################################

    def _create_dataframe(

        self,

        ranked_paths,

    ):

        """
        Converts ranked attack paths into the benchmark
        ground-truth table.
        """

        records = []

        ###############################################################

        for index, item in enumerate(

            ranked_paths,

            start=1,

        ):

            path = item["path"]

            risk = item["risk_score"]

            length = item["path_length"]

            records.append(

                {

                    "ground_truth_id": index,

                    "path_rank": index,

                    "path": "->".join(

                        map(

                            str,

                            path,

                        )

                    ),

                    "path_nodes": len(path),

                    "path_length": length,

                    "risk_score": round(

                        risk,

                        6,

                    ),

                }

            )

        ###############################################################

        dataframe = pd.DataFrame(

            records,

        )

        return dataframe

    ###################################################################
    # Validation
    ###################################################################

    def validate(

        self,

        ground_truth: pd.DataFrame,

    ):

        """
        Validate generated ground truth.
        """

        required = [

            "ground_truth_id",

            "path_rank",

            "path",

            "path_nodes",

            "path_length",

            "risk_score",

        ]

        ###############################################################

        for column in required:

            if column not in ground_truth.columns:

                raise ValueError(

                    f"Missing column '{column}'."

                )

        ###############################################################

        if len(ground_truth) == 0:

            raise ValueError(

                "Ground truth contains no paths."

            )

        ###############################################################

        if (

            ground_truth["risk_score"]

            .isna()

            .sum()

            > 0

        ):

            raise ValueError(

                "NaN values detected in risk_score."

            )

        ###############################################################

        if (

            ground_truth["path"]

            .duplicated()

            .sum()

            > 0

        ):

            raise ValueError(

                "Duplicate paths detected."

            )

        return True

    ###################################################################
    # Statistics
    ###################################################################

    def statistics(

        self,

        ground_truth,

    ):

        """
        Compute statistics of generated benchmark paths.
        """

        return {

            "critical_paths":

                len(

                    ground_truth

                ),

            "average_path_length":

                float(

                    ground_truth[

                        "path_length"

                    ].mean()

                ),

            "maximum_path_length":

                int(

                    ground_truth[

                        "path_length"

                    ].max()

                ),

            "minimum_path_length":

                int(

                    ground_truth[

                        "path_length"

                    ].min()

                ),

            "average_risk":

                float(

                    ground_truth[

                        "risk_score"

                    ].mean()

                ),

            "maximum_risk":

                float(

                    ground_truth[

                        "risk_score"

                    ].max()

                ),

            "minimum_risk":

                float(

                    ground_truth[

                        "risk_score"

                    ].min()

                ),

        }

    ###################################################################
    # Top Critical Paths
    ###################################################################

    def top_paths(

        self,

        ground_truth,

        k=10,

    ):

        """
        Return the highest-ranked attack paths.
        """

        return (

            ground_truth

            .sort_values(

                by=[

                    "risk_score",

                    "path_rank",

                ],

                ascending=[

                    False,

                    True,

                ],

            )

            .head(k)

            .reset_index(

                drop=True,

            )

        )
    
        ###################################################################
    # Export Ground Truth
    ###################################################################

    def export(

        self,

        ground_truth: pd.DataFrame,

        output_file,

    ):

        """
        Export generated benchmark ground truth.
        """

        ground_truth.to_csv(

            output_file,

            index=False,

        )

        print(

            f"Saved ground truth -> {output_file}"

        )

    ###################################################################
    # Update Configuration
    ###################################################################

    def update_configuration(

        self,

        max_path_length=None,

        top_k=None,

    ):

        """
        Update Ground Truth Generator parameters.
        """

        if max_path_length is not None:

            if max_path_length <= 0:

                raise ValueError(

                    "max_path_length must be positive."

                )

            self.max_path_length = int(

                max_path_length

            )

        ###############################################################

        if top_k is not None:

            if top_k <= 0:

                raise ValueError(

                    "top_k must be positive."

                )

            self.top_k = int(

                top_k

            )

    ###################################################################
    # Summary
    ###################################################################

    def summary(

        self,

        ground_truth,

    ):

        """
        Print benchmark summary.
        """

        stats = self.statistics(

            ground_truth,

        )

        print("\n")

        print("=" * 70)

        print("GROUND TRUTH SUMMARY")

        print("=" * 70)

        print(

            f"Critical Paths      : {stats['critical_paths']}"

        )

        print(

            f"Average Length      : {stats['average_path_length']:.2f}"

        )

        print(

            f"Maximum Length      : {stats['maximum_path_length']}"

        )

        print(

            f"Minimum Length      : {stats['minimum_path_length']}"

        )

        print(

            f"Average Risk        : {stats['average_risk']:.4f}"

        )

        print(

            f"Maximum Risk        : {stats['maximum_risk']:.4f}"

        )

        print(

            f"Minimum Risk        : {stats['minimum_risk']:.4f}"

        )

        print("=" * 70)

    ###################################################################
    # Reset
    ###################################################################

    def reset(self):

        """
        Restore default parameters.
        """

        self.max_path_length = 10

        self.top_k = 100

    ###################################################################
    # Future Extension
    ###################################################################

    def generate_probabilistic(

        self,

        graph,

    ):

        """
        Placeholder for future probabilistic ground-truth generation.

        The Scientific Reports version of AQAGC uses deterministic
        critical-path generation. Future versions may support
        probabilistic attack progression or Monte Carlo sampling.
        """

        raise NotImplementedError(

            "Probabilistic ground-truth generation "

            "is not implemented."

        )

    ###################################################################
    # Representation
    ###################################################################

    def __repr__(self):

        return (

            "GroundTruthGenerator("

            f"max_path_length={self.max_path_length}, "

            f"top_k={self.top_k}"

            ")"

        )