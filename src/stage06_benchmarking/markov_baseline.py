"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Markov Attack Graph Baseline

==============================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd
import networkx as nx



class MarkovBaseline:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph: nx.Graph,

        weight="weight",

        max_iterations=1000,

        tolerance=1e-8,

    ):

        self.graph = graph

        self.weight = weight

        self.max_iterations = max_iterations

        self.tolerance = tolerance


        self.transition_matrix = None

        self.node_order = []

        self.node_scores = {}

        self.execution_time = 0.0



    ####################################################################
    # Build Transition Matrix
    ####################################################################

    def build_transition_matrix(self):

        self.node_order = list(

            self.graph.nodes()

        )


        n = len(

            self.node_order

        )


        index = {

            node: i

            for i, node in enumerate(

                self.node_order

            )

        }


        matrix = np.zeros(

            (

                n,

                n

            )

        )


        for node in self.graph.nodes():

            i = index[node]


            neighbors = list(

                self.graph.neighbors(

                    node

                )

            )


            if len(neighbors) == 0:

                matrix[i][i] = 1.0

                continue


            total_weight = 0.0


            weights = {}


            for neighbor in neighbors:

                edge_weight = self.graph[node][neighbor].get(

                    self.weight,

                    1.0

                )

                weights[neighbor] = edge_weight

                total_weight += edge_weight



            for neighbor, value in weights.items():

                j = index[neighbor]

                matrix[i][j] = (

                    value /

                    total_weight

                )


        self.transition_matrix = matrix



    ####################################################################
    # Power Iteration
    ####################################################################

    def compute_stationary_distribution(self):

        n = len(

            self.node_order

        )


        probability = np.ones(

            n

        ) / n



        for _ in range(

            self.max_iterations

        ):

            new_probability = (

                probability @

                self.transition_matrix

            )


            difference = np.linalg.norm(

                new_probability -

                probability

            )


            probability = new_probability


            if difference < self.tolerance:

                break



        self.node_scores = {

            node:

            float(

                probability[i]

            )

            for i, node in enumerate(

                self.node_order

            )

        }



    ####################################################################
    # Execute
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.build_transition_matrix()


        self.compute_stationary_distribution()


        end = time.perf_counter()


        self.execution_time = (

            end - start

        )



    ####################################################################
    # Normalize
    ####################################################################

    def normalize_scores(self):

        maximum = max(

            self.node_scores.values()

        )


        if maximum == 0:

            maximum = 1


        for node in self.node_scores:

            self.node_scores[node] /= maximum



    ####################################################################
    # Ranking
    ####################################################################

    def ranking(self):

        return sorted(

            self.node_scores.items(),

            key=lambda x: x[1],

            reverse=True

        )



    ####################################################################
    # Results DataFrame
    ####################################################################

    def results_dataframe(self):

        rows = []


        for rank, (node, score) in enumerate(

            self.ranking(),

            start=1

        ):

            rows.append(

                {

                    "Rank":

                        rank,


                    "Node":

                        node,


                    "Markov_Score":

                        score,

                }

            )


        return pd.DataFrame(

            rows

        )



    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        return {

            "Method":

                "Markov",


            "Nodes":

                self.graph.number_of_nodes(),


            "Edges":

                self.graph.number_of_edges(),


            "Execution_Time":

                self.execution_time,

        }



    ####################################################################
    # Runner
    ####################################################################

    def run(self):

        self.execute()

        self.normalize_scores()

        return self.results_dataframe()