"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Statistical Analysis Module

==============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import (
    ttest_rel,
    wilcoxon,
)



class StatisticalAnalyzer:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        confidence_level=0.95,

    ):

        self.confidence_level = confidence_level

        self.results = []



    ####################################################################
    # Mean
    ####################################################################

    def mean(

        self,

        values,

    ):

        return float(

            np.mean(

                values

            )

        )



    ####################################################################
    # Standard Deviation
    ####################################################################

    def standard_deviation(

        self,

        values,

    ):

        return float(

            np.std(

                values,

                ddof=1

            )

        )



    ####################################################################
    # Confidence Interval
    ####################################################################

    def confidence_interval(

        self,

        values,

    ):

        values = np.asarray(

            values

        )


        mean = np.mean(

            values

        )


        std = np.std(

            values,

            ddof=1

        )


        n = len(

            values

        )


        margin = (

            1.96 *

            std /

            np.sqrt(n)

        )


        return (

            float(

                mean - margin

            ),

            float(

                mean + margin

            )

        )



    ####################################################################
    # Paired t-test
    ####################################################################

    def paired_t_test(

        self,

        baseline_values,

        aqagc_values,

    ):

        statistic, p_value = ttest_rel(

            baseline_values,

            aqagc_values,

        )


        return {

            "Test":

                "Paired t-test",

            "Statistic":

                float(statistic),

            "P_Value":

                float(p_value),

        }



    ####################################################################
    # Wilcoxon Signed-Rank Test
    ####################################################################

    def wilcoxon_test(

        self,

        baseline_values,

        aqagc_values,

    ):

        statistic, p_value = wilcoxon(

            baseline_values,

            aqagc_values,

        )


        return {

            "Test":

                "Wilcoxon Signed-Rank",

            "Statistic":

                float(statistic),

            "P_Value":

                float(p_value),

        }



    ####################################################################
    # Compare Two Methods
    ####################################################################

    def compare_methods(

        self,

        baseline_name,

        baseline_values,

        proposed_name,

        proposed_values,

    ):

        baseline_values = np.asarray(

            baseline_values

        )


        proposed_values = np.asarray(

            proposed_values

        )


        ci_low, ci_high = self.confidence_interval(

            proposed_values

        )


        result = {

            "Baseline":

                baseline_name,


            "Proposed":

                proposed_name,


            "Baseline_Mean":

                self.mean(

                    baseline_values

                ),


            "Proposed_Mean":

                self.mean(

                    proposed_values

                ),


            "Baseline_STD":

                self.standard_deviation(

                    baseline_values

                ),


            "Proposed_STD":

                self.standard_deviation(

                    proposed_values

                ),


            "CI_Lower":

                ci_low,


            "CI_Upper":

                ci_high,

        }


        result.update(

            self.paired_t_test(

                baseline_values,

                proposed_values,

            )

        )


        wilcoxon_result = self.wilcoxon_test(

            baseline_values,

            proposed_values,

        )


        result.update(

            {

                "Wilcoxon_Statistic":

                    wilcoxon_result["Statistic"],


                "Wilcoxon_P_Value":

                    wilcoxon_result["P_Value"],

            }

        )


        self.results.append(

            result

        )


        return result



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