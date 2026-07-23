"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Ablation Study Module

==============================================================
"""

from __future__ import annotations

import time

import pandas as pd



class AblationStudy:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph,

        aqagc_pipeline,

    ):

        self.graph = graph

        self.aqagc_pipeline = aqagc_pipeline

        self.results = []



    ####################################################################
    # Execute Variant
    ####################################################################

    def execute_variant(

        self,

        variant_name,

        pipeline,

    ):

        start = time.perf_counter()


        output = pipeline.run()


        end = time.perf_counter()


        execution_time = (

            end - start

        )


        return {

            "Variant":

                variant_name,


            "Output":

                output,


            "Execution_Time":

                execution_time,

        }



    ####################################################################
    # Full AQAGC
    ####################################################################

    def full_aqagc(self):

        return self.execute_variant(

            "Full_AQAGC",

            self.aqagc_pipeline,

        )



    ####################################################################
    # Without Adaptive Scheduler
    ####################################################################

    def without_adaptive_scheduler(

        self,

        pipeline,

    ):

        """

        Removes dynamic scheduler adaptation.

        Uses fixed DTQW/CTQW contribution.

        """

        pipeline.scheduler.adaptive = False


        return self.execute_variant(

            "Without_Adaptive_Scheduler",

            pipeline,

        )



    ####################################################################
    # Without DTQW
    ####################################################################

    def without_dtqw(

        self,

        pipeline,

    ):

        """

        Removes DTQW component and keeps CTQW.

        """

        pipeline.scheduler.use_dtqw = False


        return self.execute_variant(

            "Without_DTQW",

            pipeline,

        )



    ####################################################################
    # Without CTQW
    ####################################################################

    def without_ctqw(

        self,

        pipeline,

    ):

        """

        Removes CTQW component and keeps DTQW.

        """

        pipeline.scheduler.use_ctqw = False


        return self.execute_variant(

            "Without_CTQW",

            pipeline,

        )



    ####################################################################
    # Fixed Weighting
    ####################################################################

    def fixed_weighting(

        self,

        pipeline,

    ):

        """

        Replaces adaptive weighting with
        fixed DTQW/CTQW contribution.

        """

        pipeline.scheduler.fixed_weight = True


        return self.execute_variant(

            "Fixed_Weighting",

            pipeline,

        )



    ####################################################################
    # Collect Results
    ####################################################################

    def run_all(

        self,

        variants,

    ):

        """

        Parameters:

            variants:

                dictionary containing
                ablation pipelines


        Example:

            {

              "Full_AQAGC": pipeline,

              "Without_DTQW": pipeline

            }

        """


        for name, pipeline in variants.items():


            result = self.execute_variant(

                name,

                pipeline,

            )


            self.results.append(

                result

            )


        return self.dataframe()



    ####################################################################
    # Convert Results
    ####################################################################

    def dataframe(self):

        rows = []


        for item in self.results:


            rows.append(

                {

                    "Variant":

                        item["Variant"],


                    "Execution_Time":

                        item["Execution_Time"],

                }

            )


        return pd.DataFrame(

            rows

        )



    ####################################################################
    # Save Results
    ####################################################################

    def save(

        self,

        filepath,

    ):

        self.dataframe().to_csv(

            filepath,

            index=False

        )