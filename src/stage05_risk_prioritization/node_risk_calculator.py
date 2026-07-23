"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Node Risk Calculator

==============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import (
    QUANTUM_WEIGHT,
    CVSS_WEIGHT,
    CENTRALITY_WEIGHT,
    EPSILON,
)

from io_utils import (
    save_node_risk_scores,
)


class NodeRiskCalculator:
    """
    Computes node-level risk scores by combining

    1. Quantum probability
    2. CVSS score
    3. Graph centrality
    """

    def __init__(

        self,

        graph,

        nodes,

        propagated_probability,

    ):

        self.graph = graph

        self.nodes = nodes.copy()

        self.probability = np.asarray(

            propagated_probability,

            dtype=np.float64,

        )

    ####################################################################
    # Normalization
    ####################################################################

    @staticmethod
    def normalize(values):

        values = np.asarray(

            values,

            dtype=np.float64,

        )

        minimum = np.min(values)

        maximum = np.max(values)

        return (

            values - minimum

        ) / (

            maximum - minimum + EPSILON

        )

    ####################################################################
    # Quantum Score
    ####################################################################

    def quantum_score(self):

        return self.normalize(

            self.probability,

        )

    ####################################################################
    # CVSS Score
    ####################################################################

    def cvss_score(self):

        if "cvss_score" in self.nodes.columns:

            cvss = self.nodes[

                "cvss_score"

            ].to_numpy()

        elif "cvss" in self.nodes.columns:

            cvss = self.nodes[

                "cvss"

            ].to_numpy()

        else:

            cvss = np.zeros(

                len(self.nodes)

            )

        return self.normalize(

            cvss,

        )

    ####################################################################
    # Degree Centrality
    ####################################################################

    def centrality_score(self):

        values = []

        centrality = dict(

            self.graph.degree()

        )

        for node in self.graph.nodes():

            values.append(

                centrality[node]

            )

        return self.normalize(

            values,

        )

    ####################################################################
    # Final Risk Score
    ####################################################################

    def compute(self):

        quantum = self.quantum_score()

        cvss = self.cvss_score()

        centrality = self.centrality_score()

        risk = (

            QUANTUM_WEIGHT * quantum

            +

            CVSS_WEIGHT * cvss

            +

            CENTRALITY_WEIGHT * centrality

        )

        dataframe = self.nodes.copy()

        dataframe["QuantumScore"] = quantum

        dataframe["CVSSScore"] = cvss

        dataframe["CentralityScore"] = centrality

        dataframe["RiskScore"] = risk

        dataframe = dataframe.sort_values(

            by="RiskScore",

            ascending=False,

        )

        dataframe.reset_index(

            drop=True,

            inplace=True,

        )

        return dataframe

    ####################################################################
    # Save
    ####################################################################

    def save(

        self,

        dataframe,

    ):

        save_node_risk_scores(

            dataframe,

        )

    ####################################################################
    # Execute
    ####################################################################

    def run(self):

        dataframe = self.compute()

        self.save(

            dataframe,

        )

        return dataframe

    ####################################################################
    # Summary
    ####################################################################

    def summary(

        self,

        dataframe,

    ):

        return {

            "nodes":

                len(dataframe),

            "highest_risk":

                float(

                    dataframe["RiskScore"].max()

                ),

            "lowest_risk":

                float(

                    dataframe["RiskScore"].min()

                ),

            "average_risk":

                float(

                    dataframe["RiskScore"].mean()

                ),

        }