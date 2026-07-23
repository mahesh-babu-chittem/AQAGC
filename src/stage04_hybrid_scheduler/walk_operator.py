"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

DTQW Walk Operator

Implements

    U = S (C ⊗ I)

==============================================================
"""

from __future__ import annotations

import numpy as np

from coin_operator import CoinOperator
from shift_operator import ShiftOperator


class WalkOperator:
    """
    Constructs the DTQW evolution operator.
    """

    def __init__(

        self,

        number_of_nodes: int,

        coin_type: str = "grover",

    ):

        self.number_of_nodes = int(number_of_nodes)

        self.coin = CoinOperator(
            coin_type=coin_type,
        )

        self.shift = ShiftOperator(
            number_of_nodes=self.number_of_nodes,
        )

    ####################################################################
    # Coin Expansion
    ####################################################################

    def expanded_coin(self):

        coin = self.coin.matrix()

        identity = np.eye(

            self.number_of_nodes,

            dtype=np.complex128,

        )

        return np.kron(

            identity,

            coin,

        )

    ####################################################################
    # Walk Operator
    ####################################################################

    def matrix(self):

        shift = self.shift.matrix()

        coin = self.expanded_coin()

        return shift @ coin

    ####################################################################
    # Apply Walk
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
    # Multi-step Evolution
    ####################################################################

    def evolve(

        self,

        quantum_state,

        steps=1,

    ):

        state = np.asarray(

            quantum_state,

            dtype=np.complex128,

        )

        operator = self.matrix()

        for _ in range(steps):

            state = operator @ state

        return state

    ####################################################################
    # Unitary Check
    ####################################################################

    def is_unitary(self):

        operator = self.matrix()

        identity = np.eye(

            operator.shape[0],

            dtype=np.complex128,

        )

        return np.allclose(

            operator.conjugate().T @ operator,

            identity,

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        operator = self.matrix()

        return {

            "shape": operator.shape,

            "unitary": self.is_unitary(),

        }