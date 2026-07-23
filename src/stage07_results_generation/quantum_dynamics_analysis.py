"""
==============================================================
AQAGC

Stage 07

Results Generation

Quantum Exploration Dynamics Analysis


"""


from __future__ import annotations


import os
import json


import numpy as np
import pandas as pd


import matplotlib.pyplot as plt



class QuantumDynamicsAnalysis:
    """
    Evaluates AQAGC quantum exploration behavior.
    """



    def __init__(

        self,

        loader,

        output_dir="outputs/quantum_dynamics"

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

            "DTQW",

            "CTQW",

            "QAGC",

            "AQAGC"

        ]



    ##############################################################
    # Amplitude Concentration Score
    ##############################################################

    def amplitude_concentration_score(

        self,

        probabilities

    ):


        """

        ACS measures concentration
        of probability mass.

        """

        probabilities = np.asarray(

            probabilities

        )


        probabilities = (

            probabilities /

            np.sum(probabilities)

        )



        return np.sum(

            probabilities**2

        )



    ##############################################################
    # Entropy
    ##############################################################

    def entropy(

        self,

        probabilities

    ):


        p = np.asarray(

            probabilities

        )


        p = p[p>0]


        return -np.sum(

            p*np.log2(p)

        )



    ##############################################################
    # Risk Concentration Index
    ##############################################################

    def risk_concentration_index(

        self,

        probabilities,

        risk_scores

    ):


        probabilities = np.asarray(

            probabilities

        )


        risk_scores = np.asarray(

            risk_scores

        )


        return np.sum(

            probabilities*risk_scores

        )



    ##############################################################
    # Evaluate Quantum State
    ##############################################################

    def evaluate_state(

        self,

        graph_size,

        method

    ):


        state = self.loader.load_quantum_state(

            graph_size,

            method

        )


        risk = self.loader.load_risk_scores(

            graph_size

        )


        alpha = self.loader.load_scheduler_alpha(

            graph_size

        )



        probability = (

            np.abs(state)**2

        )



        return {


            "Method":

                method,


            "Graph_Size":

                graph_size,


            "ACS":

                self.amplitude_concentration_score(

                    probability

                ),


            "Entropy":

                self.entropy(

                    probability

                ),


            "RCI":

                self.risk_concentration_index(

                    probability,

                    risk

                ),


            "Alpha":

                np.mean(alpha)

        }



    ##############################################################
    # Run Experiment
    ##############################################################

    def run_experiment(self):


        results=[]



        for size in self.graph_sizes:


            for method in self.methods:


                result = self.evaluate_state(

                    size,

                    method

                )


                results.append(

                    result

                )



        return pd.DataFrame(

            results

        )



    ##############################################################
    # Generate ACS Table
    ##############################################################

    def generate_acs_table(

        self,

        dataframe

    ):


        table = dataframe.pivot(

            index="Method",

            columns="Graph_Size",

            values="ACS"

        )


        table.to_latex(

            os.path.join(

                self.table_dir,

                "acs_results.tex"

            ),

            float_format="%.3f"

        )


        return table



    ##############################################################
    # Quantum Dynamics Table
    ##############################################################

    def generate_dynamics_table(

        self,

        dataframe

    ):


        table = dataframe.groupby(

            "Graph_Size"

        )[

            [

                "Alpha",

                "Entropy"

            ]

        ].mean()



        table.to_latex(

            os.path.join(

                self.table_dir,

                "quantum_dynamics.tex"

            ),

            float_format="%.3f"

        )


        return table



    ##############################################################
    # RCI Table
    ##############################################################

    def generate_rci_table(

        self,

        dataframe

    ):


        table = dataframe.pivot(

            index="Method",

            columns="Graph_Size",

            values="RCI"

        )



        table.to_latex(

            os.path.join(

                self.table_dir,

                "rci_results.tex"

            ),

            float_format="%.3f"

        )


        return table



    ##############################################################
    # Scheduler Figure
    ##############################################################

    def scheduler_plot(

        self,

        dataframe

    ):


        values = dataframe.groupby(

            "Graph_Size"

        )[

            "Alpha"

        ].mean()



        plt.figure(

            figsize=(7,4)

        )


        plt.fill_between(

            values.index,

            values.values

        )


        plt.plot(

            values.index,

            values.values,

            marker="o"

        )


        plt.xlabel(

            "Graph Size"

        )


        plt.ylabel(

            "Average αt"

        )


        plt.grid(True)


        plt.tight_layout()



        plt.savefig(

            os.path.join(

                self.figure_dir,

                "scheduler_evolution.png"

            ),

            dpi=300

        )


        plt.close()



    ##############################################################
    # Entropy Figure
    ##############################################################

    def entropy_plot(

        self,

        dataframe

    ):


        values = dataframe.groupby(

            "Graph_Size"

        )[

            "Entropy"

        ].mean()



        plt.figure(

            figsize=(7,4)

        )


        plt.fill_between(

            values.index,

            values.values

        )


        plt.plot(

            values.index,

            values.values,

            marker="o"

        )


        plt.xlabel(

            "Graph Size"

        )


        plt.ylabel(

            "Entropy"

        )


        plt.grid(True)


        plt.tight_layout()



        plt.savefig(

            os.path.join(

                self.figure_dir,

                "entropy_evolution.png"

            ),

            dpi=300

        )


        plt.close()



    ##############################################################
    # Run
    ##############################################################

    def run(self):


        results = self.run_experiment()



        self.generate_acs_table(

            results

        )


        self.generate_dynamics_table(

            results

        )


        self.generate_rci_table(

            results

        )


        self.scheduler_plot(

            results

        )


        self.entropy_plot(

            results

        )



        results.to_csv(

            os.path.join(

                self.output_dir,

                "quantum_dynamics_results.csv"

            ),

            index=False

        )



        return results