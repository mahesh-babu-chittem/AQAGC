"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Effect Size Analysis

==============================================================
"""

from __future__ import annotations

import numpy as np

import pandas as pd



class EffectSizeAnalyzer:



    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.results = []



    ####################################################################
    # Cohen's d
    ####################################################################

    def cohens_d(

        self,

        baseline_values,

        aqagc_values,

    ):

        """
        Cohen's d:

            d = (Mean_AQAGC - Mean_Baseline)
                /
                Pooled_STD


        """

        baseline_values = np.asarray(

            baseline_values

        )


        aqagc_values = np.asarray(

            aqagc_values

        )


        baseline_mean = np.mean(

            baseline_values

        )


        aqagc_mean = np.mean(

            aqagc_values

        )


        baseline_std = np.std(

            baseline_values,

            ddof=1

        )


        aqagc_std = np.std(

            aqagc_values,

            ddof=1

        )


        pooled_std = np.sqrt(

            (

                (

                    baseline_std ** 2

                    +

                    aqagc_std ** 2

                )

                /

                2

            )

        )


        if pooled_std == 0:

            return 0.0


        return (

            aqagc_mean -

            baseline_mean

        ) / pooled_std



    ####################################################################
    # Effect Magnitude Interpretation
    ####################################################################

    def interpretation(

        self,

        value,

    ):

        """

        Cohen's d interpretation:

            < 0.2  : negligible

            0.2-0.5: small

            0.5-0.8: medium

            >0.8   : large


        """

        magnitude = abs(

            value

        )


        if magnitude < 0.2:

            return "Negligible"


        elif magnitude < 0.5:

            return "Small"


        elif magnitude < 0.8:

            return "Medium"


        else:

            return "Large"



    ####################################################################
    # Compare Methods
    ####################################################################

    def compare(

        self,

        baseline_name,

        baseline_values,

        aqagc_values,

    ):

        effect = self.cohens_d(

            baseline_values,

            aqagc_values,

        )


        result = {

            "Baseline":

                baseline_name,


            "Proposed":

                "AQAGC",


            "Cohens_d":

                effect,


            "Effect_Size":

                self.interpretation(

                    effect

                ),

        }


        self.results.append(

            result

        )


        return result



    ####################################################################
    # Batch Comparison
    ####################################################################

    def compare_all(

        self,

        baseline_results,

        aqagc_results,

    ):

        """

        baseline_results:

            {

                "BFS": values,

                "DFS": values

            }


        aqagc_results:

            values


        """

        for method, values in baseline_results.items():

            self.compare(

                method,

                values,

                aqagc_results,

            )


        return self.dataframe()



    ####################################################################
    # DataFrame
    ####################################################################

    def dataframe(self):

        return pd.DataFrame(

            self.results

        )



    ####################################################################
    # Save
    ####################################################################

    def save(

        self,

        filepath,

    ):

        self.dataframe().to_csv(

            filepath,

            index=False

        )