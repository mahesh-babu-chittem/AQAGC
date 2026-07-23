"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Risk Summary Generator

==============================================================
"""

from __future__ import annotations

import numpy as np

from io_utils import (
    save_risk_summary,
)


class RiskSummary:
    """
    Generates a statistical summary of the
    Stage-05 risk prioritization results.
    """

    def __init__(

        self,

        node_risk_dataframe,

        edge_risk_dataframe,

        path_risk_dataframe,

        critical_assets_dataframe,

    ):

        self.node_df = node_risk_dataframe

        self.edge_df = edge_risk_dataframe

        self.path_df = path_risk_dataframe

        self.asset_df = critical_assets_dataframe

    ####################################################################
    # Node Statistics
    ####################################################################

    def node_statistics(self):

        return {

            "count": int(

                len(self.node_df)

            ),

            "maximum_risk": float(

                self.node_df["RiskScore"].max()

            ),

            "minimum_risk": float(

                self.node_df["RiskScore"].min()

            ),

            "average_risk": float(

                self.node_df["RiskScore"].mean()

            ),

            "std_risk": float(

                self.node_df["RiskScore"].std()

            ),

        }

    ####################################################################
    # Edge Statistics
    ####################################################################

    def edge_statistics(self):

        return {

            "count": int(

                len(self.edge_df)

            ),

            "maximum_risk": float(

                self.edge_df["RiskScore"].max()

            ),

            "minimum_risk": float(

                self.edge_df["RiskScore"].min()

            ),

            "average_risk": float(

                self.edge_df["RiskScore"].mean()

            ),

            "std_risk": float(

                self.edge_df["RiskScore"].std()

            ),

        }

    ####################################################################
    # Path Statistics
    ####################################################################

    def path_statistics(self):

        return {

            "count": int(

                len(self.path_df)

            ),

            "maximum_risk": float(

                self.path_df["RiskScore"].max()

            ),

            "minimum_risk": float(

                self.path_df["RiskScore"].min()

            ),

            "average_risk": float(

                self.path_df["RiskScore"].mean()

            ),

            "std_risk": float(

                self.path_df["RiskScore"].std()

            ),

        }

    ####################################################################
    # Critical Asset Statistics
    ####################################################################

    def asset_statistics(self):

        if len(self.asset_df) == 0:

            return {

                "count": 0,

            }

        return {

            "count": int(

                len(self.asset_df)

            ),

            "maximum_risk": float(

                self.asset_df["RiskScore"].max()

            ),

            "minimum_risk": float(

                self.asset_df["RiskScore"].min()

            ),

            "average_risk": float(

                self.asset_df["RiskScore"].mean()

            ),

        }

    ####################################################################
    # Complete Summary
    ####################################################################

    def generate(self):

        summary = {

            "node_statistics":

                self.node_statistics(),

            "edge_statistics":

                self.edge_statistics(),

            "path_statistics":

                self.path_statistics(),

            "critical_assets":

                self.asset_statistics(),

        }

        return summary

    ####################################################################
    # Save
    ####################################################################

    def save(

        self,

        summary,

    ):

        save_risk_summary(

            summary,

        )

    ####################################################################
    # Execute
    ####################################################################

    def run(self):

        summary = self.generate()

        self.save(

            summary,

        )

        return summary