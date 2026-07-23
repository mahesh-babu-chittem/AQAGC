"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Input / Output Utilities

==============================================================
"""

import json

import networkx as nx
import numpy as np
import pandas as pd
from qiskit import qpy

from config import (
    GRAPH_FILE,
    NODE_FILE,
    EDGE_FILE,
    GROUND_TRUTH_FILE,
    METADATA_FILE,
    AMPLITUDE_FILE,
    STATEVECTOR_FILE,
    ENCODED_STATE_FILE,
    NODE_ENCODING_FILE,
    HAMILTONIAN_FILE,
    ADJACENCY_MATRIX_FILE,
    MEASUREMENT_FILE,
    CIRCUIT_FILE,
    PARAMETERS_FILE,
    ENCODING_METADATA_FILE,
)


# ============================================================
# Loading
# ============================================================

def load_attack_graph():

    if not GRAPH_FILE.exists():
        raise FileNotFoundError(GRAPH_FILE)

    return nx.read_graphml(GRAPH_FILE)


def load_nodes():

    if not NODE_FILE.exists():
        raise FileNotFoundError(NODE_FILE)

    return pd.read_csv(NODE_FILE)


def load_edges():

    if not EDGE_FILE.exists():
        raise FileNotFoundError(EDGE_FILE)

    return pd.read_csv(EDGE_FILE)


def load_ground_truth():

    if not GROUND_TRUTH_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(GROUND_TRUTH_FILE)


def load_metadata():

    if not METADATA_FILE.exists():
        return {}

    with open(METADATA_FILE, "r") as f:
        return json.load(f)


# ============================================================
# Saving
# ============================================================

def save_amplitudes(df):

    df.to_csv(
        AMPLITUDE_FILE,
        index=False
    )


def save_node_encodings(df):

    df.to_csv(
        NODE_ENCODING_FILE,
        index=False
    )


def save_statevector(statevector):

    np.save(
        STATEVECTOR_FILE,
        statevector
    )


def save_encoded_state(state):

    np.save(
        ENCODED_STATE_FILE,
        state
    )


def save_hamiltonian(matrix):

    np.save(
        HAMILTONIAN_FILE,
        matrix
    )


def save_adjacency_matrix(matrix):

    np.save(
        ADJACENCY_MATRIX_FILE,
        matrix
    )


def save_measurement_counts(counts):

    with open(
        MEASUREMENT_FILE,
        "w"
    ) as f:

        json.dump(
            counts,
            f,
            indent=4
        )


def save_parameters(parameters):

    np.save(
        PARAMETERS_FILE,
        parameters
    )


def save_metadata(metadata):

    with open(
        ENCODING_METADATA_FILE,
        "w"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )


# ============================================================
# Qiskit Circuit
# ============================================================

def save_qiskit_circuit(circuit):

    with open(
        CIRCUIT_FILE,
        "wb"
    ) as fd:

        qpy.dump(
            circuit,
            fd
        )


def load_qiskit_circuit():

    with open(
        CIRCUIT_FILE,
        "rb"
    ) as fd:

        circuits = qpy.load(fd)

    return circuits[0]


# ============================================================
# Validation
# ============================================================

def ensure_columns(df, columns):

    missing = []

    for column in columns:

        if column not in df.columns:

            missing.append(column)

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )


# ============================================================
# Console
# ============================================================

def stage_header(title):

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def info(message):

    print(f"[INFO] {message}")


def success(message):

    print(f"[SUCCESS] {message}")


def warning(message):

    print(f"[WARNING] {message}")


def separator():

    print("-" * 80)