"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Robustness Analysis

==============================================================
"""

from __future__ import annotations

import copy
import random

import networkx as nx
import pandas as pd



class RobustnessAnalyzer:


    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph,

    ):

        self.original_graph = graph

        self.records = []



    ####################################################################
    # Random Edge Removal
    ####################################################################

    def random_edge_removal(

        self,

        removal_ratio=0.1,

    ):

        """

        Removes a percentage of edges randomly.

        """

        graph = copy.deepcopy(

            self.original_graph

        )


        edges = list(

            graph.edges()

        )


        remove_count = int(

            len(edges)

            *

            removal_ratio

        )


        removed_edges = random.sample(

            edges,

            remove_count

        )


        graph.remove_edges_from(

            removed_edges

        )


        return graph



    ####################################################################
    # Missing Vulnerability Information
    ####################################################################

    def remove_vulnerability_information(

        self,

        node_data,

        missing_ratio=0.1,

    ):

        """

        Simulates missing vulnerability attributes.

        """

        data = node_data.copy()


        count = int(

            len(data)

            *

            missing_ratio

        )


        selected = random.sample(

            list(data.index),

            count

        )


        for index in selected:

            data.loc[

                index,

                "RiskScore"

            ] = None


        return data



    ####################################################################
    # Noisy Transition Weights
    ####################################################################

    def add_transition_noise(

        self,

        graph,

        noise_level=0.05,

    ):

        """

        Adds noise to attack-transition weights.

        """

        noisy_graph = copy.deepcopy(

            graph

        )


        for u, v, data in noisy_graph.edges(

            data=True

        ):


            weight = data.get(

                "weight",

                1.0

            )


            noise = random.uniform(

                -noise_level,

                noise_level

            )


            data["weight"] = max(

                0.01,

                weight + noise

            )


        return noisy_graph



    ####################################################################
    # Partial Graph Visibility
    ####################################################################

    def partial_graph_visibility(

        self,

        visibility_ratio=0.8,

    ):

        """

        Simulates incomplete graph observation.

        """

        graph = copy.deepcopy(

            self.original_graph

        )


        nodes = list(

            graph.nodes()

        )


        keep_count = int(

            len(nodes)

            *

            visibility_ratio

        )


        visible_nodes = random.sample(

            nodes,

            keep_count

        )


        return graph.subgraph(

            visible_nodes

        ).copy()



    ####################################################################
    # Robustness Degradation
    ####################################################################

    def robustness_degradation(

        self,

        original_score,

        degraded_score,

    ):

        """

        RD =

        (Original - Degraded)

        / Original


        """

        if original_score == 0:

            return 0.0


        return (

            original_score -

            degraded_score

        ) / original_score



    ####################################################################
    # Record Experiment
    ####################################################################

    def record(

        self,

        method,

        scenario,

        metric,

        value,

    ):

        self.records.append(

            {

                "Method":

                    method,


                "Scenario":

                    scenario,


                "Metric":

                    metric,


                "Value":

                    value,

            }

        )



    ####################################################################
    # Results DataFrame
    ####################################################################

    def dataframe(self):

        return pd.DataFrame(

            self.records

        )



    ####################################################################
    # Save Results
    ####################################################################

    def save(

        self,

        filepath,

    ):

        self.dataframe().to_csv(

            filepath,

            index=False

        )