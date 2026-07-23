"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Critical Asset Identifier

==============================================================
"""

from __future__ import annotations

import pandas as pd

from config import (
    TOP_K_ASSETS,
    HIGH_RISK_THRESHOLD,
)

from io_utils import (
    save_critical_assets,
)


class CriticalAssetIdentifier:
    """
    Identifies critical assets from the
    prioritized node risk scores.
    """

    def __init__(

        self,

        node_risk_dataframe,

    ):

        self.node_risk_dataframe = node_risk_dataframe.copy()

    ####################################################################
    # Critical Assets
    ####################################################################

    def identify(

        self,

        threshold=HIGH_RISK_THRESHOLD,

    ):

        dataframe = self.node_risk_dataframe.copy()

        critical = dataframe[

            dataframe["RiskScore"] >= threshold

        ].copy()

        critical = critical.sort_values(

            by="RiskScore",

            ascending=False,

        )

        critical.reset_index(

            drop=True,

            inplace=True,

        )

        return critical

    ####################################################################
    # Top-K Assets
    ####################################################################

    def top_assets(

        self,

        dataframe,

        k=TOP_K_ASSETS,

    ):

        return dataframe.head(

            k,

        ).copy()

    ####################################################################
    # Asset Categories
    ####################################################################

    def assign_category(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        dataframe["Category"] = "Critical"

        return dataframe

    ####################################################################
    # Save
    ####################################################################

    def save(

        self,

        dataframe,

    ):

        save_critical_assets(

            dataframe,

        )

    ####################################################################
    # Execute
    ####################################################################

    def run(self):

        dataframe = self.identify()

        dataframe = self.assign_category(

            dataframe,

        )

        dataframe = self.top_assets(

            dataframe,

        )

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

            "critical_assets":

                len(

                    dataframe,

                ),

            "highest_risk":

                float(

                    dataframe["RiskScore"].max()

                ) if len(dataframe) else 0.0,

            "lowest_risk":

                float(

                    dataframe["RiskScore"].min()

                ) if len(dataframe) else 0.0,

            "average_risk":

                float(

                    dataframe["RiskScore"].mean()

                ) if len(dataframe) else 0.0,

        }