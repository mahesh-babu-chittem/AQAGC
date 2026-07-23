"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Ranking and Attribution Metrics

==============================================================
"""

from __future__ import annotations

import numpy as np

import pandas as pd



class RankingMetrics:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        predicted_ranking,

        ground_truth,

        k=10,

    ):

        self.predicted_ranking = list(

            predicted_ranking

        )

        self.ground_truth = set(

            ground_truth

        )

        self.k = k



    ####################################################################
    # Precision @ K
    ####################################################################

    def precision_at_k(self):

        top_k = set(

            self.predicted_ranking[:self.k]

        )


        if len(top_k) == 0:

            return 0.0


        return len(

            top_k.intersection(

                self.ground_truth

            )

        ) / self.k



    ####################################################################
    # Recall @ K
    ####################################################################

    def recall_at_k(self):

        if len(self.ground_truth) == 0:

            return 0.0


        top_k = set(

            self.predicted_ranking[:self.k]

        )


        return len(

            top_k.intersection(

                self.ground_truth

            )

        ) / len(

            self.ground_truth

        )



    ####################################################################
    # F1 @ K
    ####################################################################

    def f1_at_k(self):

        precision = self.precision_at_k()

        recall = self.recall_at_k()


        if precision + recall == 0:

            return 0.0


        return (

            2 *

            precision *

            recall

        ) / (

            precision +

            recall

        )



    ####################################################################
    # Mean Average Precision
    ####################################################################

    def mean_average_precision(self):

        hits = 0

        precision_sum = 0.0


        for index, item in enumerate(

            self.predicted_ranking,

            start=1

        ):

            if item in self.ground_truth:

                hits += 1

                precision_sum += hits / index



        if len(self.ground_truth) == 0:

            return 0.0


        return precision_sum / len(

            self.ground_truth

        )



    ####################################################################
    # NDCG @ K
    ####################################################################

    def ndcg_at_k(self):

        relevance = [

            1 if item in self.ground_truth else 0

            for item in self.predicted_ranking[:self.k]

        ]


        dcg = sum(

            rel /

            np.log2(index + 2)

            for index, rel in enumerate(

                relevance

            )

        )


        ideal = sorted(

            relevance,

            reverse=True

        )


        idcg = sum(

            rel /

            np.log2(index + 2)

            for index, rel in enumerate(

                ideal

            )

        )


        if idcg == 0:

            return 0.0


        return dcg / idcg



    ####################################################################
    # Critical Path Coverage
    ####################################################################

    def critical_path_coverage(self):

        top_k = set(

            self.predicted_ranking[:self.k]

        )


        if len(self.ground_truth) == 0:

            return 0.0


        return len(

            top_k.intersection(

                self.ground_truth

            )

        ) / len(

            self.ground_truth

        )



    ####################################################################
    # Attribution Metrics
    ####################################################################

    def attack_path_relevance_score(

        self,

        relevance_scores,

    ):

        """

        APRS

        Measures relevance of discovered
        attack paths.

        """

        if len(relevance_scores) == 0:

            return 0.0


        return float(

            np.mean(

                relevance_scores

            )

        )



    def node_attribution_score(

        self,

        node_scores,

    ):

        """

        NAS

        """

        if len(node_scores) == 0:

            return 0.0


        return float(

            np.mean(

                node_scores

            )

        )



    def edge_attribution_score(

        self,

        edge_scores,

    ):

        """

        EAS

        """

        if len(edge_scores) == 0:

            return 0.0


        return float(

            np.mean(

                edge_scores

            )

        )



    def path_attribution_score(

        self,

        path_scores,

    ):

        """

        PAS

        """

        if len(path_scores) == 0:

            return 0.0


        return float(

            np.mean(

                path_scores

            )

        )



    ####################################################################
    # Quantum Metrics
    ####################################################################

    def amplitude_concentration_score(

        self,

        amplitudes,

    ):

        """

        ACS

        """

        probabilities = np.abs(

            amplitudes

        ) ** 2


        if probabilities.sum() == 0:

            return 0.0


        return float(

            np.max(

                probabilities

            )

            /

            probabilities.sum()

        )



    def risk_concentration_index(

        self,

        risk_scores,

    ):

        """

        RCI

        """

        total = sum(

            risk_scores

        )


        if total == 0:

            return 0.0


        return float(

            max(

                risk_scores

            )

            /

            total

        )



    ####################################################################
    # Complete Metric Report
    ####################################################################

    def calculate_all(

        self,

        relevance_scores=None,

        node_scores=None,

        edge_scores=None,

        path_scores=None,

        amplitudes=None,

        risk_scores=None,

    ):


        results = {


            "Precision@K":

                self.precision_at_k(),


            "Recall@K":

                self.recall_at_k(),


            "F1@K":

                self.f1_at_k(),


            "MAP":

                self.mean_average_precision(),


            "NDCG@K":

                self.ndcg_at_k(),


            "CPC@K":

                self.critical_path_coverage(),

        }


        if relevance_scores is not None:

            results["APRS"] = (

                self.attack_path_relevance_score(

                    relevance_scores

                )

            )


        if node_scores is not None:

            results["NAS"] = (

                self.node_attribution_score(

                    node_scores

                )

            )


        if edge_scores is not None:

            results["EAS"] = (

                self.edge_attribution_score(

                    edge_scores

                )

            )


        if path_scores is not None:

            results["PAS"] = (

                self.path_attribution_score(

                    path_scores

                )

            )


        if amplitudes is not None:

            results["ACS"] = (

                self.amplitude_concentration_score(

                    amplitudes

                )

            )


        if risk_scores is not None:

            results["RCI"] = (

                self.risk_concentration_index(

                    risk_scores

                )

            )


        return results



    ####################################################################
    # DataFrame Output
    ####################################################################

    def dataframe(self, **kwargs):

        return pd.DataFrame(

            [

                self.calculate_all(

                    **kwargs

                )

            ]

        )