"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Continuous-Time Quantum Walk (CTQW) Baseline

==============================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd



class CTQWBaseline:
    
    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph,

        evolution_time=1.0,

        steps=100,

    ):

        self.graph = graph

        self.evolution_time = evolution_time

        self.steps = steps


        self.nodes = list(

            graph.nodes()

        )


        self.node_index = {

            node: index

            for index, node in enumerate(

                self.nodes

            )

        }


        self.hamiltonian = None

        self.state = None

        self.node_scores = {}

        self.execution_time = 0.0



    ####################################################################
    # Construct Hamiltonian
    ####################################################################

    def build_hamiltonian(self):

        adjacency = nx.to_numpy_array(

            self.graph,

            nodelist=self.nodes,

        )


        self.hamiltonian = adjacency.astype(

            complex

        )



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


        self.state[0] = 1.0 + 0j



    ####################################################################
    # Matrix Exponential Evolution
    ####################################################################

    def evolve(self):

        from scipy.linalg import expm


        evolution_operator = expm(

            -1j *

            self.hamiltonian *

            self.evolution_time

        )


        self.state = (

            evolution_operator @

            self.state

        )


        norm = np.linalg.norm(

            self.state

        )


        if norm != 0:

            self.state = (

                self.state /

                norm

            )



    ####################################################################
    # Measurement
    ####################################################################

    def measure(self):

        probabilities = np.abs(

            self.state

        ) ** 2


        self.node_scores = {

            node:

            float(

                probabilities[index]

            )

            for node, index in self.node_index.items()

        }



    ####################################################################
    # Execute
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.build_hamiltonian()


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


                    "CTQW_Score":

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

                "CTQW",


            "Nodes":

                len(

                    self.nodes

                ),


            "Evolution_Time":

                self.evolution_time,


            "Execution_Time":

                self.execution_time,

        }



    ####################################################################
    # Runner
    ####################################################################

    def run(self):

        self.execute()

        return self.results_dataframe()