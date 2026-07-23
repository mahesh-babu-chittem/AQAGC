"""
==============================================================
AQAGC

Stage 07

Results Generation

Hyperparameter Sensitivity Analysis


==============================================================
"""


from __future__ import annotations


import os
import json


import pandas as pd



class HyperparameterAnalysis:


    ##############################################################
    # Initialization
    ##############################################################

    def __init__(

        self,

        loader,

        output_dir="outputs/hyperparameter"

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



        self.parameters = {


            "eta":

                [

                    0.10,

                    0.20,

                    0.30,

                    0.40,

                    0.50

                ],


            "omega1":

                [

                    0.20,

                    0.40,

                    0.60,

                    0.80

                ],


            "omega2":

                [

                    0.20,

                    0.40,

                    0.60,

                    0.80

                ],


            "theta":

                [

                    "default",

                    "-20%",

                    "+20%"

                ],


            "K":

                [

                    5,

                    10,

                    15,

                    20

                ]

        }



    ##############################################################
    # MAP Calculation
    ##############################################################

    def calculate_map(

        self,

        ranking

    ):


        ground_truth = (

            self.loader.load_ground_truth()

        )


        truth = list(

            ground_truth.iloc[:,0]

        )


        score = 0

        hits = 0


        for index,node in enumerate(ranking):


            if node in truth:


                hits += 1


                score += (

                    hits /

                    (

                        index + 1

                    )

                )


        if len(truth)==0:

            return 0


        return score / len(truth)



    ##############################################################
    # Evaluate Configuration
    ##############################################################

    def evaluate_configuration(

        self,

        parameter,

        value

    ):


        """

        Creates AQAGC with modified
        parameter.

        """


        graph = (

            self.loader.load_graphs(

                1000

            )[0]

        )


        config = {


            parameter:

                value

        }



        model = self.loader.load_aqagc_model(

            graph,

            config

        )


        ranking = model.run()



        if isinstance(

            ranking,

            pd.DataFrame

        ):


            ranking = (

                ranking.iloc[:,0]

                .tolist()

            )



        return self.calculate_map(

            ranking

        )



    ##############################################################
    # Run Sensitivity Experiment
    ##############################################################

    def run_experiment(self):


        results=[]



        for parameter,values in self.parameters.items():


            for value in values:


                print(

                    "Testing",

                    parameter,

                    value

                )


                map_score = self.evaluate_configuration(

                    parameter,

                    value

                )



                results.append(

                    {


                    "Parameter":

                        parameter,


                    "Value":

                        str(value),


                    "MAP":

                        map_score

                    }

                )



        return pd.DataFrame(

            results

        )



    ##############################################################
    # Generate Manuscript Table
    ##############################################################

    def generate_table(

        self,

        dataframe

    ):


        selected=[]



        for parameter in self.parameters:


            subset = dataframe[

                dataframe.Parameter == parameter

            ]


            best = subset.loc[

                subset.MAP.idxmax()

            ]



            selected.append(

                {


                "Parameter":

                    parameter,


                "Evaluated Range":

                    str(

                        list(

                            self.parameters[parameter]

                        )

                    ),


                "Selected Value":

                    best.Value,


                "MAP":

                    best.MAP

                }

            )



        table = pd.DataFrame(

            selected

        )



        table.to_latex(

            os.path.join(

                self.table_dir,

                "hyperparameter_sensitivity.tex"

            ),

            index=False,

            float_format="%.3f"

        )



        return table



    ##############################################################
    # Save Values
    ##############################################################

    def save_values(

        self,

        table

    ):


        with open(

            os.path.join(

                self.value_dir,

                "hyperparameter_values.json"

            ),

            "w"

        ) as file:


            json.dump(

                table.to_dict(

                    orient="records"

                ),

                file,

                indent=4

            )



    ##############################################################
    # Run
    ##############################################################

    def run(self):


        results = self.run_experiment()



        table = self.generate_table(

            results

        )


        self.save_values(

            table

        )


        return table