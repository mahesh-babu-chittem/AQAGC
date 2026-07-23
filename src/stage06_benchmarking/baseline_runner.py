"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Complete Benchmark Runner

==============================================================
"""

from __future__ import annotations

import time

import pandas as pd


# Classical baselines
from bfs_baseline import BFSBaseline
from dfs_baseline import DFSBaseline
from astar_baseline import AStarBaseline
from markov_baseline import MarkovBaseline


# Existing quantum walk implementations
from stage04_hybrid_scheduler.dtqw_walk import DTQWWalk
from stage04_hybrid_scheduler.ctqw_walk import CTQWWalk


# Existing AQAGC pipeline
from aqagc_runner import AQAGCRunner



class BenchmarkRunner:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph,

        config=None,

    ):

        self.graph = graph

        self.config = config


        self.results = {}

        self.execution_times = {}



    ####################################################################
    # Execute Single Method
    ####################################################################

    def execute_method(

        self,

        method_name,

        model,

    ):

        start = time.perf_counter()


        output = model.run()


        end = time.perf_counter()


        self.execution_times[method_name] = (

            end - start

        )


        self.results[method_name] = output


        return output



    ####################################################################
    # Classical Methods
    ####################################################################

    def run_classical_methods(self):

        methods = {


            "BFS":

                BFSBaseline(

                    self.graph

                ),



            "DFS":

                DFSBaseline(

                    self.graph

                ),



            "AStar":

                AStarBaseline(

                    self.graph

                ),



            "Markov":

                MarkovBaseline(

                    self.graph

                ),

        }



        for name, model in methods.items():

            self.execute_method(

                name,

                model

            )



    ####################################################################
    # Quantum Walk Methods
    ####################################################################

    def run_quantum_walk_methods(self):

        methods = {


            "DTQW":

                DTQWWalk(

                    self.graph

                ),



            "CTQW":

                CTQWWalk(

                    self.graph

                ),

        }



        for name, model in methods.items():

            self.execute_method(

                name,

                model

            )



    ####################################################################
    # AQAGC
    ####################################################################

    def run_aqagc(self):

        model = AQAGCRunner(

            graph=self.graph,

            config=self.config,

        )


        self.execute_method(

            "AQAGC",

            model

        )



    ####################################################################
    # Combine Outputs
    ####################################################################

    def combined_results(self):

        combined = []


        for method, result in self.results.items():


            dataframe = result.copy()


            dataframe["Method"] = method


            combined.append(

                dataframe

            )


        return pd.concat(

            combined,

            ignore_index=True

        )



    ####################################################################
    # Runtime Results
    ####################################################################

    def runtime_dataframe(self):

        return pd.DataFrame(

            {

                "Method":

                    list(

                        self.execution_times.keys()

                    ),


                "Execution_Time":

                    list(

                        self.execution_times.values()

                    ),

            }

        )



    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        return {

            "Methods":

                list(

                    self.results.keys()

                ),


            "Total_Methods":

                len(

                    self.results

                ),

        }



    ####################################################################
    # Complete Benchmark Execution
    ####################################################################

    def run(self):


        self.run_classical_methods()


        self.run_quantum_walk_methods()


        self.run_aqagc()


        return {

            "results":

                self.combined_results(),


            "runtime":

                self.runtime_dataframe(),


            "summary":

                self.summary(),

        }