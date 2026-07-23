"""
==============================================================
AQAGC

Stage 07

Results Generation

Attack Path Discovery Performance Analysis


==============================================================
"""


from __future__ import annotations


import os
import json
import time


import pandas as pd
import matplotlib.pyplot as plt



class APDTAnalysis:
    """
    Attack Path Discovery Performance


    Evaluates:

        - Attack Path Discovery Time (APDT)
        - Quantum Simulation Efficiency Gain (QSEG)


    """



    ##################################################################
    # Initialization
    ##################################################################

    def __init__(

        self,

        loader,

        output_dir="outputs/apdt"

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



        self.graph_sizes = (

            self.loader.graph_sizes()

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



        self.results = []



    ##################################################################
    # Execute Single Model
    ##################################################################

    def execute_model(

        self,

        model

    ):


        start = time.perf_counter()


        output = model.run()


        end = time.perf_counter()



        apdt = (

            end-start

        ) * 1000



        return apdt, output



    ##################################################################
    # Run Experiments
    ##################################################################

    def run_experiment(self):


        for size in self.graph_sizes:


            print(

                f"Running APDT for {size} node graphs"

            )


            graphs = self.loader.load_graphs(

                size

            )



            method_times = {



                method:

                    []

                for method in self.methods

            }



            for graph in graphs:


                models = self.loader.get_all_models(

                    graph

                )



                for method, model in models.items():


                    runtime, _ = self.execute_model(

                        model

                    )


                    method_times[method].append(

                        runtime

                    )



            for method in self.methods:


                self.results.append(

                    {

                    "Method":

                        method,


                    "Graph_Size":

                        size,


                    "APDT":

                        sum(

                            method_times[method]

                        )

                        /

                        len(

                            method_times[method]

                        )

                    }

                )



        return pd.DataFrame(

            self.results

        )



    ##################################################################
    # QSEG Calculation
    ##################################################################

    def compute_qseg(

        self,

        dataframe

    ):


        values = []


        for size in self.graph_sizes:


            markov = dataframe[

                (

                    dataframe.Method=="Markov"

                )

                &

                (

                    dataframe.Graph_Size==size

                )

            ]["APDT"].iloc[0]



            aqagc = dataframe[

                (

                    dataframe.Method=="AQAGC"

                )

                &

                (

                    dataframe.Graph_Size==size

                )

            ]["APDT"].iloc[0]



            values.append(

                {

                "Graph_Size":

                    size,


                "QSEG":

                    markov / aqagc

                }

            )


        return pd.DataFrame(

            values

        )



    ##################################################################
    # Generate Table
    ##################################################################

    def generate_table(

        self,

        dataframe,

        qseg

    ):



        table = dataframe.pivot(

            index="Method",

            columns="Graph_Size",

            values="APDT"

        )



        qseg_row = qseg.set_index(

            "Graph_Size"

        ).T



        final_table = pd.concat(

            [

                table,

                qseg_row

            ]

        )



        final_table.to_latex(

            os.path.join(

                self.table_dir,

                "apdt_results.tex"

            ),

            float_format="%.3f"

        )



        return final_table



    ##################################################################
    # APDT Figure
    ##################################################################

    def generate_apdt_plot(

        self,

        dataframe

    ):



        plt.figure(

            figsize=(8,5)

        )



        for method in self.methods:


            subset = dataframe[

                dataframe.Method == method

            ]



            plt.plot(

                subset.Graph_Size,

                subset.APDT,

                marker="o",

                label=method

            )



        plt.xlabel(

            "Graph Size (Nodes)"

        )


        plt.ylabel(

            "APDT (ms)"

        )


        plt.legend()


        plt.grid(True)



        plt.tight_layout()



        plt.savefig(

            os.path.join(

                self.figure_dir,

                "apdt_comparison_publication.png"

            ),

            dpi=300

        )


        plt.close()



    ##################################################################
    # QSEG Figure
    ##################################################################

    def generate_qseg_plot(

        self,

        qseg

    ):


        plt.figure(

            figsize=(7,4)

        )


        plt.fill_between(

            qseg.Graph_Size,

            qseg.QSEG

        )


        plt.plot(

            qseg.Graph_Size,

            qseg.QSEG,

            marker="o"

        )



        plt.xlabel(

            "Graph Size"

        )


        plt.ylabel(

            "QSEG"

        )


        plt.grid(True)



        plt.tight_layout()



        plt.savefig(

            os.path.join(

                self.figure_dir,

                "qseg_growth_publication.png"

            ),

            dpi=300

        )


        plt.close()



    ##################################################################
    # Save Values
    ##################################################################

    def save_values(

        self,

        table

    ):


        values = {


            "AQAGC_APDT_5000":

                float(

                    table.loc[

                        "AQAGC",

                        5000

                    ]

                ),


            "Markov_APDT_5000":

                float(

                    table.loc[

                        "Markov",

                        5000

                    ]

                )

        }



        with open(

            os.path.join(

                self.value_dir,

                "apdt_values.json"

            ),

            "w"

        ) as file:


            json.dump(

                values,

                file,

                indent=4

            )



    ##################################################################
    # Run
    ##################################################################

    def run(self):


        results = self.run_experiment()


        qseg = self.compute_qseg(

            results

        )


        table = self.generate_table(

            results,

            qseg

        )


        self.generate_apdt_plot(

            results

        )


        self.generate_qseg_plot(

            qseg

        )


        self.save_values(

            table

        )


        return {


            "APDT":

                results,


            "QSEG":

                qseg

        }