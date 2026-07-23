"""
==============================================================
AQAGC

Stage 07

Results Generation

Attack Path Ranking Performance Analysis

==============================================================
"""


from __future__ import annotations


import os
import json


import numpy as np
import pandas as pd


from sklearn.metrics import ndcg_score



class RankingAnalysis:
    """
    Attack path ranking evaluation.

    """


    ##############################################################
    # Initialization
    ##############################################################

    def __init__(

        self,

        loader,

        output_dir="outputs/ranking"

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

            "BFS",

            "DFS",

            "AStar",

            "Markov",

            "DTQW",

            "CTQW",

            "QAGC",

            "AQAGC"

        ]



    ##############################################################
    # Precision@K
    ##############################################################

    def precision_at_k(

        self,

        predicted,

        truth,

        k=10

    ):


        predicted = predicted[:k]


        hits = len(

            set(predicted)

            &

            set(truth)

        )


        return hits/k



    ##############################################################
    # Recall@K
    ##############################################################

    def recall_at_k(

        self,

        predicted,

        truth,

        k=10

    ):


        predicted = predicted[:k]


        hits = len(

            set(predicted)

            &

            set(truth)

        )


        return hits / len(truth)



    ##############################################################
    # F1@K
    ##############################################################

    def f1_at_k(

        self,

        precision,

        recall

    ):


        if precision + recall == 0:

            return 0


        return (

            2 *

            precision *

            recall

            /

            (

                precision +

                recall

            )

        )



    ##############################################################
    # MAP
    ##############################################################

    def mean_average_precision(

        self,

        predicted,

        truth

    ):


        score = 0

        hits = 0


        for i,node in enumerate(predicted):


            if node in truth:


                hits += 1


                score += hits/(i+1)



        if len(truth)==0:

            return 0


        return score/len(truth)



    ##############################################################
    # CPC@10
    ##############################################################

    def cpc_at_k(

        self,

        predicted,

        critical_paths,

        k=10

    ):


        top = predicted[:k]


        covered = len(

            set(top)

            &

            set(critical_paths)

        )


        return covered / len(critical_paths)



    ##############################################################
    # APRS
    ##############################################################

    def aprs(

        self,

        predicted,

        risk_scores,

        k=10

    ):


        top = predicted[:k]


        values = [

            risk_scores.get(

                node,

                0

            )

            for node in top

        ]


        return np.mean(values)



    ##############################################################
    # Evaluate One Graph
    ##############################################################

    def evaluate_graph(

        self,

        graph,

    ):


        ground_truth = self.loader.load_ground_truth()



        critical_nodes = list(

            ground_truth.iloc[:,0]

        )


        risk_scores = dict(

            zip(

                ground_truth.iloc[:,0],

                ground_truth.iloc[:,1]

            )

        )



        models = self.loader.get_all_models(

            graph

        )


        results=[]



        for name,model in models.items():


            ranking = model.run()



            if isinstance(

                ranking,

                pd.DataFrame

            ):


                ranking = ranking.iloc[:,0].tolist()


            else:


                ranking=list(ranking)



            precision = self.precision_at_k(

                ranking,

                critical_nodes

            )


            recall = self.recall_at_k(

                ranking,

                critical_nodes

            )


            f1 = self.f1_at_k(

                precision,

                recall

            )


            results.append(

                {


                "Method":

                    name,


                "Precision@10":

                    precision,


                "Recall@10":

                    recall,


                "F1@10":

                    f1,


                "MAP":

                    self.mean_average_precision(

                        ranking,

                        critical_nodes

                    ),


                "NDCG":

                    self.compute_ndcg(

                        ranking,

                        critical_nodes

                    ),


                "CPC@10":

                    self.cpc_at_k(

                        ranking,

                        critical_nodes

                    ),


                "APRS":

                    self.aprs(

                        ranking,

                        risk_scores

                    )

                }

            )


        return results



    ##############################################################
    # NDCG
    ##############################################################

    def compute_ndcg(

        self,

        ranking,

        truth

    ):


        relevance = [

            1 if node in truth else 0

            for node in ranking[:10]

        ]


        ideal = sorted(

            relevance,

            reverse=True

        )


        return ndcg_score(

            [

                ideal

            ],

            [

                relevance

            ]

        )



    ##############################################################
    # Run Experiments
    ##############################################################

    def run_experiment(self):


        all_results=[]



        for size in self.loader.graph_sizes():


            graphs = self.loader.load_graphs(

                size

            )


            for graph in graphs:


                results = self.evaluate_graph(

                    graph

                )


                for row in results:


                    row["Graph_Size"]=size


                    all_results.append(

                        row

                    )



        return pd.DataFrame(

            all_results

        )



    ##############################################################
    # Generate Table
    ##############################################################

    def generate_table(

        self,

        dataframe

    ):


        table = (

            dataframe

            .groupby(

                "Method"

            )

            [

            [

            "Precision@10",

            "Recall@10",

            "F1@10",

            "MAP",

            "NDCG",

            "CPC@10",

            "APRS"

            ]

            ]

            .mean()

        )



        table.to_latex(

            os.path.join(

                self.table_dir,

                "ranking_results.tex"

            ),

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


        values={

            "AQAGC":

                table.loc[

                    "AQAGC"

                ].to_dict()

        }


        with open(

            os.path.join(

                self.value_dir,

                "ranking_values.json"

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



        table = self.generate_table(

            results

        )


        self.save_values(

            table

        )


        return table