"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Scalability Analysis

==============================================================
"""

from __future__ import annotations

import time

import pandas as pd



class ScalabilityAnalyzer:



    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.records = []



    ####################################################################
    # Single Scale Evaluation
    ####################################################################

    def evaluate_scale(

        self,

        graph_size,

        edge_count,

        method_name,

        execution_time,

        memory_usage=None,

        alpha_mean=None,

    ):

        """
        Stores scalability result for one experiment.
        """

        self.records.append(

            {

                "Graph_Size":

                    graph_size,


                "Edge_Count":

                    edge_count,


                "Method":

                    method_name,


                "Execution_Time":

                    execution_time,


                "Memory_Usage":

                    memory_usage,


                "Mean_Alpha":

                    alpha_mean,

            }

        )



    ####################################################################
    # Run Experiment
    ####################################################################

    def run_experiment(

        self,

        graph_generator,

        sizes,

        methods,

    ):


        for size in sizes:


            graph = graph_generator(

                size

            )


            for name, method in methods.items():


                start = time.perf_counter()


                method.graph = graph


                method.run()


                end = time.perf_counter()


                self.evaluate_scale(

                    graph_size=size,

                    edge_count=graph.number_of_edges(),

                    method_name=name,

                    execution_time=end-start,

                )



    ####################################################################
    # Runtime Scaling Table
    ####################################################################

    def runtime_scaling(self):

        dataframe = pd.DataFrame(

            self.records

        )


        return dataframe[

            [

                "Graph_Size",

                "Method",

                "Execution_Time",

            ]

        ]



    ####################################################################
    # Memory Scaling Table
    ####################################################################

    def memory_scaling(self):

        dataframe = pd.DataFrame(

            self.records

        )


        return dataframe[

            [

                "Graph_Size",

                "Method",

                "Memory_Usage",

            ]

        ]



    ####################################################################
    # Adaptive Scheduler Analysis
    ####################################################################

    def scheduler_analysis(self):

        dataframe = pd.DataFrame(

            self.records

        )


        return dataframe[

            [

                "Graph_Size",

                "Method",

                "Mean_Alpha",

            ]

        ]



    ####################################################################
    # Complete Report
    ####################################################################

    def report(self):

        return pd.DataFrame(

            self.records

        )



    ####################################################################
    # Save
    ####################################################################

    def save(

        self,

        filepath,

    ):

        self.report().to_csv(

            filepath,

            index=False

        )