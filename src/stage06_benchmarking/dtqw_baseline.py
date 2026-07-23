"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Discrete-Time Quantum Walk (DTQW) Baseline

==============================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd


class DTQWBaseline:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph,

        walk_steps=100,

    ):

        self.graph = graph

        self.walk_steps = walk_steps

        self.nodes = list(

            graph.nodes()

        )

        self.node_index = {

            node: idx

            for idx, node in enumerate(

                self.nodes

            )

        }


        self.probability_distribution = None

        self.node_scores = {}

        self.execution_time = 0.0



    ####################################################################
    # Initial State
    ####################################################################

    def initialize_state(self):

        n = len(

            self.nodes

        )


        state = np.zeros(

            n,

            dtype=np.complex128

        )


        state[0] = 1.0 + 0j


        return state



    ####################################################################
    # Transition Operator
    ####################################################################

    def build_transition_operator(self):

        n = len(

            self.nodes

        )


        operator = np.zeros(

            (

                n,

                n

            ),

            dtype=np.complex128

        )


        for node in self.graph.nodes():

            i = self.node_index[node]


            neighbors = list(

                self.graph.neighbors(

                    node

                )

            )


            if len(neighbors) == 0:

                operator[i][i] = 1.0

                continue


            amplitude = (

                1 /

                np.sqrt(

                    len(neighbors)

                )

            )


            for neighbor in neighbors:

                j = self.node_index[neighbor]

                operator[j][i] = amplitude



        return operator



    ####################################################################
    # Quantum Walk Evolution
    ####################################################################

    def evolve(self):

        operator = self.build_transition_operator()


        state = self.initialize_state()


        for _ in range(

            self.walk_steps

        ):

            state = operator @ state


            norm = np.linalg.norm(

                state

            )


            if norm != 0:

                state = state / norm



        probabilities = np.abs(

            state

        ) ** 2


        self.probability_distribution = probabilities



    ####################################################################
    # Execute
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.evolve()


        self.node_scores = {

            node:

            float(

                self.probability_distribution[index]

            )

            for node, index in self.node_index.items()

        }


        end = time.perf_counter()


        self.execution_time = (

            end - start

        )



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


                    "DTQW_Score":

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

                "DTQW",


            "Nodes":

                len(

                    self.nodes

                ),


            "WalkSteps":

                self.walk_steps,


            "Execution_Time":

                self.execution_time,

        }



    ####################################################################
    # Runner
    ####################################################################

    def run(self):

        self.execute()

        return self.results_dataframe()