"""
==============================================================
AQAGC

Stage 07

Results Generation

Scalability Evaluation

==============================================================

"""


from __future__ import annotations


import os
import time
import json
import tracemalloc


import pandas as pd
import matplotlib.pyplot as plt



class ScalabilityAnalysis:
    """
    Scalability evaluation of AQAGC
    """



    ##############################################################
    # Initialization
    ##############################################################

    def __init__(

        self,

        loader,

        output_dir="outputs/scalability"

    ):


        self.loader = loader


        self.output_dir = output_dir



        self.table_dir = os.path.join(

            output_dir,

            "tables"

        )


        self.figure_dir = os.path.join(

            output_dir,

            "figures"

        )


        self.value_dir = os.path.join(

            output_dir,

            "values"

        )


        os.makedirs(

            self.table_dir,

            exist_ok=True

        )


        os.makedirs(

            self.figure_dir,

            exist_ok=True

        )


        os.makedirs(

            self.value_dir,

            exist_ok=True

        )


        self.methods = [

            "BFS",

            "DFS",

            "AStar",

            "Markov",

            "DTQW",

            "CTQW",

            "QAGC",

            "AQAGC"

        ]



    ##############################################################
    # Runtime and Memory Measurement
    ##############################################################

    def execute_profile(

        self,

        model

    ):


        tracemalloc.start()


        start = time.perf_counter()


        model.run()


        end = time.perf_counter()



        current, peak = tracemalloc.get_traced_memory()


        tracemalloc.stop()



        runtime = (

            end-start

        )



        memory_mb = (

            peak /

            (

                1024 *

                1024

            )

        )


        return runtime, memory_mb



    ##############################################################
    # Run Experiments
    ##############################################################

    def run_experiment(self):


        runtime_results=[]

        memory_results=[]



        for size in self.loader.graph_sizes():


            print(

                f"Scalability evaluation: {size} nodes"

            )



            graphs = self.loader.load_graphs(

                size

            )



            runtime_sum={

                method: []

                for method in self.methods

            }



            memory_sum={

                method: []

                for method in self.methods

            }



            for graph in graphs:


                models = self.loader.get_all_models(

                    graph

                )



                for name,model in models.items():


                    runtime, memory = self.execute_profile(

                        model

                    )


                    runtime_sum[name].append(

                        runtime

                    )


                    memory_sum[name].append(

                        memory

                    )



            for method in self.methods:


                runtime_results.append(

                    {

                    "Method":

                        method,


                    "Graph_Size":

                        size,


                    "Runtime":

                        sum(

                            runtime_sum[method]

                        )

                        /

                        len(

                            runtime_sum[method]

                        )

                    }

                )


                memory_results.append(

                    {

                    "Method":

                        method,


                    "Graph_Size":

                        size,


                    "Memory_MB":

                        sum(

                            memory_sum[method]

                        )

                        /

                        len(

                            memory_sum[method]

                        )

                    }

                )



        return (

            pd.DataFrame(runtime_results),

            pd.DataFrame(memory_results)

        )



    ##############################################################
    # Runtime Growth Factor
    ##############################################################

    def runtime_growth(

        self,

        runtime_df

    ):


        growth = runtime_df.copy()



        growth["Runtime_Growth"] = 0.0



        for method in self.methods:


            base = growth[

                (

                    growth.Method == method

                )

                &

                (

                    growth.Graph_Size == 50

                )

            ]["Runtime"].iloc[0]



            idx = growth.Method == method



            growth.loc[idx,"Runtime_Growth"] = (

                growth.loc[idx,"Runtime"]

                /

                base

            )



        return growth



    ##############################################################
    # Generate Tables
    ##############################################################

    def generate_tables(

        self,

        runtime,

        memory

    ):


        memory_table = memory.pivot(

            index="Method",

            columns="Graph_Size",

            values="Memory_MB"

        )


        runtime_table = runtime.pivot(

            index="Method",

            columns="Graph_Size",

            values="Runtime_Growth"

        )



        memory_table.to_latex(

            os.path.join(

                self.table_dir,

                "memory_results.tex"

            ),

            float_format="%.2f"

        )



        runtime_table.to_latex(

            os.path.join(

                self.table_dir,

                "runtime_growth_results.tex"

            ),

            float_format="%.2f"

        )



        return (

            memory_table,

            runtime_table

        )



    ##############################################################
    # Heatmap
    ##############################################################

    def generate_heatmap(

        self,

        memory_table

    ):


        plt.figure(

            figsize=(9,6)

        )


        plt.imshow(

            memory_table.values,

            aspect="auto"

        )


        plt.xticks(

            range(

                len(memory_table.columns)

            ),

            memory_table.columns

        )


        plt.yticks(

            range(

                len(memory_table.index)

            ),

            memory_table.index

        )


        plt.xlabel(

            "Graph Size"

        )


        plt.ylabel(

            "Method"

        )


        plt.colorbar(

            label="Memory MB"

        )


        plt.tight_layout()



        plt.savefig(

            os.path.join(

                self.figure_dir,

                "AQAGC_Scalability_Heatmap.png"

            ),

            dpi=300

        )


        plt.close()



    ##############################################################
    # Save Values
    ##############################################################

    def save_values(

        self,

        memory_table,

        runtime_table

    ):


        values = {


            "AQAGC_memory_5000":

                float(

                    memory_table.loc[

                        "AQAGC",

                        5000

                    ]

                ),


            "AQAGC_runtime_growth_5000":

                float(

                    runtime_table.loc[

                        "AQAGC",

                        5000

                    ]

                )

        }



        with open(

            os.path.join(

                self.value_dir,

                "scalability_values.json"

            ),

            "w"

        ) as file:


            json.dump(

                values,

                file,

                indent=4

            )



    ##############################################################
    # Run
    ##############################################################

    def run(self):


        runtime, memory = self.run_experiment()



        growth = self.runtime_growth(

            runtime

        )



        memory_table, runtime_table = self.generate_tables(

            growth,

            memory

        )



        self.generate_heatmap(

            memory_table

        )



        self.save_values(

            memory_table,

            runtime_table

        )



        return {


            "Memory":

                memory_table,


            "Runtime":

                runtime_table

        }