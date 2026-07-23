"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Configuration

==============================================================
"""

from pathlib import Path

###############################################################
# Project Directories
###############################################################

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

STAGE03_DIR = DATA_DIR / "stage03"

STAGE04_DIR = DATA_DIR / "stage04"

STAGE04_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

###############################################################
# Stage-03 Inputs
###############################################################

ATTACK_GRAPH_FILE = STAGE03_DIR / "attack_graph.graphml"

NODES_FILE = STAGE03_DIR / "node_encodings.csv"

EDGES_FILE = STAGE03_DIR / "edges.csv"

GROUND_TRUTH_FILE = STAGE03_DIR / "ground_truth.csv"

METADATA_FILE = STAGE03_DIR / "metadata.json"

ENCODED_STATE_FILE = STAGE03_DIR / "encoded_state.npy"

HAMILTONIAN_FILE = STAGE03_DIR / "graph_hamiltonian.npy"

###############################################################
# Stage-04 Outputs
###############################################################

GRAPH_STATISTICS_FILE = STAGE04_DIR / "graph_statistics.json"

ADJACENCY_MATRIX_FILE = STAGE04_DIR / "adjacency_matrix.npy"

LAPLACIAN_MATRIX_FILE = STAGE04_DIR / "laplacian_matrix.npy"

DTQW_STATE_FILE = STAGE04_DIR / "dtqw_state.npy"

CTQW_STATE_FILE = STAGE04_DIR / "ctqw_state.npy"

HYBRID_STATE_FILE = STAGE04_DIR / "hybrid_state.npy"

PROPAGATED_RISK_FILE = STAGE04_DIR / "propagated_risk.csv"

ATTACK_PATHS_FILE = STAGE04_DIR / "attack_paths.csv"

METADATA_OUTPUT_FILE = STAGE04_DIR / "metadata.json"

###############################################################
# Adaptive Scheduler
###############################################################

OMEGA1 = 0.60

OMEGA2 = 0.40

###############################################################
# DTQW
###############################################################

DTQW_STEPS = 10

COIN_TYPE = "grover"

###############################################################
# CTQW
###############################################################

CTQW_STEPS = 10

EVOLUTION_TIME = 1.0

###############################################################
# Attack Path Search
###############################################################

DEFAULT_PATH_CUTOFF = 6

TOP_K_PATHS = 20

###############################################################
# Numerical Parameters
###############################################################

EPSILON = 1e-12

RANDOM_SEED = 42

VERBOSE = True