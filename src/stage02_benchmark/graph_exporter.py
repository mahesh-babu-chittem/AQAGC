"""
===========================================================================
AQAGC

Stage 2

Graph Exporter

Exports

• Complete attack graph
• Benchmark graph collection
• Node table
• Edge table
• Ground truth
• Metadata

===========================================================================

"""

from __future__ import annotations

from fileinput import filename
import json
from pathlib import Path

import networkx as nx
from numpy import rint
import pandas as pd


class GraphExporter:

    """
    Dataset-independent exporter.

    Every dataset produces exactly the same output structure,
    regardless of node types.

    Outputs

    benchmark/
        dataset_name/
            graph.graphml
            nodes.csv
            edges.csv
            ground_truth.csv
            metadata.json

            benchmark_graphs/
                50_nodes/
                200_nodes/
                ...
    """

    ##################################################################

    def __init__(

        self,

        output_directory,

    ):

        self.output_directory = Path(

            output_directory

        )

        self.output_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        ###############################################################

        self.graph_directory = (

            self.output_directory

            /

            "benchmark_graphs"

        )

        self.graph_directory.mkdir(

            exist_ok=True,

            parents=True,

        )

    ##################################################################
    # Helper
    ##################################################################

    def _save_csv(

        self,

        dataframe,

        filename,

    ):

        file = (

            self.output_directory

            /

            filename

        )

        dataframe.to_csv(

            file,

            index=False,

        )

        print(

            f"Saved {filename}"

        )

    ##################################################################
    # Helper
    ##################################################################

    def _save_graph(

    self,

    graph,

    filename,

    ):

        file = self.output_directory / filename

    ##############################################################

        print("\nChecking node attributes...\n")

        for node, attrs in graph.nodes(data=True):

            for key, value in attrs.items():

                if not isinstance(value, (str, int, float, bool, type(None))):

                    print(
                        f"NODE {node}: {key} -> {type(value)}"
                    )

    ##############################################################

        print("\nChecking edge attributes...\n")

        for u, v, attrs in graph.edges(data=True):

            for key, value in attrs.items():

                if not isinstance(value, (str, int, float, bool, type(None))):

                    print(
                        f"EDGE {u}->{v}: {key} -> {type(value)}"
                    )

    ##############################################################

        nx.write_graphml(

            graph,

            file,

        )

        print(f"Saved {filename}")
    
    def export_nodes(

        self,

        nodes: pd.DataFrame,

    ):

        """
        Export node table.
        """

        self._save_csv(

            nodes,

            "nodes.csv",

        )

    ##################################################################
    # Export Edges
    ##################################################################

    def export_edges(

        self,

        edges: pd.DataFrame,

    ):

        """
        Export edge table.
        """

        self._save_csv(

            edges,

            "edges.csv",

        )

    ##################################################################
    # Export Ground Truth
    ##################################################################

    def export_ground_truth(

        self,

        ground_truth: pd.DataFrame,

    ):

        """
        Export deterministic ground truth.
        """

        self._save_csv(

            ground_truth,

            "ground_truth.csv",

        )

    ##################################################################
    # Export Complete Attack Graph
    ##################################################################

    def export_complete_graph(

        self,

        graph: nx.DiGraph,

    ):

        """
        Export complete attack graph.

        GraphML preserves all node and edge attributes.
        """

        self._save_graph(

            graph,

            "AQAGC_Attack_Graph.graphml",

        )

    ##################################################################
    # Export Benchmark Graph Collection
    ##################################################################

    def export_benchmark_graphs(

        self,

        benchmark_graphs,

    ):

        """
        Export sampled benchmark graphs.

        benchmark_graphs

        {

            50 : [graph1, graph2, ...],

            200 : [...],

            ...

        }

        """

        print("\nExporting Benchmark Graphs...")

        ###############################################################

        for graph_size, graphs in benchmark_graphs.items():

            size_folder = (

                self.graph_directory

                /

                f"{graph_size}_nodes"

            )

            size_folder.mkdir(

                parents=True,

                exist_ok=True,

            )

            ###########################################################

            for index, graph in enumerate(

                graphs,

                start=1,

            ):

                filename = (

                    size_folder

                    /

                    f"graph_{index:02d}.graphml"

                )

                nx.write_graphml(

                    graph,

                    filename,

                )

        print(

            "Benchmark graphs exported successfully."

        )

            ##################################################################
    # Export Metadata
    ##################################################################

    def export_metadata(

        self,

        graph: nx.DiGraph,

        nodes: pd.DataFrame,

        edges: pd.DataFrame,

        ground_truth: pd.DataFrame,

        benchmark_graphs,

    ):

        """
        Export benchmark metadata.

        This file provides reproducibility information for the
        generated benchmark.
        """

        metadata = {}

        ###############################################################
        # Graph Statistics
        ###############################################################

        metadata["graph"] = {

            "nodes":

                int(

                    graph.number_of_nodes()

                ),

            "edges":

                int(

                    graph.number_of_edges()

                ),

            "density":

                float(

                    nx.density(graph)

                ),

            "self_loops":

                int(

                    nx.number_of_selfloops(graph)

                ),

            "is_directed":

                bool(

                    graph.is_directed()

                ),

        }

        ###############################################################
        # Node Statistics
        ###############################################################

        metadata["nodes"] = {

            "total":

                int(

                    len(nodes)

                ),

            "node_types":

                {

                    str(k): int(v)

                    for k, v in

                    nodes["node_type"]

                    .value_counts()

                    .to_dict()

                    .items()

                },

        }

        ###############################################################
        # Dataset Statistics
        ###############################################################

        if "dataset" in nodes.columns:

            metadata["datasets"] = {

                str(k): int(v)

                for k, v in

                nodes["dataset"]

                .value_counts()

                .to_dict()

                .items()

            }

        ###############################################################
        # Edge Statistics
        ###############################################################

        metadata["edges"] = {

            "total":

                int(

                    len(edges)

                ),

        }

        if "edge_type" in edges.columns:

            metadata["edges"]["edge_types"] = {

                str(k): int(v)

                for k, v in

                edges["edge_type"]

                .value_counts()

                .to_dict()

                .items()

            }

        ###############################################################
        # Ground Truth
        ###############################################################

        metadata["ground_truth"] = {

            "critical_paths":

                int(

                    len(ground_truth)

                )

        }

        ###############################################################
        # Benchmark Collection
        ###############################################################

        benchmark_summary = {}

        for graph_size, graphs in benchmark_graphs.items():

            benchmark_summary[str(graph_size)] = {

                "instances":

                    len(graphs)

            }

        metadata["benchmark_graphs"] = benchmark_summary

        ###############################################################
        # Save JSON
        ###############################################################

        metadata_file = (

            self.output_directory

            /

            "metadata.json"

        )

        with open(

            metadata_file,

            "w",

        ) as fp:

            json.dump(

                metadata,

                fp,

                indent=4,

            )

        print(

            "Saved metadata.json"

        )

    ##################################################################
    # Summary
    ##################################################################

    def summary(

        self,

        graph,

        nodes,

        edges,

        ground_truth,

    ):

        """
        Print export summary.
        """

        print("\n")

        print("=" * 70)

        print("EXPORT SUMMARY")

        print("=" * 70)

        print(

            f"Nodes               : {len(nodes):,}"

        )

        print(

            f"Edges               : {len(edges):,}"

        )

        print(

            f"Ground Truth Paths  : {len(ground_truth):,}"

        )

        print(

            f"Graph Nodes         : {graph.number_of_nodes():,}"

        )

        print(

            f"Graph Edges         : {graph.number_of_edges():,}"

        )

        print("=" * 70)

            ##################################################################
    # Export Everything
    ##################################################################

    def export_all(

        self,

        graph: nx.DiGraph,

        nodes: pd.DataFrame,

        edges: pd.DataFrame,

        ground_truth: pd.DataFrame,

        benchmark_graphs,

    ):

        """
        Export the complete AQAGC benchmark.
        """

        print("\n")

        print("=" * 70)

        print("EXPORTING AQAGC BENCHMARK")

        print("=" * 70)

        ##############################################################

        self.export_complete_graph(

            graph,

        )

        ##############################################################

        self.export_nodes(

            nodes,

        )

        ##############################################################

        self.export_edges(

            edges,

        )

        ##############################################################

        self.export_ground_truth(

            ground_truth,

        )

        ##############################################################

        self.export_benchmark_graphs(

            benchmark_graphs,

        )

        ##############################################################

        self.export_metadata(

            graph,

            nodes,

            edges,

            ground_truth,

            benchmark_graphs,

        )

        ##############################################################

        self.summary(

            graph,

            nodes,

            edges,

            ground_truth,

        )

        print("\nBenchmark exported successfully.\n")

    ##################################################################
    # Validation
    ##################################################################

    def validate(

        self,

        graph,

        nodes,

        edges,

    ):

        """
        Basic validation before export.
        """

        if graph.number_of_nodes() == 0:

            raise ValueError(

                "Graph contains no nodes."

            )

        if graph.number_of_edges() == 0:

            raise ValueError(

                "Graph contains no edges."

            )

        if len(nodes) == 0:

            raise ValueError(

                "Node table is empty."

            )

        if len(edges) == 0:

            raise ValueError(

                "Edge table is empty."

            )

        return True

    ##################################################################
    # Output Directory
    ##################################################################

    def output_path(self):

        """
        Returns benchmark output directory.
        """

        return self.output_directory

    ##################################################################
    # Reset
    ##################################################################

    def reset(self):

        """
        Placeholder for future exporter state.
        """

        pass

    ##################################################################
    # Representation
    ##################################################################

    def __repr__(self):

        return (

            "GraphExporter("

            f"output_directory='{self.output_directory}'"

            ")"

        )