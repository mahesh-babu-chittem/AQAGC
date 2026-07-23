"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Feature Encoder

==============================================================
"""

import numpy as np
import pandas as pd

from config import FLOAT_DTYPE, EPSILON
from io_utils import save_amplitudes


class FeatureEncoder:

    """
    Generates the vulnerability-aware amplitudes used for
    quantum state initialization.
    """

    def __init__(self, nodes_df: pd.DataFrame):

        self.nodes = nodes_df.copy()

        self.risk_column = None

    # ---------------------------------------------------------
    # Detect Risk Column
    # ---------------------------------------------------------

    def detect_risk_column(self):

        candidates = [

            "Risk_Score",
            "risk_score",
            "Risk",
            "risk",
            "Node_Risk",
            "Severity",
            "severity"

        ]

        for column in candidates:

            if column in self.nodes.columns:

                self.risk_column = column
                return

        raise ValueError(
            "Unable to locate vulnerability risk column."
        )

    # ---------------------------------------------------------
    # Equation (28)
    # ---------------------------------------------------------

    def compute_amplitudes(self):

        risk = self.nodes[self.risk_column].astype(
            FLOAT_DTYPE
        ).to_numpy()

        denominator = np.sqrt(
            np.sum(np.square(risk))
        )

        denominator = max(
            denominator,
            EPSILON
        )

        amplitudes = risk / denominator

        return amplitudes

    # ---------------------------------------------------------
    # Equation (27)
    # ---------------------------------------------------------

    @staticmethod
    def normalize(amplitudes):

        norm = np.linalg.norm(amplitudes)

        norm = max(norm, EPSILON)

        return amplitudes / norm

    # ---------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------

    def export(self, amplitudes):

        output = self.nodes.copy()

        output["Amplitude"] = amplitudes

        output["Probability"] = amplitudes ** 2

        save_amplitudes(output)

    # ---------------------------------------------------------
    # Equation (29)
    # ---------------------------------------------------------

    def create_initial_state(self):

        self.detect_risk_column()

        amplitudes = self.compute_amplitudes()

        amplitudes = self.normalize(amplitudes)

        self.export(amplitudes)

        return amplitudes.astype(np.complex128)

    # ---------------------------------------------------------

    def run(self):

        return self.create_initial_state()