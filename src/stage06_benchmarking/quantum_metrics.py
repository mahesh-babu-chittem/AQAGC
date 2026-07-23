"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Quantum Performance Metrics

==============================================================
"""

from __future__ import annotations

import numpy as np

import pandas as pd



class QuantumMetrics:




    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.results = {}



    ####################################################################
    # Quantum Simulation Efficiency Gain
    ####################################################################

    def qseg(

        self,

        classical_time,

        quantum_time,

    ):


        if quantum_time == 0:

            return 0.0


        return (

            classical_time /

            quantum_time

        )



    ####################################################################
    # Quantum Entropy
    ####################################################################

    def quantum_entropy(

        self,

        probabilities,

    ):

        """
        Shannon entropy of quantum measurement
        probability distribution.

        H(p) = -Σ p log2(p)

        """

        probabilities = np.asarray(

            probabilities

        )


        probabilities = probabilities[

            probabilities > 0

        ]


        if len(probabilities) == 0:

            return 0.0


        entropy = -np.sum(

            probabilities *

            np.log2(

                probabilities

            )

        )


        return float(

            entropy

        )



    ####################################################################
    # Normalized Quantum Entropy
    ####################################################################

    def normalized_entropy(

        self,

        probabilities,

    ):

        """

        Normalized entropy:

            H(p) / log2(N)


        """

        probabilities = np.asarray(

            probabilities

        )


        n = len(

            probabilities

        )


        if n <= 1:

            return 0.0


        entropy = self.quantum_entropy(

            probabilities

        )


        return float(

            entropy /

            np.log2(

                n

            )

        )



    ####################################################################
    # Adaptive Scheduler Coefficient
    ####################################################################

    def scheduler_statistics(

        self,

        alpha_values,

    ):

        """
        Analyse adaptive scheduler coefficient αt.

        αt controls DTQW-CTQW contribution.
        """

        alpha_values = np.asarray(

            alpha_values

        )


        if len(alpha_values) == 0:

            return {


                "Mean_Alpha":

                    0.0,


                "Std_Alpha":

                    0.0,


                "Min_Alpha":

                    0.0,


                "Max_Alpha":

                    0.0,

            }



        return {


            "Mean_Alpha":

                float(

                    np.mean(

                        alpha_values

                    )

                ),


            "Std_Alpha":

                float(

                    np.std(

                        alpha_values

                    )

                ),


            "Min_Alpha":

                float(

                    np.min(

                        alpha_values

                    )

                ),


            "Max_Alpha":

                float(

                    np.max(

                        alpha_values

                    )

                ),

        }



    ####################################################################
    # Probability Concentration
    ####################################################################

    def probability_concentration(

        self,

        probabilities,

    ):

        """
        Measures concentration of quantum
        probability distribution.

        """

        probabilities = np.asarray(

            probabilities

        )


        total = probabilities.sum()


        if total == 0:

            return 0.0


        return float(

            np.max(

                probabilities

            )

            /

            total

        )



    ####################################################################
    # Complete Quantum Report
    ####################################################################

    def calculate(

        self,

        classical_time=None,

        quantum_time=None,

        probabilities=None,

        alpha_values=None,

    ):

        results = {}



        if (

            classical_time is not None

            and

            quantum_time is not None

        ):

            results["QSEG"] = self.qseg(

                classical_time,

                quantum_time

            )



        if probabilities is not None:


            results["Quantum_Entropy"] = (

                self.quantum_entropy(

                    probabilities

                )

            )


            results["Normalized_Entropy"] = (

                self.normalized_entropy(

                    probabilities

                )

            )


            results["Probability_Concentration"] = (

                self.probability_concentration(

                    probabilities

                )

            )



        if alpha_values is not None:


            results.update(

                self.scheduler_statistics(

                    alpha_values

                )

            )



        return results



    ####################################################################
    # DataFrame
    ####################################################################

    def dataframe(

        self,

        **kwargs

    ):

        return pd.DataFrame(

            [

                self.calculate(

                    **kwargs

                )

            ]

        )