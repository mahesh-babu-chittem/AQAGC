"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Hamiltonian Evolution

Implements the Continuous-Time Quantum Walk evolution

    |ψ(t)> = exp(-iHt)|ψ(0)>

==============================================================
"""

from __future__ import annotations

import numpy as np

from io_utils import load_hamiltonian


class HamiltonianEvolution:
    """
    Continuous-Time Quantum Evolution using the
    graph Hamiltonian generated in Stage-03.
    """

    def __init__(

        self,

        hamiltonian=None,

    ):

        if hamiltonian is None:

            hamiltonian = load_hamiltonian()

        self.hamiltonian = np.asarray(

            hamiltonian,

            dtype=np.complex128,

        )

    ####################################################################
    # Hamiltonian
    ####################################################################

    def matrix(self):

        return self.hamiltonian

    ####################################################################
    # Evolution Operator
    ####################################################################

    def evolution_operator(

        self,

        time=1.0,

    ):

        eigenvalues, eigenvectors = np.linalg.eigh(

            self.hamiltonian

        )

        diagonal = np.diag(

            np.exp(

                -1j *

                eigenvalues *

                time

            )

        )

        operator = (

            eigenvectors

            @ diagonal

            @ eigenvectors.conjugate().T

        )

        return operator

    ####################################################################
    # Single Evolution
    ####################################################################

    def evolve(

        self,

        quantum_state,

        time=1.0,

    ):

        quantum_state = np.asarray(

            quantum_state,

            dtype=np.complex128,

        )

        operator = self.evolution_operator(

            time

        )

        return operator @ quantum_state

    ####################################################################
    # Multiple Evolutions
    ####################################################################

    def evolve_steps(

        self,

        quantum_state,

        steps=10,

        delta_time=1.0,

    ):

        state = np.asarray(

            quantum_state,

            dtype=np.complex128,

        )

        for _ in range(steps):

            state = self.evolve(

                state,

                delta_time,

            )

        return state

    ####################################################################
    # Hamiltonian Dimension
    ####################################################################

    def dimension(self):

        return self.hamiltonian.shape[0]

    ####################################################################
    # Hermitian Check
    ####################################################################

    def is_hermitian(self):

        return np.allclose(

            self.hamiltonian,

            self.hamiltonian.conjugate().T,

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        return {

            "dimension":

                self.dimension(),

            "hermitian":

                self.is_hermitian(),

            "trace":

                float(

                    np.trace(

                        self.hamiltonian

                    ).real

                ),

        }