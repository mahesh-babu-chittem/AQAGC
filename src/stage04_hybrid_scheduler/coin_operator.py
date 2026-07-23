"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

DTQW Coin Operator

==============================================================
"""

from __future__ import annotations

import numpy as np


class CoinOperator:
    """
    Generates the quantum coin operator used by
    the Discrete-Time Quantum Walk (DTQW).
    """

    def __init__(

        self,

        coin_type="grover",

    ):

        self.coin_type = coin_type.lower()

    ####################################################################
    # Grover Coin
    ####################################################################

    @staticmethod
    def grover():

        return np.array(

            [

                [0.0, 1.0],

                [1.0, 0.0],

            ],

            dtype=np.complex128,

        )

    ####################################################################
    # Hadamard Coin
    ####################################################################

    @staticmethod
    def hadamard():

        return (

            1.0 / np.sqrt(2.0)

        ) * np.array(

            [

                [1.0, 1.0],

                [1.0, -1.0],

            ],

            dtype=np.complex128,

        )

    ####################################################################
    # Identity Coin
    ####################################################################

    @staticmethod
    def identity():

        return np.eye(

            2,

            dtype=np.complex128,

        )

    ####################################################################
    # Coin Matrix
    ####################################################################

    def matrix(self):

        if self.coin_type == "grover":

            return self.grover()

        if self.coin_type == "hadamard":

            return self.hadamard()

        if self.coin_type == "identity":

            return self.identity()

        raise ValueError(

            f"Unsupported coin type: {self.coin_type}"

        )

    ####################################################################
    # Apply Coin
    ####################################################################

    def apply(

        self,

        state,

    ):

        state = np.asarray(

            state,

            dtype=np.complex128,

        )

        coin = self.matrix()

        dimension = state.shape[0]

        if dimension % 2 != 0:

            raise ValueError(

                "DTQW state dimension must be even."

            )

        output = np.zeros_like(

            state,

        )

        for index in range(

            0,

            dimension,

            2,

        ):

            output[index:index + 2] = (

                coin @ state[index:index + 2]

            )

        return output

    ####################################################################
    # Validate Coin
    ####################################################################

    def is_unitary(self):

        coin = self.matrix()

        identity = np.eye(

            coin.shape[0],

            dtype=np.complex128,

        )

        return np.allclose(

            coin.conjugate().T @ coin,

            identity,

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        coin = self.matrix()

        return {

            "coin_type": self.coin_type,

            "shape": coin.shape,

            "unitary": self.is_unitary(),

        }