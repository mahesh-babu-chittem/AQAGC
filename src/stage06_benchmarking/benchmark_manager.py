"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Benchmark Manager

==============================================================
"""

from __future__ import annotations

import pandas as pd

from baseline_runner import BenchmarkRunner

from io_utils import (
    save_csv,
)



class BenchmarkManager:

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


        self.runner = BenchmarkRunner(

            graph=self.graph,

            config=self.config,

        )


        self.results = None

        self.runtime = None

        self.summary = None



    ####################################################################
    # Execute Benchmark
    ####################################################################

    def execute(self):

        output = self.runner.run()


        self.results = output["results"]

        self.runtime = output["runtime"]

        self.summary = output["summary"]


        return output



    ####################################################################
    # Save Benchmark Results
    ####################################################################

    def save_results(self):

        if self.results is not None:

            save_csv(

                self.results,

                "benchmark_results.csv"

            )


        if self.runtime is not None:

            save_csv(

                self.runtime,

                "runtime_results.csv"

            )



    ####################################################################
    # Get Results
    ####################################################################

    def get_results(self):

        return self.results



    ####################################################################
    # Get Runtime
    ####################################################################

    def get_runtime(self):

        return self.runtime



    ####################################################################
    # Comparison Table
    ####################################################################

    def comparison_table(self):

        """

        Generates method-level summary.

        """

        if self.results is None:

            return None



        table = (

            self.results

            .groupby(

                "Method"

            )

            .size()

            .reset_index()

        )


        table.columns = [

            "Method",

            "Number_of_Ranked_Items"

        ]


        return table



    ####################################################################
    # Summary
    ####################################################################

    def report(self):

        return {

            "Methods":

                self.summary["Methods"],


            "Total_Methods":

                self.summary["Total_Methods"],


            "Runtime":

                self.runtime,


            "Comparison":

                self.comparison_table(),

        }



    ####################################################################
    # Public Runner
    ####################################################################

    def run(self):

        self.execute()

        self.save_results()

        return self.report()