"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Priority Ranker

==============================================================
"""

from __future__ import annotations

import pandas as pd

from config import (
    TOP_K_NODES,
)

from io_utils import (
    save_priority_ranking,
)


class PriorityRanker:
    """
    Produces the final prioritized list of attack
    graph nodes based on the computed risk scores.
    """

    def __init__(

        self,

        node_risk_dataframe,

    ):

        self.node_risk_dataframe = node_risk_dataframe.copy()

    ####################################################################
    # Assign Rank
    ####################################################################

    def assign_rank(self):

        dataframe = self.node_risk_dataframe.copy()

        dataframe = dataframe.sort_values(

            by="RiskScore",

            ascending=False,

        )

        dataframe.reset_index(

            drop=True,

            inplace=True,

        )

        dataframe.insert(

            0,

            "PriorityRank",

            range(

                1,

                len(dataframe) + 1,

            ),

        )

        return dataframe

    ####################################################################
    # Top-K Ranking
    ####################################################################

    def top_k(

        self,

        dataframe,

        k=TOP_K_NODES,

    ):

        return dataframe.head(

            k,

        ).copy()

    ####################################################################
    # High Priority Nodes
    ####################################################################

    def high_priority(

        self,

        dataframe,

        threshold=0.80,

    ):

        return dataframe[

            dataframe["RiskScore"] >= threshold

        ].copy()

    ####################################################################
    # Medium Priority Nodes
    ####################################################################

    def medium_priority(

        self,

        dataframe,

        lower=0.50,

        upper=0.80,

    ):

        return dataframe[

            (

                dataframe["RiskScore"] >= lower

            )

            &

            (

                dataframe["RiskScore"] < upper

            )

        ].copy()

    ####################################################################
    # Low Priority Nodes
    ####################################################################

    def low_priority(

        self,

        dataframe,

        threshold=0.50,

    ):

        return dataframe[

            dataframe["RiskScore"] < threshold

        ].copy()

    ####################################################################
    # Save
    ####################################################################

    def save(

        self,

        dataframe,

    ):

        save_priority_ranking(

            dataframe,

        )

    ####################################################################
    # Execute
    ####################################################################

    def run(self):

        dataframe = self.assign_rank()

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

            "total_nodes":

                len(dataframe),

            "top_k":

                len(

                    self.top_k(

                        dataframe,

                    )

                ),

            "high_priority":

                len(

                    self.high_priority(

                        dataframe,

                    )

                ),

            "medium_priority":

                len(

                    self.medium_priority(

                        dataframe,

                    )

                ),

            "low_priority":

                len(

                    self.low_priority(

                        dataframe,

                    )

                ),

        }