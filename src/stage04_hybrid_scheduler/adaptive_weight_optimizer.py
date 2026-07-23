"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Adaptive Weight Optimizer

Computes adaptive fusion weights

    Hybrid = ω1·DTQW + ω2·CTQW

==============================================================
"""

from __future__ import annotations

import numpy as np

from config import OMEGA1, OMEGA2


class AdaptiveWeightOptimizer:
    """
    Computes adaptive fusion weights for
    DTQW and CTQW.
    """

    def __init__(

        self,

        default_dtqw=OMEGA1,

        default_ctqw=OMEGA2,

    ):

        self.default_dtqw = float(default_dtqw)

        self.default_ctqw = float(default_ctqw)

    ####################################################################
    # Normalize
    ####################################################################

    @staticmethod
    def normalize(

        dtqw_weight,

        ctqw_weight,

    ):

        total = dtqw_weight + ctqw_weight

        if total <= 0:

            return 0.5, 0.5

        return (

            dtqw_weight / total,

            ctqw_weight / total,

        )

    ####################################################################
    # Entropy
    ####################################################################

    @staticmethod
    def entropy(

        probability,

    ):

        probability = np.asarray(

            probability,

            dtype=np.float64,

        )

        probability = probability + 1e-12

        probability /= probability.sum()

        return float(

            -np.sum(

                probability *

                np.log(probability)

            )

        )

    ####################################################################
    # State Confidence
    ####################################################################

    @staticmethod
    def confidence(

        probability,

    ):

        probability = np.asarray(

            probability,

            dtype=np.float64,

        )

        return float(

            np.max(

                probability

            )

        )

    ####################################################################
    # Adaptive Weights
    ####################################################################

    def optimize(

        self,

        dtqw_probability,

        ctqw_probability,

    ):

        dtqw_conf = self.confidence(

            dtqw_probability,

        )

        ctqw_conf = self.confidence(

            ctqw_probability,

        )

        return self.normalize(

            dtqw_conf,

            ctqw_conf,

        )

    ####################################################################
    # Entropy-Based Weights
    ####################################################################

    def optimize_entropy(

        self,

        dtqw_probability,

        ctqw_probability,

    ):

        dtqw_entropy = self.entropy(

            dtqw_probability,

        )

        ctqw_entropy = self.entropy(

            ctqw_probability,

        )

        dtqw_score = 1.0 / (

            dtqw_entropy + 1e-12

        )

        ctqw_score = 1.0 / (

            ctqw_entropy + 1e-12

        )

        return self.normalize(

            dtqw_score,

            ctqw_score,

        )

    ####################################################################
    # Fixed Weights
    ####################################################################

    def default_weights(self):

        return self.normalize(

            self.default_dtqw,

            self.default_ctqw,

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(

        self,

        dtqw_probability,

        ctqw_probability,

    ):

        omega1, omega2 = self.optimize(

            dtqw_probability,

            ctqw_probability,

        )

        return {

            "dtqw_weight": omega1,

            "ctqw_weight": omega2,

            "weight_sum": omega1 + omega2,

        }