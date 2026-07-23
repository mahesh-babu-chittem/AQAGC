"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Graph Laplacian Builder

Constructs the graph Laplacian used by the
Continuous-Time Quantum Walk (CTQW).

==============================================================
"""

from __future__ import annotations

import numpy as np

from io_utils import (
    save_laplacian_matrix,
)


class LaplacianBuilder:
    """
    Constructs the graph Laplacian.

    L = D - A
    """

    def __init__(

        self,

        adjacency_matrix,

    ):

        self.adjacency = np.asarray(

            adjacency_matrix,

            dtype=np.float64,

        )

    ####################################################################
    # Degree Matrix
    ####################################################################

    def degree_matrix(self):

        degree = np.sum(

            self.adjacency,

            axis=1,

        )

        return np.diag(

            degree

        )

    ####################################################################
    # Laplacian
    ####################################################################

    def build(self):

        degree = self.degree_matrix()

        laplacian = degree - self.adjacency

        save_laplacian_matrix(

            laplacian

        )

        return laplacian

    ####################################################################
    # Spectral Radius
    ####################################################################

    def spectral_radius(self):

        laplacian = self.build()

        eigenvalues = np.linalg.eigvals(

            laplacian

        )

        return float(

            np.max(

                np.abs(

                    eigenvalues

                )

            )

        )

    ####################################################################
    # Eigenvalues
    ####################################################################

    def eigenvalues(self):

        laplacian = self.build()

        return np.linalg.eigvals(

            laplacian

        )

    ####################################################################
    # Eigenvectors
    ####################################################################

    def eigenvectors(self):

        laplacian = self.build()

        _, vectors = np.linalg.eigh(

            laplacian

        )

        return vectors

    ####################################################################
    # Trace
    ####################################################################

    def trace(self):

        laplacian = self.build()

        return float(

            np.trace(

                laplacian

            )

        )

    ####################################################################
    # Frobenius Norm
    ####################################################################

    def frobenius_norm(self):

        laplacian = self.build()

        return float(

            np.linalg.norm(

                laplacian,

                ord="fro",

            )

        )

    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        laplacian = self.build()

        return {

            "shape": laplacian.shape,

            "trace": self.trace(),

            "spectral_radius": self.spectral_radius(),

            "frobenius_norm": self.frobenius_norm(),

        }