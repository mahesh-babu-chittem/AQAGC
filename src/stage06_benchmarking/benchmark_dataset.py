"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Benchmark Dataset Loader

==============================================================
"""

from __future__ import annotations

import pandas as pd

from io_utils import (
    load_node_risk_scores,
    load_edge_risk_scores,
    load_path_risk_scores,
    load_priority_attack_paths,
    load_ground_truth_paths,
)


class BenchmarkDataset:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.node_risk = None

        self.edge_risk = None

        self.path_risk = None

        self.priority_paths = None

        self.ground_truth = None


    ####################################################################
    # Load Dataset
    ####################################################################

    def load(self):

        self.node_risk = load_node_risk_scores()

        self.edge_risk = load_edge_risk_scores()

        self.path_risk = load_path_risk_scores()

        self.priority_paths = load_priority_attack_paths()

        self.ground_truth = load_ground_truth_paths()

        return self


    ####################################################################
    # Node Data
    ####################################################################

    def get_node_risk(self):

        return self.node_risk.copy()



    ####################################################################
    # Edge Data
    ####################################################################

    def get_edge_risk(self):

        return self.edge_risk.copy()



    ####################################################################
    # Path Data
    ####################################################################

    def get_path_risk(self):

        return self.path_risk.copy()



    ####################################################################
    # Priority Paths
    ####################################################################

    def get_priority_paths(self):

        return self.priority_paths.copy()



    ####################################################################
    # Ground Truth
    ####################################################################

    def get_ground_truth(self):

        return self.ground_truth.copy()



    ####################################################################
    # Dataset Statistics
    ####################################################################

    def statistics(self):

        return {

            "Number_of_Nodes":

                len(self.node_risk),


            "Number_of_Edges":

                len(self.edge_risk),


            "Number_of_Paths":

                len(self.path_risk),


            "Priority_Attack_Paths":

                len(self.priority_paths),


            "Ground_Truth_Paths":

                len(self.ground_truth),

        }



    ####################################################################
    # Validation
    ####################################################################

    def validate(self):

        missing = []

        if self.node_risk is None:

            missing.append(

                "node_risk_scores"

            )

        if self.edge_risk is None:

            missing.append(

                "edge_risk_scores"

            )

        if self.path_risk is None:

            missing.append(

                "path_risk_scores"

            )

        if self.priority_paths is None:

            missing.append(

                "priority_attack_paths"

            )

        if self.ground_truth is None:

            missing.append(

                "ground_truth_paths"

            )


        return {

            "valid":

                len(missing) == 0,

            "missing":

                missing,

        }



    ####################################################################
    # Complete Dataset Package
    ####################################################################

    def package(self):

        return {

            "node_risk":

                self.node_risk,


            "edge_risk":

                self.edge_risk,


            "path_risk":

                self.path_risk,


            "priority_paths":

                self.priority_paths,


            "ground_truth":

                self.ground_truth,

        }