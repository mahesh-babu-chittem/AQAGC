"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Discrete-Time Quantum Walk (DTQW)

==============================================================
"""

from __future__ import annotations

import numpy as np

from walk_operator import WalkOperator
from io_utils import save_dtqw_state


class DTQWWalk:
    """
    Executes the Discrete-Time Quantum Walk.
    """

    def __init__(
        self,
        number_of_nodes: int,
        coin_type: str = "grover",
    ):

        self.number_of_nodes = int(number_of_nodes)

        self.walk_operator = WalkOperator(
            number_of_nodes=self.number_of_nodes,
            coin_type=coin_type,
        )

    ####################################################################
    # Initial State
    ####################################################################

    def initialize_state(self):

        dimension = 2 * self.number_of_nodes

        state = np.ones(
            dimension,
            dtype=np.complex128,
        )

        state /= np.linalg.norm(state)

        return state

    ####################################################################
    # Single Step
    ####################################################################

    def step(
        self,
        state,
    ):

        return self.walk_operator.apply(state)

    ####################################################################
    # Multiple Steps
    ####################################################################

    def evolve(
        self,
        initial_state=None,
        steps=10,
    ):

        if initial_state is None:

            state = self.initialize_state()

        else:

            state = np.asarray(
                initial_state,
                dtype=np.complex128,
            )

        for _ in range(steps):

            state = self.step(state)

        return state

    ####################################################################
    # Final State
    ####################################################################

    def final_state(
        self,
        initial_state=None,
        steps=10,
    ):

        state = self.evolve(
            initial_state=initial_state,
            steps=steps,
        )

        save_dtqw_state(state)

        return state

    ####################################################################
    # Measurement Probabilities
    ####################################################################

    @staticmethod
    def probabilities(
        quantum_state,
    ):

        probability = np.abs(
            quantum_state
        ) ** 2

        return probability / probability.sum()

    ####################################################################
    # Node Probabilities
    ####################################################################

    def node_probabilities(
        self,
        quantum_state,
    ):

        probability = self.probabilities(
            quantum_state
        )

        node_probability = np.zeros(
            self.number_of_nodes,
            dtype=np.float64,
        )

        for node in range(self.number_of_nodes):

            node_probability[node] = (

                probability[2 * node]

                +

                probability[2 * node + 1]

            )

        return node_probability

    ####################################################################
    # Most Probable Nodes
    ####################################################################

    def top_nodes(
        self,
        quantum_state,
        k=10,
    ):

        probability = self.node_probabilities(
            quantum_state
        )

        ranking = np.argsort(
            probability
        )[::-1]

        results = []

        for node in ranking[:k]:

            results.append({

                "node": int(node),

                "probability": float(
                    probability[node]
                ),

            })

        return results

    ####################################################################
    # Summary
    ####################################################################

    def summary(
        self,
        quantum_state,
    ):

        probability = self.node_probabilities(
            quantum_state
        )

        return {

            "dimension":

                len(quantum_state),

            "number_of_nodes":

                self.number_of_nodes,

            "probability_sum":

                float(probability.sum()),

            "maximum_probability":

                float(probability.max()),

            "minimum_probability":

                float(probability.min()),

        }