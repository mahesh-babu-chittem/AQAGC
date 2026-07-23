"""
==============================================================
AQAGC

Stage 07

Results Generation

==============================================================
"""


from __future__ import annotations


import os
import json


import pandas as pd
import networkx as nx



# ==============================================================
# Stage 06 Imports
# ==============================================================


from stage06_benchmarking.bfs_baseline import BFSBaseline
from stage06_benchmarking.dfs_baseline import DFSBaseline
from stage06_benchmarking.astar_baseline import AStarBaseline
from stage06_benchmarking.markov_baseline import MarkovBaseline

from stage06_benchmarking.dtqw_baseline import DTQWBaseline
from stage06_benchmarking.ctqw_baseline import CTQWBaseline

from stage06_benchmarking.qagc_baseline import QAGCBaseline

from stage06_benchmarking.aqagc_runner import AQAGCRunner



class ResultsLoader:
    """
    Central loader for Stage 07.

    Stage 07 does not read previous
    result files.

    It reloads:

        Data  -> from data folder

        Models -> from Stage 06


    """



    ##################################################################
    # Initialization
    ##################################################################

    def __init__(

        self,

        data_root="../data/benchmark/CSE_CIC_IDS2018",

    ):


        self.data_root = data_root


        self.graph_root = os.path.join(

            data_root,

            "benchmark_graphs"

        )



        self.nodes_path = os.path.join(

            data_root,

            "nodes.csv"

        )


        self.edges_path = os.path.join(

            data_root,

            "edges.csv"

        )


        self.ground_truth_path = os.path.join(

            data_root,

            "ground_truth.csv"

        )


        self.metadata_path = os.path.join(

            data_root,

            "metadata.json"

        )



    ##################################################################
    # Load Nodes
    ##################################################################

    def load_nodes(self):


        return pd.read_csv(

            self.nodes_path

        )



    ##################################################################
    # Load Edges
    ##################################################################

    def load_edges(self):


        return pd.read_csv(

            self.edges_path

        )



    ##################################################################
    # Load Ground Truth
    ##################################################################

    def load_ground_truth(self):


        return pd.read_csv(

            self.ground_truth_path

        )



    ##################################################################
    # Load Metadata
    ##################################################################

    def load_metadata(self):


        with open(

            self.metadata_path,

            "r"

        ) as file:


            return json.load(file)



    ##################################################################
    # Load Single GraphML
    ##################################################################

    def load_graph(

        self,

        graph_size,

        graph_id=1,

    ):


        folder = os.path.join(

            self.graph_root,

            f"{graph_size}_nodes"

        )


        graph_file = os.path.join(

            folder,

            f"graph_{graph_id:02d}.graphml"

        )


        graph = nx.read_graphml(

            graph_file

        )


        return graph



    ##################################################################
    # Load All Graphs
    ##################################################################

    def load_graphs(

        self,

        graph_size,

    ):


        folder = os.path.join(

            self.graph_root,

            f"{graph_size}_nodes"

        )


        graphs = []


        for file in sorted(

            os.listdir(folder)

        ):


            if file.endswith(

                ".graphml"

            ):


                graph = nx.read_graphml(

                    os.path.join(

                        folder,

                        file

                    )

                )


                graphs.append(

                    graph

                )


        return graphs



    ##################################################################
    # Available Graph Sizes
    ##################################################################

    def graph_sizes(self):


        return [

            50,

            200,

            500,

            1000,

            2000,

            5000

        ]



    ##################################################################
    # Load Stage 06 Models
    ##################################################################

    def get_all_models(

        self,

        graph,

    ):


        """
        Returns all benchmark models
        implemented in Stage 06.

        """


        models = {}



        models["BFS"] = BFSBaseline(

            graph

        )


        models["DFS"] = DFSBaseline(

            graph

        )


        models["AStar"] = AStarBaseline(

            graph

        )


        models["Markov"] = MarkovBaseline(

            graph

        )


        models["DTQW"] = DTQWBaseline(

            graph

        )


        models["CTQW"] = CTQWBaseline(

            graph

        )


        models["QAGC"] = QAGCBaseline(

            graph

        )


        #
        # AQAGC is already wrapped
        # by Stage 06 runner
        #

        models["AQAGC"] = AQAGCRunner(

            graph

        )


        return models



    ##################################################################
    # Load Ground Truth Nodes
    ##################################################################

    def critical_nodes(self):


        ground_truth = self.load_ground_truth()


        if "Node_ID" in ground_truth.columns:


            return list(

                ground_truth["Node_ID"]

            )


        return list(

            ground_truth.iloc[:,0]

        )