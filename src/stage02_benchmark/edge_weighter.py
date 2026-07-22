"""
===========================================================================
AQAGC
Adaptive Quantum Attack Graph Compiler

Stage 2

Edge Weight Assignment

===========================================================================

"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

import numpy as np


###########################################################################
# Configuration
###########################################################################

@dataclass

class WeightConfiguration:

    alpha: float = 0.35

    beta: float = 0.30

    gamma: float = 0.20

    delta: float = 0.15


###########################################################################
# Edge Weighter
###########################################################################

class EdgeWeighter:

    """
    Computes edge weights for the AQAGC benchmark.

    Every edge weight is derived from the destination node
    vulnerability attributes.

    Implements Equation (43).
    """

    #######################################################################

    def __init__(

        self,

        config: WeightConfiguration = WeightConfiguration(),

    ):

        self.config = config

        self._validate_coefficients()

    #######################################################################

    def _validate_coefficients(self):

        total = (

            self.config.alpha

            +

            self.config.beta

            +

            self.config.gamma

            +

            self.config.delta

        )

        if abs(total - 1.0) > 1e-8:

            raise ValueError(

                "Equation (44) violated. "

                "alpha + beta + gamma + delta must equal 1."

            )

    #######################################################################
    # Public API
    #######################################################################

    def assign(

        self,

        nodes: pd.DataFrame,

        edges: pd.DataFrame,

    ):

        """
        Assign edge weights.
        """

        print("\nAssigning Edge Weights...")

        ###################################################################

        lookup = (

            nodes

            .set_index(

                "node_id"

            )

            .to_dict(

                orient="index"

            )

        )

        ###################################################################

        edge_weights = []

        normalized_weights = []

        destination_risk = []

        ###################################################################

        for _, edge in edges.iterrows():

            destination = edge["destination"]

            ###############################################################

            if destination not in lookup:

                edge_weights.append(0.0)

                normalized_weights.append(0.0)

                destination_risk.append(0.0)

                continue

            ###############################################################

            node = lookup[destination]

            weight = self._compute_weight(

                node,

            )

            edge_weights.append(weight)

            destination_risk.append(

                node["risk_score"]

            )

        ###################################################################

        maximum = max(edge_weights)

        minimum = min(edge_weights)

        if maximum == minimum:

            normalized_weights = [

                1.0

                for _ in edge_weights

            ]

        else:

            normalized_weights = [

                (

                    w

                    - minimum

                )

                /

                (

                    maximum

                    - minimum

                )

                for w in edge_weights

            ]

        ###################################################################

        edges["edge_weight"] = np.round(

            edge_weights,

            6,

        )

        edges["normalized_weight"] = np.round(

            normalized_weights,

            6,

        )

        edges["destination_risk"] = np.round(

            destination_risk,

            6,

        )

        return edges
    
        #######################################################################
    # Equation (43)
    #######################################################################

    def _compute_weight(

        self,

        node,

    ):

        """
        Computes

        W(u,v)

        = αS + βE + γP + δF

        where

        S = Severity

        E = Exploitability

        P = Privilege

        F = Communication Frequency
        """

        severity = float(

            node.get(

                "severity",

                0.0,

            )

        )

        exploitability = float(

            node.get(

                "exploitability",

                0.0,

            )

        )

        privilege = float(

            node.get(

                "privilege",

                0.0,

            )

        )

        communication = float(

            node.get(

                "communication_frequency",

                0.0,

            )

        )

        ###############################################################

        weight = (

            self.config.alpha

            * severity

            +

            self.config.beta

            * exploitability

            +

            self.config.gamma

            * privilege

            +

            self.config.delta

            * communication

        )

        return float(weight)

    #######################################################################
    # Weight Validation
    #######################################################################

    def validate(

        self,

        edges: pd.DataFrame,

    ):

        """
        Validate edge weights.
        """

        required = [

            "edge_weight",

            "normalized_weight",

            "destination_risk",

        ]

        for column in required:

            if column not in edges.columns:

                raise ValueError(

                    f"Missing required column '{column}'."

                )

        ###############################################################

        if (

            edges["normalized_weight"].min() < 0

            or

            edges["normalized_weight"].max() > 1

        ):

            raise ValueError(

                "Normalized edge weights must lie within [0,1]."

            )

        ###############################################################

        if (

            edges["edge_weight"].isna().sum()

            > 0

        ):

            raise ValueError(

                "NaN edge weights detected."

            )

        return True

    #######################################################################
    # Weight Statistics
    #######################################################################

    def statistics(

        self,

        edges: pd.DataFrame,

    ):

        """
        Compute edge weight statistics.
        """

        return {

            "edges":

                len(edges),

            "minimum":

                float(

                    edges["edge_weight"].min()

                ),

            "maximum":

                float(

                    edges["edge_weight"].max()

                ),

            "mean":

                float(

                    edges["edge_weight"].mean()

                ),

            "median":

                float(

                    edges["edge_weight"].median()

                ),

            "std":

                float(

                    edges["edge_weight"].std()

                ),

            "normalized_mean":

                float(

                    edges["normalized_weight"].mean()

                ),

        }

    #######################################################################
    # Top Weighted Edges
    #######################################################################

    def top_edges(

        self,

        edges: pd.DataFrame,

        k=20,

    ):

        """
        Return the top-k highest weighted edges.
        """

        return (

            edges

            .sort_values(

                by="edge_weight",

                ascending=False,

            )

            .head(k)

            .reset_index(drop=True)

        )
    
        #######################################################################
    # Update Coefficients
    #######################################################################

    def update_configuration(

        self,

        alpha=None,

        beta=None,

        gamma=None,

        delta=None,

    ):

        """
        Update Equation (43) coefficients.
        """

        if alpha is not None:

            self.config.alpha = alpha

        if beta is not None:

            self.config.beta = beta

        if gamma is not None:

            self.config.gamma = gamma

        if delta is not None:

            self.config.delta = delta

        self._validate_coefficients()

    #######################################################################
    # Export Edge Weights
    #######################################################################

    def export(

        self,

        edges: pd.DataFrame,

        output_file,

    ):

        """
        Export weighted edge table.
        """

        edges.to_csv(

            output_file,

            index=False,

        )

        print(

            f"Saved weighted edges -> {output_file}"

        )

    #######################################################################
    # Dataset-wise Statistics
    #######################################################################

    def dataset_statistics(

        self,

        edges: pd.DataFrame,

    ):

        """
        Compute statistics for every dataset separately.
        """

        if "dataset" not in edges.columns:

            return pd.DataFrame()

        return (

            edges

            .groupby("dataset")

            .agg(

                {

                    "edge_weight": [

                        "count",

                        "mean",

                        "std",

                        "min",

                        "max",

                    ],

                    "normalized_weight": [

                        "mean",

                        "std",

                    ],

                }

            )

        )

    #######################################################################
    # Weight Distribution
    #######################################################################

    def weight_distribution(

        self,

        edges: pd.DataFrame,

    ):

        """
        Summary of edge weight distribution.
        """

        weights = edges["edge_weight"]

        return {

            "minimum": float(weights.min()),

            "q1": float(weights.quantile(0.25)),

            "median": float(weights.median()),

            "q3": float(weights.quantile(0.75)),

            "maximum": float(weights.max()),

            "variance": float(weights.var()),

            "std": float(weights.std()),

            "mean": float(weights.mean()),

        }

    #######################################################################
    # Risk-weight Correlation
    #######################################################################

    def correlation(

        self,

        edges: pd.DataFrame,

    ):

        """
        Pearson correlation between destination risk
        and computed edge weight.
        """

        if len(edges) < 2:

            return 0.0

        return float(

            edges["edge_weight"].corr(

                edges["destination_risk"]

            )

        )

    #######################################################################
    # Highest Risk Edges
    #######################################################################

    def highest_risk_edges(

        self,

        edges: pd.DataFrame,

        k=25,

    ):

        """
        Returns highest weighted edges.
        """

        return (

            edges

            .sort_values(

                by=[

                    "edge_weight",

                    "destination_risk",

                ],

                ascending=False,

            )

            .head(k)

            .reset_index(drop=True)

        )

    #######################################################################
    # Edge Type Statistics
    #######################################################################

    def edge_type_statistics(

        self,

        edges: pd.DataFrame,

    ):

        """
        Statistics grouped by edge type.
        """

        if "edge_type" not in edges.columns:

            return pd.DataFrame()

        return (

            edges

            .groupby(

                "edge_type"

            )

            .agg(

                {

                    "edge_weight": [

                        "count",

                        "mean",

                        "std",

                        "max",

                    ],

                    "normalized_weight": "mean",

                }

            )

        )
    
        #######################################################################
    # Reset Configuration
    #######################################################################

    def reset(self):
        """
        Restore default AQAGC weighting coefficients.
        """

        self.config = WeightConfiguration()

        self._validate_coefficients()

    #######################################################################
    # Edge Ranking
    #######################################################################

    def rank_edges(
        self,
        edges: pd.DataFrame,
    ):
        """
        Assign deterministic ranks based on edge weight.
        """

        ranked = edges.sort_values(
            by=[
                "edge_weight",
                "destination_risk",
            ],
            ascending=False,
        ).reset_index(drop=True)

        ranked["edge_rank"] = ranked.index + 1

        return ranked

    #######################################################################
    # Normalize Existing Edge Weights
    #######################################################################

    def normalize_weights(
        self,
        edges: pd.DataFrame,
    ):

        weights = edges["edge_weight"].astype(float)

        minimum = weights.min()

        maximum = weights.max()

        if maximum == minimum:

            edges["normalized_weight"] = 1.0

            return edges

        edges["normalized_weight"] = (

            weights - minimum

        ) / (

            maximum - minimum

        )

        return edges

    #######################################################################
    # Weight Matrix
    #######################################################################

    def weight_matrix(
        self,
        edges: pd.DataFrame,
    ):
        """
        Returns a sparse edge-weight dictionary.

        {(u,v): weight}
        """

        matrix = {}

        for _, edge in edges.iterrows():

            matrix[

                (

                    int(edge["source"]),

                    int(edge["destination"]),

                )

            ] = float(

                edge["normalized_weight"]

            )

        return matrix

    #######################################################################
    # Future Extension Hook
    #######################################################################

    def assign_learned_weights(
        self,
        nodes,
        edges,
        model=None,
    ):
        """
        Placeholder for future learning-based edge weighting.

        The AQAGC manuscript uses deterministic edge weights
        computed from Equation (43).

        Future work may replace these with
        graph neural network or reinforcement-learning
        based edge estimators.
        """

        raise NotImplementedError(

            "Learning-based edge weighting "

            "is not implemented."

        )

    #######################################################################
    # String Representation
    #######################################################################

    def __repr__(self):

        return (

            "EdgeWeighter("

            f"alpha={self.config.alpha}, "

            f"beta={self.config.beta}, "

            f"gamma={self.config.gamma}, "

            f"delta={self.config.delta}"

            ")"

        )