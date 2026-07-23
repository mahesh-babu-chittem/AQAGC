"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Breadth-First Search (BFS) Baseline

==============================================================
"""

from __future__ import annotations

from collections import deque
import time

import networkx as nx
import pandas as pd


class BFSBaseline:

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
    # BFS Traversal
    ####################################################################

    def bfs(

        self,

        source,

    ):

        visited = set()

        queue = deque()

        queue.append(

            (

                source,

                [

                    source

                ]

            )

        )


        visited.add(source)


        while queue:

            current, path = queue.popleft()


            self.node_scores[current] += 1


            self.discovered_paths.append(

                path

            )


            for neighbor in self.graph.neighbors(

                current

            ):

                if neighbor not in visited:

                    visited.add(

                        neighbor

                    )


                    queue.append(

                        (

                            neighbor,

                            path + [neighbor]

                        )

                    )


    ####################################################################
    # Execute BFS
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.node_scores = {

            node: 0

            for node in self.graph.nodes()

        }


        self.discovered_paths = []


        for node in self.graph.nodes():

            self.bfs(

                node

            )


        end = time.perf_counter()


        self.execution_time = (

            end - start

        )


    ####################################################################
    # Normalize Scores
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
    # Generate Ranking
    ####################################################################

    def ranking(self):

        return sorted(

            self.node_scores.items(),

            key=lambda x: x[1],

            reverse=True

        )



    ####################################################################
    # Convert Results
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


                    "BFS_Score":

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

                "BFS",


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