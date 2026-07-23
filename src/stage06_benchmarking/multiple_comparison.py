"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Multiple Comparison Correction

==============================================================
"""

from __future__ import annotations

import numpy as np

import pandas as pd



class MultipleComparisonCorrection:


    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.results = []



    ####################################################################
    # Holm-Bonferroni Correction
    ####################################################################

    def holm_bonferroni(

        self,

        p_values,

        alpha=0.05,

    ):

        """
        Holm-Bonferroni step-down correction.

        Parameters:

            p_values:
                list of p-values


            alpha:
                significance level


        Returns:

            corrected decisions

        """

        p_values = np.asarray(

            p_values,

            dtype=float

        )


        number_tests = len(

            p_values

        )


        sorted_indices = np.argsort(

            p_values

        )


        adjusted_results = np.zeros(

            number_tests

        )


        rejected = []


        for rank, index in enumerate(

            sorted_indices

        ):

            adjusted_alpha = (

                alpha /

                (

                    number_tests -

                    rank

                )

            )


            is_significant = (

                p_values[index]

                <=

                adjusted_alpha

            )


            rejected.append(

                is_significant

            )


            adjusted_results[index] = adjusted_alpha



        return {

            "Adjusted_Thresholds":

                adjusted_results,


            "Rejected":

                rejected,

        }



    ####################################################################
    # Add Comparison Result
    ####################################################################

    def add_result(

        self,

        comparison,

        p_value,

    ):

        self.results.append(

            {

                "Comparison":

                    comparison,


                "Raw_P_Value":

                    p_value,

            }

        )



    ####################################################################
    # Apply Correction
    ####################################################################

    def apply(

        self,

        alpha=0.05,

    ):

        dataframe = pd.DataFrame(

            self.results

        )


        if len(dataframe) == 0:

            return dataframe



        correction = self.holm_bonferroni(

            dataframe["Raw_P_Value"].values,

            alpha,

        )


        dataframe["Adjusted_Threshold"] = (

            correction["Adjusted_Thresholds"]

        )


        dataframe["Significant"] = (

            dataframe["Raw_P_Value"]

            <=

            dataframe["Adjusted_Threshold"]

        )


        return dataframe



    ####################################################################
    # Save
    ####################################################################

    def save(

        self,

        filepath,

    ):

        self.apply().to_csv(

            filepath,

            index=False

        )