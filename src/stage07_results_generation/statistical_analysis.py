"""
==============================================================
AQAGC

Stage 07

Results Generation

Statistical Significance Analysis

==============================================================
"""


from __future__ import annotations


import os
import json


import numpy as np
import pandas as pd


from scipy.stats import (
    ttest_rel,
    wilcoxon,
    t
)


from statsmodels.stats.multitest import (
    multipletests
)



class StatisticalAnalysis:



    def __init__(

        self,

        loader,

        output_dir="outputs/statistical"

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

            "Markov",

            "CTQW",

            "QAGC",

            "AQAGC"

        ]



        self.runs = 20



    ##############################################################
    # Precision Calculation
    ##############################################################

    def precision_at_10(

        self,

        ranking,

        truth

    ):


        top10 = ranking[:10]


        return len(

            set(top10)

            &

            set(truth)

        ) / 10



    ##############################################################
    # MAP Calculation
    ##############################################################

    def calculate_map(

        self,

        ranking,

        truth

    ):


        hits = 0

        score = 0



        for i,node in enumerate(ranking):


            if node in truth:


                hits += 1


                score += hits/(i+1)



        if len(truth)==0:

            return 0


        return score/len(truth)



    ##############################################################
    # Execute Multiple Runs
    ##############################################################

    def collect_runs(self):


        results=[]



        graph = (

            self.loader.load_graphs(

                1000

            )[0]

        )


        ground_truth = (

            self.loader.load_ground_truth()

        )


        truth = list(

            ground_truth.iloc[:,0]

        )



        for run in range(

            self.runs

        ):


            models = self.loader.get_all_models(

                graph

            )



            for method in self.methods:


                ranking = models[method].run()



                if isinstance(

                    ranking,

                    pd.DataFrame

                ):


                    ranking = (

                        ranking.iloc[:,0]

                        .tolist()

                    )



                results.append(

                    {


                    "Run":

                        run,


                    "Method":

                        method,


                    "Precision@10":

                        self.precision_at_10(

                            ranking,

                            truth

                        ),


                    "MAP":

                        self.calculate_map(

                            ranking,

                            truth

                        )

                    }

                )



        return pd.DataFrame(

            results

        )



    ##############################################################
    # Cohen d
    ##############################################################

    def cohens_d(

        self,

        x,

        y

    ):


        difference = np.array(x)-np.array(y)


        return (

            np.mean(difference)

            /

            np.std(

                difference,

                ddof=1

            )

        )



    ##############################################################
    # Confidence Interval
    ##############################################################

    def confidence_interval(

        self,

        values

    ):


        values = np.asarray(values)


        mean = np.mean(values)


        error = (

            t.ppf(

                0.975,

                len(values)-1

            )

            *

            np.std(

                values,

                ddof=1

            )

            /

            np.sqrt(

                len(values)

            )

        )


        return (

            mean-error,

            mean+error

        )



    ##############################################################
    # Pairwise Comparison
    ##############################################################

    def statistical_tests(

        self,

        dataframe

    ):


        results=[]

        p_values=[]



        aqagc = dataframe[

            dataframe.Method=="AQAGC"

        ]["Precision@10"].values



        for baseline in [

            "Markov",

            "CTQW",

            "QAGC"

        ]:



            other = dataframe[

                dataframe.Method==baseline

            ]["Precision@10"].values



            t_stat,t_p = ttest_rel(

                aqagc,

                other

            )



            try:


                w_stat,w_p = wilcoxon(

                    aqagc,

                    other

                )


            except:


                w_stat=0

                w_p=1



            d = self.cohens_d(

                aqagc,

                other

            )


            results.append(

                {


                "Comparison":

                    f"AQAGC vs {baseline}",


                "t-statistic":

                    t_stat,


                "t-test p-value":

                    t_p,


                "Wilcoxon statistic":

                    w_stat,


                "Wilcoxon p-value":

                    w_p,


                "Cohen d":

                    d

                }

            )


            p_values.append(

                t_p

            )



        corrected = multipletests(

            p_values,

            method="holm"

        )[1]



        for i,value in enumerate(corrected):


            results[i][

                "Holm-adjusted p-value"

            ] = value



        return pd.DataFrame(

            results

        )



    ##############################################################
    # Stability Analysis
    ##############################################################

    def stability_analysis(

        self,

        dataframe

    ):


        results=[]



        for method in self.methods:


            values = dataframe[

                dataframe.Method==method

            ]["Precision@10"]



            low,high = self.confidence_interval(

                values

            )



            results.append(

                {


                "Method":

                    method,


                "Mean":

                    values.mean(),


                "Std Dev":

                    values.std(),


                "95% CI":

                    f"[{low:.3f},{high:.3f}]"

                }

            )



        return pd.DataFrame(

            results

        )



    ##############################################################
    # Save
    ##############################################################

    def save_outputs(

        self,

        tests,

        stability

    ):


        combined = pd.concat(

            [

                tests,

                stability

            ],

            ignore_index=True

        )



        combined.to_latex(

            os.path.join(

                self.table_dir,

                "statistical_results.tex"

            ),

            index=False,

            float_format="%.3f"

        )



        with open(

            os.path.join(

                self.value_dir,

                "statistical_values.json"

            ),

            "w"

        ) as file:


            json.dump(

                combined.to_dict(

                    orient="records"

                ),

                file,

                indent=4

            )



    ##############################################################
    # Run
    ##############################################################

    def run(self):


        results = self.collect_runs()



        tests = self.statistical_tests(

            results

        )


        stability = self.stability_analysis(

            results

        )



        self.save_outputs(

            tests,

            stability

        )


        return {


            "tests":

                tests,


            "stability":

                stability

        }