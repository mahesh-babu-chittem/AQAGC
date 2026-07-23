"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Depth-First Search (DFS) Baseline

==============================================================
"""

from __future__ import annotations

import time

import networkx as nx
import pandas as pd


class DFSBaseline:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph: nx.Graph,

    ):

        self.graph = graph

        self.node_scores = {}

        self.execution_time = 0.0

        self.discovered_paths = []



    ####################################################################
    # DFS Traversal
    ####################################################################

    def dfs(

        self,

        current,

        visited,

        path,

    ):

        visited.add(

            current

        )


        self.node_scores[current] += 1


        current_path = path + [

            current

        ]


        self.discovered_paths.append(

            current_path

        )


        for neighbor in self.graph.neighbors(

            current

        ):

            if neighbor not in visited:

                self.dfs(

                    neighbor,

                    visited.copy(),

                    current_path,

                )



    ####################################################################
    # Execute DFS
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.node_scores = {

            node: 0

            for node in self.graph.nodes()

        }


        self.discovered_paths = []


        for node in self.graph.nodes():

            self.dfs(

                node,

                set(),

                [],

            )


        end = time.perf_counter()


        self.execution_time = (

            end - start

        )



    ####################################################################
    # Normalize Node Scores
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


                    "DFS_Score":

                        score,

                }

            )


        return pd.DataFrame(

            rows

        )



    ####################################################################
    # Retrieve Paths
    ####################################################################

    def get_paths(self):

        return self.discovered_paths



    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        return {

            "Method":

                "DFS",


            "Nodes":

                self.graph.number_of_nodes(),


            "Edges":

                self.graph.number_of_edges(),


            "Execution_Time":

                self.execution_time,


            "Discovered_Paths":

                len(

                    self.discovered_paths

                ),

        }



    ####################################################################
    # Public Runner
    ####################################################################

    def run(self):

        self.execute()

        self.normalize_scores()

        return self.results_dataframe()