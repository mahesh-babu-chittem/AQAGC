"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Input / Output Utilities

==============================================================
"""

import json
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from config import (
    ATTACK_GRAPH_FILE,
    NODES_FILE,
    EDGES_FILE,
    GROUND_TRUTH_FILE,
    METADATA_FILE,
    ENCODED_STATE_FILE,
    HAMILTONIAN_FILE,
    GRAPH_STATISTICS_FILE,
    ADJACENCY_MATRIX_FILE,
    LAPLACIAN_MATRIX_FILE,
    DTQW_STATE_FILE,
    CTQW_STATE_FILE,
    HYBRID_STATE_FILE,
    PROPAGATED_RISK_FILE,
    ATTACK_PATHS_FILE,
    METADATA_OUTPUT_FILE,
)


###############################################################
# Stage-03 Loaders
###############################################################

def load_attack_graph():

    return nx.read_graphml(
        ATTACK_GRAPH_FILE
    )


def load_nodes():

    return pd.read_csv(
        NODES_FILE
    )


def load_edges():

    return pd.read_csv(
        EDGES_FILE
    )


def load_ground_truth():

    return pd.read_csv(
        GROUND_TRUTH_FILE
    )


def load_metadata():

    if not Path(METADATA_FILE).exists():

        return {}

    with open(
        METADATA_FILE,
        "r",
    ) as f:

        return json.load(f)


def load_encoded_state():

    return np.load(
        ENCODED_STATE_FILE
    )


def load_hamiltonian():

    return np.load(
        HAMILTONIAN_FILE
    )


###############################################################
# Graph Statistics
###############################################################

def save_graph_statistics(stats):

    with open(
        GRAPH_STATISTICS_FILE,
        "w",
    ) as f:

        json.dump(
            stats,
            f,
            indent=4,
        )


###############################################################
# Adjacency Matrix
###############################################################

def save_adjacency_matrix(matrix):

    np.save(
        ADJACENCY_MATRIX_FILE,
        matrix,
    )


def load_adjacency_matrix():

    return np.load(
        ADJACENCY_MATRIX_FILE
    )


###############################################################
# Laplacian Matrix
###############################################################

def save_laplacian_matrix(matrix):

    np.save(
        LAPLACIAN_MATRIX_FILE,
        matrix,
    )


def load_laplacian_matrix():

    return np.load(
        LAPLACIAN_MATRIX_FILE
    )


###############################################################
# DTQW State
###############################################################

def save_dtqw_state(state):

    np.save(
        DTQW_STATE_FILE,
        state,
    )


def load_dtqw_state():

    return np.load(
        DTQW_STATE_FILE
    )


###############################################################
# CTQW State
###############################################################

def save_ctqw_state(state):

    np.save(
        CTQW_STATE_FILE,
        state,
    )


def load_ctqw_state():

    return np.load(
        CTQW_STATE_FILE
    )


###############################################################
# Hybrid State
###############################################################

def save_hybrid_state(state):

    np.save(
        HYBRID_STATE_FILE,
        state,
    )


def load_hybrid_state():

    return np.load(
        HYBRID_STATE_FILE
    )


###############################################################
# Propagated Risk
###############################################################

def save_propagated_risk(df):

    df.to_csv(
        PROPAGATED_RISK_FILE,
        index=False,
    )


def load_propagated_risk():

    return pd.read_csv(
        PROPAGATED_RISK_FILE
    )


###############################################################
# Attack Paths
###############################################################

def save_attack_paths(df):

    df.to_csv(
        ATTACK_PATHS_FILE,
        index=False,
    )


def load_attack_paths():

    return pd.read_csv(
        ATTACK_PATHS_FILE
    )


###############################################################
# Stage Metadata
###############################################################

def save_metadata(metadata):

    with open(
        METADATA_OUTPUT_FILE,
        "w",
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
        )