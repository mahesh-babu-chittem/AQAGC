"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Edge Risk Calculator

==============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import (
    EPSILON,
)

from io_utils import (
    save_edge_risk_scores,
)


class EdgeRiskCalculator:
    """
    Computes edge-level risk scores using

    1. Source node risk
    2. Destination node risk
    3. Edge betweenness centrality
    """

    def __init__(

        self,

        graph,

        node_risk_dataframe,

    ):

        self.graph = graph

        self.node_risk_dataframe = node_risk_dataframe.copy()

        self.node_scores = self._build_lookup()

    ####################################################################
    # Build Lookup Table
    ####################################################################

    def _build_lookup(self):

        lookup = {}

        node_column = self.node_risk_dataframe.columns[0]

        for _, row in self.node_risk_dataframe.iterrows():

            lookup[row[node_column]] = row["RiskScore"]

        return lookup

    ####################################################################
    # Normalize
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
    # Edge Betweenness
    ####################################################################

    def edge_centrality(self):

        return dict(

            __import__(

                "networkx"

            ).edge_betweenness_centrality(

                self.graph,

                normalized=True,

            )

        )

    ####################################################################
    # Compute
    ####################################################################

    def compute(self):

        centrality = self.edge_centrality()

        records = []

        centrality_values = []

        for edge in self.graph.edges():

            centrality_values.append(

                centrality.get(

                    edge,

                    0.0,

                )

            )

        normalized_centrality = self.normalize(

            centrality_values,

        )

        index = 0

        for edge in self.graph.edges():

            source, target = edge

            source_score = self.node_scores.get(

                source,

                0.0,

            )

            target_score = self.node_scores.get(

                target,

                0.0,

            )

            edge_score = (

                source_score

                +

                target_score

            ) / 2.0

            final_score = (

                0.8 * edge_score

                +

                0.2 * normalized_centrality[index]

            )

            records.append(

                {

                    "Source": source,

                    "Target": target,

                    "SourceRisk": source_score,

                    "TargetRisk": target_score,

                    "EdgeCentrality": normalized_centrality[index],

                    "RiskScore": final_score,

                }

            )

            index += 1

        dataframe = pd.DataFrame(

            records,

        )

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

        save_edge_risk_scores(

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

            "edges":

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