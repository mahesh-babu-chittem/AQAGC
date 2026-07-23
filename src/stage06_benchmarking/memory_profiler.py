"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Memory Profiler

==============================================================
"""

from __future__ import annotations

import tracemalloc
import time

import pandas as pd



class MemoryProfiler:



    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.records = []



    ####################################################################
    # Measure Memory Usage
    ####################################################################

    def measure(

        self,

        method_name,

        function,

        *args,

        **kwargs,

    ):

        """
        Executes a method while tracking memory usage.

        Returns:
            method output
        """

        tracemalloc.start()


        start_time = time.perf_counter()


        result = function(

            *args,

            **kwargs

        )


        end_time = time.perf_counter()


        current_memory, peak_memory = tracemalloc.get_traced_memory()


        tracemalloc.stop()



        self.records.append(

            {

                "Method":

                    method_name,


                "Execution_Time":

                    end_time - start_time,


                "Current_Memory_Bytes":

                    current_memory,


                "Peak_Memory_Bytes":

                    peak_memory,


                "Peak_Memory_MB":

                    peak_memory /

                    (

                        1024 ** 2

                    ),

            }

        )


        return result



    ####################################################################
    # Benchmark Multiple Methods
    ####################################################################

    def benchmark(

        self,

        methods,

    ):

        """
        Parameters:

            methods = {

                "BFS": bfs_function,

                "AQAGC": aqagc_function

            }

        """

        for name, function in methods.items():

            self.measure(

                name,

                function

            )



    ####################################################################
    # DataFrame Output
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