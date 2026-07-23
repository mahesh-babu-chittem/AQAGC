"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Runtime Profiler

==============================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd



class RuntimeProfiler:


    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.records = []



    ####################################################################
    # Measure Single Execution
    ####################################################################

    def measure(

        self,

        method_name,

        function,

        *args,

        **kwargs,

    ):

        start = time.perf_counter()


        result = function(

            *args,

            **kwargs

        )


        end = time.perf_counter()


        execution_time = (

            end - start

        )


        self.records.append(

            {

                "Method":

                    method_name,


                "Execution_Time":

                    execution_time,

            }

        )


        return result



    ####################################################################
    # Multiple Runs
    ####################################################################

    def benchmark(

        self,

        method_name,

        function,

        repetitions=10,

        *args,

        **kwargs,

    ):

        runtimes = []


        for _ in range(

            repetitions

        ):

            start = time.perf_counter()


            function(

                *args,

                **kwargs

            )


            end = time.perf_counter()


            runtimes.append(

                end - start

            )



        summary = {


            "Method":

                method_name,


            "Runs":

                repetitions,


            "Mean_Runtime":

                float(

                    np.mean(

                        runtimes

                    )

                ),


            "Std_Runtime":

                float(

                    np.std(

                        runtimes

                    )

                ),


            "Min_Runtime":

                float(

                    np.min(

                        runtimes

                    ) ),

            
            "Max_Runtime":

                float(

                    np.max(

                        runtimes

                    ) ),

        }


        self.records.append(

            summary

        )


        return summary



    ####################################################################
    # Attack Path Discovery Time
    ####################################################################

    def apdt(

        self,

        start_time,

        discovery_time,

    ):

        """
        Attack Path Discovery Time.

        APDT = time required to discover
        critical attack paths.
        """

        return (

            discovery_time -

            start_time

        )



    ####################################################################
    # Runtime DataFrame
    ####################################################################

    def dataframe(self):

        return pd.DataFrame(

            self.records

        )



    ####################################################################
    # Reset
    ####################################################################

    def reset(self):

        self.records = []