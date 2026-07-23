"""
==============================================================
AQAGC

Stage 07

Results Generation

Explainability and Attribution Analysis


==============================================================
"""


from __future__ import annotations


import os
import json


import numpy as np
import pandas as pd


from scipy.stats import pearsonr, spearmanr



class ExplainabilityAnalysis:



    def __init__(

        self,

        loader,

        output_dir="outputs/explainability"

    ):


        self.loader = loader


        self.output_dir = output_dir



        self.table_dir = os.path.join(

            output_dir,

            "tables"

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

            self.value_dir,

            exist_ok=True

        )



        self.methods = [

            "Markov",

            "DTQW",

            "CTQW",

            "QAGC",

            "AQAGC"

        ]



    ##############################################################
    # Attribution Score Calculation
    ##############################################################

    def calculate_scores(

        self,

        method,

        graph

    ):


        """

        Loads attribution module
        from Stage 05.

        """


        attribution = (

            self.loader.load_attribution_model(

                method,

                graph

            )

        )


        scores = attribution.compute()



        return {


            "Method":

                method,


            "NAS":

                scores["NAS"],


            "EAS":

                scores["EAS"],


            "PAS":

                scores["PAS"]

        }



    ##############################################################
    # Overall Explainability Evaluation
    ##############################################################

    def run_explainability(self):


        graph = (

            self.loader.load_graphs(

                1000

            )[0]

        )


        results=[]



        for method in self.methods:


            results.append(

                self.calculate_scores(

                    method,

                    graph

                )

            )



        dataframe = pd.DataFrame(

            results

        )


        return dataframe



    ##############################################################
    # Case Study
    ##############################################################

    def case_study(self):


        graph = (

            self.loader.load_graphs(

                50

            )[0]

        )


        paths = (

            self.loader.load_representative_paths(

                graph

            )

        )


        results=[]



        for path in paths:


            scores = (

                self.loader.calculate_path_attribution(

                    path

                )

            )


            results.append(

                {


                "Attack Path":

                    path["name"],


                "NAS":

                    scores["NAS"],


                "EAS":

                    scores["EAS"],


                "PAS":

                    scores["PAS"],


                "Analyst Interpretation":

                    scores["interpretation"]

                }

            )



        dataframe = pd.DataFrame(

            results

        )


        dataframe.to_latex(

            os.path.join(

                self.table_dir,

                "explainability_case.tex"

            ),

            index=False

        )


        return dataframe



    ##############################################################
    # CVSS Correlation
    ##############################################################

    def correlation_analysis(self):


        attribution = (

            self.loader.load_all_attribution_scores()

        )


        cvss = (

            self.loader.load_cvss_scores()

        )


        exploitability = (

            self.loader.load_exploitability_scores()

        )


        path_risk = (

            self.loader.load_path_risk()

        )



        results=[]



        pairs=[


            (

                "NAS",

                cvss,

                "CVSS Severity"

            ),


            (

                "EAS",

                exploitability,

                "Exploitability Score"

            ),


            (

                "PAS",

                path_risk,

                "Aggregated Path Risk"

            )

        ]



        for metric,target,label in pairs:


            pearson,_ = pearsonr(

                attribution[metric],

                target

            )


            spearman,_ = spearmanr(

                attribution[metric],

                target

            )



            results.append(

                {


                "Attribution Metric":

                    metric,


                "Reference Indicator":

                    label,


                "Pearson":

                    pearson,


                "Spearman":

                    spearman

                }

            )



        dataframe = pd.DataFrame(

            results

        )



        dataframe.to_latex(

            os.path.join(

                self.table_dir,

                "cvss_correlation.tex"

            ),

            index=False,

            float_format="%.3f"

        )



        return dataframe



    ##############################################################
    # Save Values
    ##############################################################

    def save_values(

        self,

        explainability,

        correlation

    ):


        aqagc = explainability[

            explainability.Method=="AQAGC"

        ].iloc[0]



        values={


            "AQAGC_NAS":

                float(

                    aqagc.NAS

                ),


            "AQAGC_EAS":

                float(

                    aqagc.EAS

                ),


            "AQAGC_PAS":

                float(

                    aqagc.PAS

                ),


            "PAS_Pearson":

                float(

                    correlation.iloc[2].Pearson

                )

        }



        with open(

            os.path.join(

                self.value_dir,

                "explainability_values.json"

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


        explainability = (

            self.run_explainability()

        )


        case = self.case_study()



        correlation = (

            self.correlation_analysis()

        )



        explainability.to_latex(

            os.path.join(

                self.table_dir,

                "explainability_results.tex"

            ),

            index=False,

            float_format="%.3f"

        )



        self.save_values(

            explainability,

            correlation

        )



        return {


            "Explainability":

                explainability,


            "Case":

                case,


            "Correlation":

                correlation

        }