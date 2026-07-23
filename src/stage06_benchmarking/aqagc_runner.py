"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

AQAGC Existing Pipeline Runner

==============================================================
"""

from __future__ import annotations

import time

import pandas as pd


# Stage 04
from stage04_hybrid_scheduler.scheduler_pipeline import (
    SchedulerPipeline,
)


# Stage 05
from stage05_risk_prioritization.risk_prioritization_pipeline import (
    RiskPrioritizationPipeline,
)



class AQAGCRunner:

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


        self.scheduler_output = None

        self.risk_output = None

        self.final_results = None


        self.execution_time = 0.0



    ####################################################################
    # Execute Stage 04
    ####################################################################

    def execute_hybrid_scheduler(self):

        scheduler = SchedulerPipeline(

            graph=self.graph,

            config=self.config,

        )


        self.scheduler_output = scheduler.run()


        return self.scheduler_output



    ####################################################################
    # Execute Stage 05
    ####################################################################

    def execute_risk_prioritization(self):

        risk_pipeline = RiskPrioritizationPipeline(

            graph=self.graph,

            scheduler_output=self.scheduler_output,

            config=self.config,

        )


        self.risk_output = risk_pipeline.run()


        return self.risk_output



    ####################################################################
    # Format Benchmark Output
    ####################################################################

    def prepare_results(self):

        """
        Converts AQAGC output into a common
        benchmarking format.
        """


        if isinstance(

            self.risk_output,

            pd.DataFrame

        ):

            results = self.risk_output.copy()


        elif isinstance(

            self.risk_output,

            dict

        ):

            results = pd.DataFrame(

                self.risk_output

            )


        else:

            results = pd.DataFrame(

                self.risk_output

            )


        if "Rank" not in results.columns:

            results.insert(

                0,

                "Rank",

                range(

                    1,

                    len(results)+1

                )

            )


        results["Method"] = "AQAGC"


        return results



    ####################################################################
    # Execute Complete AQAGC
    ####################################################################

    def execute(self):

        start = time.perf_counter()


        self.execute_hybrid_scheduler()


        self.execute_risk_prioritization()


        self.final_results = self.prepare_results()


        end = time.perf_counter()


        self.execution_time = (

            end - start

        )


        return self.final_results



    ####################################################################
    # Results
    ####################################################################

    def results_dataframe(self):

        return self.final_results



    ####################################################################
    # Summary
    ####################################################################

    def summary(self):

        return {

            "Method":

                "AQAGC",


            "Execution_Time":

                self.execution_time,


            "Number_of_Ranked_Items":

                len(

                    self.final_results

                )

                if self.final_results is not None

                else 0,

        }



    ####################################################################
    # Public Runner
    ####################################################################

    def run(self):

        return self.execute()