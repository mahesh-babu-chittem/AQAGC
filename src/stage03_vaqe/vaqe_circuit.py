"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Variational Quantum Circuit

==============================================================
"""

import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import StatePreparation


class VAQECircuit:

    """
    Figure 2

    Input Layer
            ↓
    Amplitude Encoding
            ↓
    Risk Re-upload Layer
            ↓
    Variational Layers
            ↓
    Risk Re-upload Layer
            ↓
    Output Layer
    """

    def __init__(
        self,
        amplitudes,
        num_variational_layers=3,
        reupload_layers=2
    ):

        self.amplitudes = np.asarray(
            amplitudes,
            dtype=np.complex128
        )

        self.num_layers = num_variational_layers
        self.reupload_layers = reupload_layers

        self.num_qubits = int(
            np.ceil(
                np.log2(
                    len(self.amplitudes)
                )
            )
        )

        self.dimension = 2 ** self.num_qubits

        self.state = self._pad_state()

        self.circuit = QuantumCircuit(
            self.num_qubits,
            self.num_qubits
        )

        self.theta = ParameterVector(
            "θ",
            self.num_layers * self.num_qubits * 2
        )

    # ----------------------------------------------------------

    def _pad_state(self):

        state = np.zeros(
            self.dimension,
            dtype=np.complex128
        )

        state[:len(self.amplitudes)] = self.amplitudes

        state /= np.linalg.norm(state)

        return state

    # ----------------------------------------------------------
    # Figure 2
    # Amplitude Mapping
    # ----------------------------------------------------------

    def amplitude_encoding(self):

        preparation = StatePreparation(
            self.state
        )

        self.circuit.append(
            preparation,
            range(self.num_qubits)
        )

    # ----------------------------------------------------------
    # Figure 2
    # Risk Feature Re-upload
    # ----------------------------------------------------------

    def risk_reupload(self):

        for qubit in range(self.num_qubits):

            angle = float(
                np.abs(
                    self.state[qubit]
                )
            ) * np.pi

            self.circuit.ry(
                angle,
                qubit
            )

    # ----------------------------------------------------------
    # Figure 2
    # Variational Layer
    # ----------------------------------------------------------

    def variational_layer(self, layer):

        offset = layer * self.num_qubits * 2

        for qubit in range(self.num_qubits):

            self.circuit.ry(
                self.theta[offset],
                qubit
            )

            offset += 1

        for qubit in range(self.num_qubits - 1):

            self.circuit.cx(
                qubit,
                qubit + 1
            )

        for qubit in range(self.num_qubits):

            self.circuit.rz(
                self.theta[offset],
                qubit
            )

            offset += 1

    # ----------------------------------------------------------
    # Output Layer
    # ----------------------------------------------------------

    def output_layer(self):

        self.circuit.barrier()

        self.circuit.measure_all()

    # ----------------------------------------------------------

    def build(self):

        self.amplitude_encoding()

        self.risk_reupload()

        for layer in range(self.num_layers):

            self.variational_layer(layer)

            if layer < self.reupload_layers:

                self.risk_reupload()

        self.output_layer()

        return self.circuit