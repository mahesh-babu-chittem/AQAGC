"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Input / Output Utilities

==============================================================
"""

from __future__ import annotations

import json
import pickle

import numpy as np
import pandas as pd
import networkx as nx

from config import *

###############################################################
# Graph
###############################################################

def load_attack_graph():

    return nx.read_graphml(
        GRAPH_FILE,
    )


###############################################################
# Nodes
###############################################################

def load_nodes():

    return pd.read_csv(
        NODE_FILE,
    )


###############################################################
# Edges
###############################################################

def load_edges():

    return pd.read_csv(
        EDGE_FILE,
    )


###############################################################
# Hybrid State
###############################################################

def load_hybrid_state():

    return np.load(
        HYBRID_STATE_FILE,
    )


###############################################################
# DTQW State
###############################################################

def load_dtqw_state():

    return np.load(
        DTQW_STATE_FILE,
    )


###############################################################
# CTQW State
###############################################################

def load_ctqw_state():

    return np.load(
        CTQW_STATE_FILE,
    )


###############################################################
# Propagated Risk
###############################################################

def load_propagated_risk():

    return np.load(
        PROPAGATED_RISK_FILE,
    )


###############################################################
# Attack Paths
###############################################################

def load_attack_paths():

    with open(
        ATTACK_PATH_FILE,
        "r",
    ) as file:

        return json.load(file)


###############################################################
# Node Risk
###############################################################

def save_node_risk_scores(df):

    df.to_csv(

        NODE_RISK_FILE,

        index=False,

    )


def load_node_risk_scores():

    return pd.read_csv(

        NODE_RISK_FILE,

    )


###############################################################
# Edge Risk
###############################################################

def save_edge_risk_scores(df):

    df.to_csv(

        EDGE_RISK_FILE,

        index=False,

    )


def load_edge_risk_scores():

    return pd.read_csv(

        EDGE_RISK_FILE,

    )


###############################################################
# Path Risk
###############################################################

def save_path_risk_scores(df):

    df.to_csv(

        PATH_RISK_FILE,

        index=False,

    )


def load_path_risk_scores():

    return pd.read_csv(

        PATH_RISK_FILE,

    )


###############################################################
# Priority Ranking
###############################################################

def save_priority_ranking(df):

    df.to_csv(

        PRIORITY_RANKING_FILE,

        index=False,

    )


def load_priority_ranking():

    return pd.read_csv(

        PRIORITY_RANKING_FILE,

    )


###############################################################
# Critical Assets
###############################################################

def save_critical_assets(df):

    df.to_csv(

        CRITICAL_ASSETS_FILE,

        index=False,

    )


def load_critical_assets():

    return pd.read_csv(

        CRITICAL_ASSETS_FILE,

    )


###############################################################
# Risk Summary
###############################################################

def save_risk_summary(summary):

    with open(

        RISK_SUMMARY_FILE,

        "w",

    ) as file:

        json.dump(

            summary,

            file,

            indent=4,

        )


def load_risk_summary():

    with open(

        RISK_SUMMARY_FILE,

        "r",

    ) as file:

        return json.load(file)


###############################################################
# Generic Utilities
###############################################################

def save_pickle(

    obj,

    filename,

):

    with open(

        filename,

        "wb",

    ) as file:

        pickle.dump(

            obj,

            file,

        )


def load_pickle(

    filename,

):

    with open(

        filename,

        "rb",

    ) as file:

        return pickle.load(

            file,

        )