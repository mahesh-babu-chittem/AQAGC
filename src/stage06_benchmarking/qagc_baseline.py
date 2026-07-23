"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Original Quantum Attack Graph Compiler (QAGC) Baseline

==============================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd



class QAGCBaseline:

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

            node: index

            for index, node in enumerate(

                self.nodes

            )

        }


        self.state = None

        self.node_scores = {}

        self.execution_time = 0.0



    ####################################################################
    # Initial Quantum State
    ####################################################################

    def initialize_state(self):

        dimension = len(

            self.nodes

        )


        self.state = np.zeros(

            dimension,

            dtype=np.complex128

        )


        if dimension > 0:

            self.state[0] = 1.0 + 0j



    ####################################################################
    # Fixed Quantum Transition Operator
    ####################################################################

    def build_operator(self):

        dimension = len(

            self.nodes

        )


        operator = np.zeros(

            (

                dimension,

                dimension

            ),

            dtype=np.complex128

        )


        for node in self.nodes:

            source = self.node_index[node]


            neighbors = list(

                self.graph.neighbors(

                    node

                )

            )


            if len(neighbors) == 0:

                operator[source][source] = 1.0

                continue



            amplitude = (

                1 /

                np.sqrt(

                    len(neighbors)

                )

            )


            for neighbor in neighbors:

                target = self.node_index[neighbor]


                operator[target][source] = amplitude



        return operator



    ####################################################################
    # Quantum Evolution
    ####################################################################

    def evolve(self):

        operator = self.build_operator()


        for _ in range(

            self.walk_steps

        ):

            self.state = (

                operator @

                self.state

            )


            norm = np.linalg.norm(

                self.state

            )


            if norm != 0:

                self.state /= norm



    ####################################################################
    # Measurement
    ####################################################################

    def measure(self):

        probability = np.abs(

            self.state

        ) ** 2


        self.node_scores = {

            node:

            float(

                probability[index]

            )

            for node, index in self.node_index.items()

        }



    ####################################################################
    # Execute
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.initialize_state()


        self.evolve()


        self.measure()


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


                    "QAGC_Score":

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

                "QAGC",


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