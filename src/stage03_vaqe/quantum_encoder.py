"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Quantum Encoder

==============================================================
"""

import numpy as np

from qiskit import transpile
from qiskit.quantum_info import DensityMatrix

from qiskit_aer import AerSimulator

from config import (
    SHOTS,
    RANDOM_SEED,
    OPTIMIZATION_LEVEL,
    SIMULATION_METHOD,
    NUM_VARIATIONAL_LAYERS,
    REUPLOAD_LAYERS,
)

from feature_encoder import FeatureEncoder
from vaqe_circuit import VAQECircuit

from io_utils import (
    save_statevector,
    save_encoded_state,
    save_measurement_counts,
    save_qiskit_circuit,
)


class QuantumEncoder:

    def __init__(self, nodes):

        self.nodes = nodes

        self.initial_state = None

        self.circuit = None

        self.backend = AerSimulator(
            method=SIMULATION_METHOD
        )

    # ----------------------------------------------------------
    # Equation (28-29)
    # ----------------------------------------------------------

    def prepare_state(self):

        encoder = FeatureEncoder(
            self.nodes
        )

        self.initial_state = encoder.run()

        save_statevector(
            self.initial_state
        )

    # ----------------------------------------------------------
    # Figure 2
    # ----------------------------------------------------------

    def build_circuit(self):

        builder = VAQECircuit(
            amplitudes=self.initial_state,
            num_variational_layers=NUM_VARIATIONAL_LAYERS,
            reupload_layers=REUPLOAD_LAYERS
        )

        self.circuit = builder.build()

        save_qiskit_circuit(
            self.circuit
        )

    # ----------------------------------------------------------
    # Execute
    # ----------------------------------------------------------

    def execute(self):

        compiled = transpile(

            self.circuit,

            backend=self.backend,

            optimization_level=OPTIMIZATION_LEVEL,

            seed_transpiler=RANDOM_SEED

        )

        job = self.backend.run(

            compiled,

            shots=SHOTS,

            seed_simulator=RANDOM_SEED

        )

        result = job.result()

        counts = result.get_counts()

        save_measurement_counts(
            counts
        )

        return result

    # ----------------------------------------------------------
    # Density Matrix
    # ----------------------------------------------------------

    def extract_density_matrix(self):

        circuit = self.circuit.remove_final_measurements(
            inplace=False
        )

        density = DensityMatrix.from_instruction(
            circuit
        )

        matrix = np.asarray(
            density.data
        )

        save_encoded_state(
            matrix
        )

        return matrix

    # ----------------------------------------------------------

    def run(self):

        self.prepare_state()

        self.build_circuit()

        self.execute()

        encoded_state = self.extract_density_matrix()

        return encoded_state