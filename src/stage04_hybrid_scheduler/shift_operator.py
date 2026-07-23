"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

DTQW Shift Operator

==============================================================
"""

from __future__ import annotations

import numpy as np


class ShiftOperator:
    """
    Shift operator for the Discrete-Time Quantum Walk.
    """

    def __init__(

        self,

        number_of_nodes: int,

    ):

        self.number_of_nodes = int(

            number_of_nodes

        )

    ####################################################################
    # Shift Matrix
    ####################################################################

    def matrix(self):

        dimension = 2 * self.number_of_nodes

        shift = np.zeros(

            (

                dimension,

                dimension,

            ),

            dtype=np.complex128,

        )

        for node in range(

            self.number_of_nodes

        ):

            left = (node - 1) % self.number_of_nodes

            right = (node + 1) % self.number_of_nodes

            shift[
                2 * left,
                2 * node,
            ] = 1.0

            shift[
                2 * right + 1,
                2 * node + 1,
            ] = 1.0

        return shift

    ####################################################################
    # Apply Shift
    ####################################################################

    def apply(

        self,

        quantum_state,

    ):

        quantum_state = np.asarray(

            quantum_state,

            dtype=np.complex128,

        )

        return self.matrix() @ quantum_state

    ####################################################################
    # Identity Check
    ####################################################################

    def identity(self):

        dimension = 2 * self.number_of_nodes

        return np.eye(

            dimension,

            dtype=np.complex128,

        )

    ####################################################################
    # Unitary Check
    ####################################################################

    def is_unitary(self):

        shift = self.matrix()

        identity = np.eye(

            shift.shape[0],

            dtype=np.complex128,

        )

        return np.allclose(

            shift.conjugate().T @ shift,

            identity,

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        shift = self.matrix()

        return {

            "dimension": shift.shape,

            "unitary": self.is_unitary(),

        }