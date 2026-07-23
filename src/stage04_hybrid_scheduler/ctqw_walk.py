"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Continuous-Time Quantum Walk (CTQW)

==============================================================
"""

from __future__ import annotations

import numpy as np

from hamiltonian_evolution import HamiltonianEvolution
from io_utils import (
    load_hamiltonian,
    save_ctqw_state,
)


class CTQWWalk:
    """
    Executes the Continuous-Time Quantum Walk (CTQW).

    Evolution:

        |ψ(t)> = exp(-iHt)|ψ(0)>
    """

    def __init__(

        self,

        hamiltonian=None,

    ):

        if hamiltonian is None:

            hamiltonian = load_hamiltonian()

        self.evolution = HamiltonianEvolution(

            hamiltonian

        )

    ####################################################################
    # Initial State
    ####################################################################

    def initialize_state(self):

        dimension = self.evolution.dimension()

        state = np.ones(

            dimension,

            dtype=np.complex128,

        )

        state /= np.linalg.norm(state)

        return state

    ####################################################################
    # Single Evolution
    ####################################################################

    def step(

        self,

        state,

        delta_time=1.0,

    ):

        return self.evolution.evolve(

            state,

            delta_time,

        )

    ####################################################################
    # Multiple Evolution
    ####################################################################

    def evolve(

        self,

        initial_state=None,

        steps=10,

        delta_time=1.0,

    ):

        if initial_state is None:

            state = self.initialize_state()

        else:

            state = np.asarray(

                initial_state,

                dtype=np.complex128,

            )

        for _ in range(steps):

            state = self.step(

                state,

                delta_time,

            )

        return state

    ####################################################################
    # Final State
    ####################################################################

    def final_state(

        self,

        initial_state=None,

        steps=10,

        delta_time=1.0,

    ):

        state = self.evolve(

            initial_state=initial_state,

            steps=steps,

            delta_time=delta_time,

        )

        save_ctqw_state(

            state

        )

        return state

    ####################################################################
    # Probability Distribution
    ####################################################################

    @staticmethod
    def probabilities(

        quantum_state,

    ):

        probability = np.abs(

            quantum_state

        ) ** 2

        probability /= probability.sum()

        return probability

    ####################################################################
    # Most Important Nodes
    ####################################################################

    def top_nodes(

        self,

        quantum_state,

        k=10,

    ):

        probability = self.probabilities(

            quantum_state

        )

        ranking = np.argsort(

            probability

        )[::-1]

        results = []

        for node in ranking[:k]:

            results.append(

                {

                    "node": int(node),

                    "probability": float(

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

        quantum_state,

    ):

        probability = self.probabilities(

            quantum_state

        )

        return {

            "dimension":

                len(

                    quantum_state

                ),

            "probability_sum":

                float(

                    probability.sum()

                ),

            "maximum_probability":

                float(

                    probability.max()

                ),

            "minimum_probability":

                float(

                    probability.min()

                ),

        }