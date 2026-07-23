"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Input / Output Utility Functions

==============================================================
"""

from __future__ import annotations

import json

import pandas as pd

from config import *


####################################################################
# Stage-05 Output Loaders
####################################################################

def load_node_risk_scores():

    return pd.read_csv(

        NODE_RISK_FILE

    )


def load_edge_risk_scores():

    return pd.read_csv(

        EDGE_RISK_FILE

    )


def load_path_risk_scores():

    return pd.read_csv(

        PATH_RISK_FILE

    )


def load_priority_attack_paths():

    return pd.read_csv(

        PRIORITY_PATH_FILE

    )


def load_ground_truth_paths():

    return pd.read_csv(

        GROUND_TRUTH_FILE

    )


####################################################################
# Generic CSV Utilities
####################################################################

def save_csv(

    dataframe,

    filepath,

):

    dataframe.to_csv(

        filepath,

        index=False

    )



def load_csv(

    filepath,

):

    return pd.read_csv(

        filepath

    )


####################################################################
# Baseline Results
####################################################################

def save_baseline_result(

    method_name,

    dataframe,

):

    filepath = (

        BASELINE_RESULTS_DIR /

        f"{method_name.lower()}_results.csv"

    )

    save_csv(

        dataframe,

        filepath

    )



def load_baseline_result(

    method_name,

):

    filepath = (

        BASELINE_RESULTS_DIR /

        f"{method_name.lower()}_results.csv"

    )

    return load_csv(

        filepath

    )


####################################################################
# AQAGC Results
####################################################################

def save_aqagc_result(

    dataframe,

):

    filepath = (

        AQAGC_RESULTS_DIR /

        "aqagc_results.csv"

    )

    save_csv(

        dataframe,

        filepath

    )


def load_aqagc_result():

    filepath = (

        AQAGC_RESULTS_DIR /

        "aqagc_results.csv"

    )

    return load_csv(

        filepath

    )


####################################################################
# Metrics
####################################################################

def save_metrics(

    dataframe,

):

    filepath = (

        METRICS_DIR /

        "benchmark_metrics.csv"

    )

    save_csv(

        dataframe,

        filepath

    )


def load_metrics():

    filepath = (

        METRICS_DIR /

        "benchmark_metrics.csv"

    )

    return load_csv(

        filepath

    )


####################################################################
# Statistics
####################################################################

def save_statistics(

    dataframe,

    filename="statistical_results.csv"

):

    filepath = (

        STATISTICS_DIR /

        filename

    )

    save_csv(

        dataframe,

        filepath

    )


def load_statistics(

    filename="statistical_results.csv"

):

    filepath = (

        STATISTICS_DIR /

        filename

    )

    return load_csv(

        filepath

    )


####################################################################
# Robustness Results
####################################################################

def save_robustness_results(

    dataframe,

):

    filepath = (

        ROBUSTNESS_DIR /

        "robustness_results.csv"

    )

    save_csv(

        dataframe,

        filepath

    )


def load_robustness_results():

    filepath = (

        ROBUSTNESS_DIR /

        "robustness_results.csv"

    )

    return load_csv(

        filepath

    )


####################################################################
# Ablation Results
####################################################################

def save_ablation_results(

    dataframe,

):

    filepath = (

        ABLATION_DIR /

        "ablation_results.csv"

    )

    save_csv(

        dataframe,

        filepath

    )


def load_ablation_results():

    filepath = (

        ABLATION_DIR /

        "ablation_results.csv"

    )

    return load_csv(

        filepath

    )


####################################################################
# JSON Utilities
####################################################################

def save_json(

    data,

    filepath,

):

    with open(

        filepath,

        "w"

    ) as file:

        json.dump(

            data,

            file,

            indent=4

        )


def load_json(

    filepath,

):

    with open(

        filepath,

        "r"

    ) as file:

        return json.load(

            file

        )