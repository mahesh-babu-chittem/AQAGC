"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Configuration

==============================================================
"""

from pathlib import Path
import numpy as np

# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

BENCHMARK_DIR = DATA_DIR / "benchmark"

ENCODED_DIR = DATA_DIR / "encoded"

# ============================================================
# Dataset Selection
# ============================================================

DATASET_NAME = "CSE_CIC_IDS2018"

INPUT_DIR = BENCHMARK_DIR / DATASET_NAME

OUTPUT_DIR = ENCODED_DIR / DATASET_NAME

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Stage 02 Inputs
# ============================================================

GRAPH_FILE = INPUT_DIR / "AQAGC_Attack_Graph.graphml"

NODE_FILE = INPUT_DIR / "nodes.csv"

EDGE_FILE = INPUT_DIR / "edges.csv"

GROUND_TRUTH_FILE = INPUT_DIR / "ground_truth.csv"

METADATA_FILE = INPUT_DIR / "metadata.json"

# ============================================================
# Stage 03 Outputs
# ============================================================

AMPLITUDE_FILE = OUTPUT_DIR / "risk_amplitudes.csv"

STATEVECTOR_FILE = OUTPUT_DIR / "initial_statevector.npy"

ENCODED_STATE_FILE = OUTPUT_DIR / "encoded_quantum_state.npy"

NODE_ENCODING_FILE = OUTPUT_DIR / "node_encoding_scores.csv"

HAMILTONIAN_FILE = OUTPUT_DIR / "hamiltonian.npy"

ADJACENCY_MATRIX_FILE = OUTPUT_DIR / "adjacency_matrix.npy"

MEASUREMENT_FILE = OUTPUT_DIR / "measurement_counts.json"

CIRCUIT_FILE = OUTPUT_DIR / "vaqe_circuit.qpy"

PARAMETERS_FILE = OUTPUT_DIR / "trained_parameters.npy"

ENCODING_METADATA_FILE = OUTPUT_DIR / "encoding_metadata.json"

# ============================================================
# Numerical Parameters
# ============================================================

FLOAT_DTYPE = np.float64

EPSILON = 1e-12

# ============================================================
# Quantum Parameters
# ============================================================

MAX_QUBITS = 12

SHOTS = 4096

RANDOM_SEED = 42

OPTIMIZATION_LEVEL = 3

# ============================================================
# Variational Circuit
# ============================================================

NUM_VARIATIONAL_LAYERS = 3

REUPLOAD_LAYERS = 2

ENTANGLEMENT = "linear"

ROTATION_GATES = ["ry", "rz"]

# ============================================================
# Hamiltonian
# ============================================================

PROPAGATION_COEFFICIENT = 0.05

# ============================================================
# Equation (31)
# ============================================================

LAMBDA = 0.7

# ============================================================
# Backend
# ============================================================

SIMULATION_METHOD = "density_matrix"

SAVE_DENSITY_MATRIX = True

SAVE_STATEVECTOR = True

# ============================================================
# Logging
# ============================================================

VERBOSE = True