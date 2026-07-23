"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Hybrid Quantum Scheduler

Implements

    Hybrid_State =
        ω1 × DTQW_State +
        ω2 × CTQW_State

==============================================================
"""

from __future__ import annotations

import numpy as np

from config import (
    OMEGA1,
    OMEGA2,
    DTQW_STEPS,
    CTQW_STEPS,
    CTQW_TIME_STEP,
)

from dtqw_walk import DTQWWalk
from ctqw_walk import CTQWWalk

from io_utils import (
    save_hybrid_state,
)


class HybridScheduler:
    """
    Adaptive Hybrid DTQW–CTQW Scheduler.
    """

    def __init__(

        self,

        number_of_nodes,

        omega1=OMEGA1,

        omega2=OMEGA2,

    ):

        self.number_of_nodes = int(number_of_nodes)

        self.omega1 = float(omega1)

        self.omega2 = float(omega2)

        self.dtqw = DTQWWalk(

            number_of_nodes=self.number_of_nodes,

        )

        self.ctqw = CTQWWalk()

    ####################################################################
    # Normalize Weights
    ####################################################################

    def normalize_weights(self):

        total = self.omega1 + self.omega2

        if total == 0:

            self.omega1 = 0.5
            self.omega2 = 0.5

        else:

            self.omega1 /= total
            self.omega2 /= total

    ####################################################################
    # DTQW State
    ####################################################################

    def run_dtqw(self):

        return self.dtqw.final_state(

            steps=DTQW_STEPS,

        )

    ####################################################################
    # CTQW State
    ####################################################################

    def run_ctqw(self):

        return self.ctqw.final_state(

            steps=CTQW_STEPS,

            delta_time=CTQW_TIME_STEP,

        )

    ####################################################################
    # Hybrid Fusion
    ####################################################################

    def fuse(

        self,

        dtqw_state,

        ctqw_state,

    ):

        self.normalize_weights()

        hybrid = (

            self.omega1 * dtqw_state

            +

            self.omega2 * ctqw_state

        )

        norm = np.linalg.norm(hybrid)

        if norm > 0:

            hybrid /= norm

        return hybrid

    ####################################################################
    # Execute Scheduler
    ####################################################################

    def run(self):

        dtqw_state = self.run_dtqw()

        ctqw_state = self.run_ctqw()

        hybrid_state = self.fuse(

            dtqw_state,

            ctqw_state,

        )

        save_hybrid_state(

            hybrid_state,

        )

        return hybrid_state

    ####################################################################
    # Probability Distribution
    ####################################################################

    @staticmethod
    def probabilities(

        hybrid_state,

    ):

        probability = np.abs(

            hybrid_state

        ) ** 2

        probability /= probability.sum()

        return probability

    ####################################################################
    # Ranked Nodes
    ####################################################################

    def ranked_nodes(

        self,

        hybrid_state,

    ):

        probability = self.probabilities(

            hybrid_state,

        )

        ranking = np.argsort(

            probability

        )[::-1]

        results = []

        for node in ranking:

            results.append(

                {

                    "node": int(node),

                    "score": float(

                        probability[node]

                    ),

                }

            )

        return results

    ####################################################################
    # Summary
    ####################################################################

    def summary(

        self,

        hybrid_state,

    ):

        probability = self.probabilities(

            hybrid_state,

        )

        return {

            "omega1": self.omega1,

            "omega2": self.omega2,

            "dimension": len(hybrid_state),

            "probability_sum": float(

                probability.sum()

            ),

            "maximum_probability": float(

                probability.max()

            ),

            "minimum_probability": float(

                probability.min()

            ),

        }