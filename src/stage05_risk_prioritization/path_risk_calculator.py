"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Attack Path Risk Calculator

==============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import (
    PATH_WEIGHT,
    EPSILON,
)

from io_utils import (
    save_path_risk_scores,
)


class PathRiskCalculator:
    """
    Computes risk scores for attack paths generated
    during Stage-04.
    """

    def __init__(

        self,

        attack_paths,

        node_risk_dataframe,

    ):

        self.attack_paths = attack_paths

        self.node_risk_dataframe = node_risk_dataframe.copy()

        self.node_lookup = self._build_lookup()

    ####################################################################
    # Build Lookup
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
    # Path Risk
    ####################################################################

    def compute_path_score(

        self,

        path,

    ):

        if len(path) == 0:

            return 0.0

        scores = [

            self.node_lookup.get(

                node,

                0.0,

            )

            for node in path

        ]

        return float(

            np.mean(

                scores

            )

        )

    ####################################################################
    # Compute
    ####################################################################

    def compute(self):

        records = []

        scores = []

        for item in self.attack_paths:

            score = self.compute_path_score(

                item["path"]

            )

            scores.append(

                score

            )

        normalized_scores = self.normalize(

            scores

        )

        for index, item in enumerate(

            self.attack_paths

        ):

            path = item["path"]

            length = len(path)

            final_score = (

                (1.0 - PATH_WEIGHT)

                * normalized_scores[index]

                +

                PATH_WEIGHT

                * (

                    1.0 /

                    max(length, 1)

                )

            )

            records.append(

                {

                    "Source":

                        item.get(

                            "source"

                        ),

                    "Target":

                        item.get(

                            "target"

                        ),

                    "Path":

                        " -> ".join(

                            map(

                                str,

                                path,

                            )

                        ),

                    "Length":

                        length,

                    "RiskScore":

                        final_score,

                }

            )

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

        save_path_risk_scores(

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

            "paths":

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