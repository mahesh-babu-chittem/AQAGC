"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

A* Search Baseline

==============================================================
"""

from __future__ import annotations

import time
import heapq

import networkx as nx
import pandas as pd


class AStarBaseline:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph: nx.Graph,

        node_risk=None,

        weight="weight",

    ):

        self.graph = graph

        self.node_risk = node_risk

        self.weight = weight

        self.node_scores = {}

        self.execution_time = 0.0

        self.discovered_paths = []



    ####################################################################
    # Heuristic Function
    ####################################################################

    def heuristic(

        self,

        node,

    ):

        """
        Risk-aware heuristic.

        Higher risk nodes receive lower heuristic cost,
        encouraging exploration of critical regions.
        """

        if self.node_risk is None:

            return 0.0


        try:

            risk = self.node_risk.loc[

                self.node_risk["Node"]

                == node,

                "RiskScore"

            ].values[0]


            return 1.0 / (

                1.0 +

                risk

            )


        except Exception:

            return 0.0



    ####################################################################
    # A* Search
    ####################################################################

    def search(

        self,

        source,

    ):

        queue = []


        heapq.heappush(

            queue,

            (

                0.0,

                source,

                [

                    source

                ],

            )

        )


        visited = set()



        while queue:

            cost, current, path = heapq.heappop(

                queue

            )


            if current in visited:

                continue


            visited.add(

                current

            )


            self.node_scores[current] += 1


            self.discovered_paths.append(

                path

            )


            for neighbor in self.graph.neighbors(

                current

            ):

                if neighbor not in visited:


                    edge_cost = self.graph[current][neighbor].get(

                        self.weight,

                        1.0

                    )


                    new_cost = (

                        cost +

                        edge_cost

                    )


                    priority = (

                        new_cost +

                        self.heuristic(

                            neighbor

                        )

                    )


                    heapq.heappush(

                        queue,

                        (

                            priority,

                            neighbor,

                            path +

                            [

                                neighbor

                            ]

                        )

                    )



    ####################################################################
    # Execute
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.node_scores = {

            node: 0

            for node in self.graph.nodes()

        }


        self.discovered_paths = []


        for node in self.graph.nodes():

            self.search(

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


                    "AStar_Score":

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

                "AStar",


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