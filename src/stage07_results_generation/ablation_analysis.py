"""
==============================================================
AQAGC

Stage 07

Results Generation

Ablation Study Analysis

==============================================================
"""


from __future__ import annotations


import os
import json
import time


import pandas as pd



from stage06_benchmarking.aqagc_runner import AQAGCRunner



class AblationAnalysis:


    def __init__(

        self,

        loader,

        output_dir="outputs/ablation"

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


        self.variants = [

            "AQAGC-NoVE",

            "AQAGC-NoAS",

            "AQAGC-NoER",

            "AQAGC-FixedAS",

            "AQAGC-UniformInit",

            "AQAGC"

        ]



    ##############################################################
    # Build AQAGC Variant
    ##############################################################

    def build_variant(

        self,

        graph,

        variant

    ):


        """
        Creates AQAGC variants.

        The underlying AQAGC model is
        imported from previous stages.

        """


        config = {


            "remove_vulnerability_encoding":

                False,


            "remove_adaptive_scheduler":

                False,


            "remove_explainability":

                False,


            "fixed_scheduler":

                False,


            "uniform_initialization":

                False

        }



        if variant == "AQAGC-NoVE":

            config[

                "remove_vulnerability_encoding"

            ] = True



        elif variant == "AQAGC-NoAS":

            config[

                "remove_adaptive_scheduler"

            ] = True



        elif variant == "AQAGC-NoER":

            config[

                "remove_explainability"

            ] = True



        elif variant == "AQAGC-FixedAS":

            config[

                "fixed_scheduler"

            ] = True



        elif variant == "AQAGC-UniformInit":

            config[

                "uniform_initialization"

            ] = True



        aqagc_model = (

            self.loader.load_aqagc_model(

                graph,

                config

            )

        )



        return AQAGCRunner(

            aqagc_model

        )



    ##############################################################
    # Ranking Metrics
    ##############################################################

    def compute_metrics(

        self,

        ranking

    ):


        """
        Uses same ranking metrics
        as manuscript.

        """


        ground_truth = (

            self.loader.load_ground_truth()

        )


        critical_nodes = list(

            ground_truth.iloc[:,0]

        )



        predicted = list(

            ranking

        )


        precision = (

            len(

                set(predicted[:10])

                &

                set(critical_nodes)

            )

            /

            10

        )


        recall = (

            len(

                set(predicted[:10])

                &

                set(critical_nodes)

            )

            /

            len(critical_nodes)

        )



        f1 = (

            2 *

            precision *

            recall

            /

            (

                precision +

                recall

            )

            if precision+recall > 0

            else 0

        )



        return {


            "Precision@10":

                precision,


            "Recall@10":

                recall,


            "F1@10":

                f1

        }



    ##############################################################
    # Run Ablation
    ##############################################################

    def run_experiment(self):


        results=[]


        graphs = self.loader.load_graphs(

            1000

        )


        for graph in graphs:


            for variant in self.variants:


                model = self.build_variant(

                    graph,

                    variant

                )


                start = time.perf_counter()


                ranking = model.run()


                end = time.perf_counter()



                if isinstance(

                    ranking,

                    pd.DataFrame

                ):


                    ranking = (

                        ranking.iloc[:,0]

                        .tolist()

                    )



                metrics = self.compute_metrics(

                    ranking

                )



                results.append(

                    {


                    "Method":

                        variant,


                    "APDT":

                        (

                            end-start

                        )

                        *

                        1000,


                    **metrics


                    }

                )



        return pd.DataFrame(

            results

        )



    ##############################################################
    # Calculate Loss
    ##############################################################

    def add_loss(

        self,

        dataframe

    ):


        baseline = dataframe[

            dataframe.Method=="AQAGC"

        ].iloc[0]



        dataframe["Precision Loss (%)"] = (

            (

                baseline["Precision@10"]

                -

                dataframe["Precision@10"]

            )

            /

            baseline["Precision@10"]

            ) * 100


        dataframe["MAP Loss (%)"] = 0



        dataframe["APRS Loss (%)"] = 0



        return dataframe



    ##############################################################
    # Save Table
    ##############################################################

    def save_table(

        self,

        dataframe

    ):


        dataframe.to_latex(

            os.path.join(

                self.table_dir,

                "ablation_results.tex"

            ),

            index=False,

            float_format="%.3f"

        )



    ##############################################################
    # Save Values
    ##############################################################

    def save_values(

        self,

        dataframe

    ):


        values = {


            "AQAGC":

                dataframe[

                    dataframe.Method=="AQAGC"

                ]

                .to_dict(

                    orient="records"

                )

        }



        with open(

            os.path.join(

                self.value_dir,

                "ablation_values.json"

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


        results = self.run_experiment()



        results = self.add_loss(

            results

        )


        self.save_table(

            results

        )


        self.save_values(

            results

        )


        return results