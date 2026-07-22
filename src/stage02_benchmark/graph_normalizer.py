"""
===========================================================================
AQAGC
Adaptive Quantum Attack Graph Compiler

Stage 2

Graph Normalization

This module normalizes the generated attack graph before
ground-truth generation and benchmark sampling.

Responsibilities

1. Remove duplicate nodes
2. Remove duplicate edges
3. Remove isolated nodes
4. Re-index node IDs
5. Normalize edge weights
6. Construct NetworkX graph

===========================================================================

"""

from __future__ import annotations

import networkx as nx
import pandas as pd


class GraphNormalizer:

    """
    Generic graph normalization.

    This class is intentionally dataset-independent.
    """

    ##################################################################

    def __init__(self):

        pass

    ##################################################################
    # Public API
    ##################################################################

    def normalize(

        self,

        nodes: pd.DataFrame,

        edges: pd.DataFrame,

    ):

        print("\nNormalizing Attack Graph...")

        ###############################################################
        # Step 1
        ###############################################################

        nodes = self._remove_duplicate_nodes(

            nodes

        )

        ###############################################################

        edges = self._remove_duplicate_edges(

            edges

        )

        ###############################################################

        #dataset = set(nodes["dataset"])

        #if "CSE_CIC_IDS2018" not in dataset:


            #edges = self._remove_self_loops(

                #edges

            #)

        ###############################################################

        nodes = self._remove_isolated_nodes(

            nodes,

            edges,

        )

        ###############################################################

        nodes, edges = self._reindex(

            nodes,

            edges,

        )

        ###############################################################

        edges = self._normalize_weights(

            edges,

        )

        ###############################################################

        graph = self._build_graph(

            nodes,

            edges,

        )

        ###############################################################

        return (

            graph,

            nodes,

            edges,

        )
    
        ##################################################################
    # Duplicate Nodes
    ##################################################################

    def _remove_duplicate_nodes(

        self,

        nodes,

    ):

        return (

            nodes

            .drop_duplicates(

                subset=[

                    "node_type",

                    "identifier",

                    "dataset",

                ]

            )

            .reset_index(

                drop=True

            )

        )

    ##################################################################
    # Duplicate Edges
    ##################################################################

    def _remove_duplicate_edges(

        self,

        edges,

    ):

        return (

            edges

            .drop_duplicates(

                subset=[

                    "source",

                    "destination",

                    "edge_type",

                ]

            )

            .reset_index(

                drop=True

            )

        )

    ##################################################################
    # Remove Self Loops
    ##################################################################

    def _remove_self_loops(

        self,

        edges,

    ):

        return (

            edges[

                edges["source"]

                !=

                edges["destination"]

            ]

            .reset_index(

                drop=True

            )

        )

    ##################################################################
    # Remove Isolated Nodes
    ##################################################################
    def _remove_isolated_nodes(

        self,

        nodes,

        edges,

    ):

        """
        Keep all extracted nodes.

     Isolation removal is disabled because some datasets
    (e.g., CSE-CIC-IDS2018) use node identifiers that are
    re-indexed later in the pipeline. Removing isolated nodes
        at this stage may incorrectly discard every node.
    """

        return nodes.reset_index(drop=True)    

    def _reindex(

        self,

        nodes,

        edges,

    ):

        """
        Re-index node IDs to consecutive integers.

        This ensures deterministic graph construction.
        """

        mapping = {}

        ##############################################################

        for new_id, old_id in enumerate(

            nodes["node_id"],

            start=0,

        ):

            mapping[old_id] = new_id

        ##############################################################

        nodes = nodes.copy()

        edges = edges.copy()

        ##############################################################

        nodes["node_id"] = (

            nodes["node_id"]

            .map(mapping)

        )

        edges["source"] = (

            edges["source"]

            .map(mapping)

        )

        edges["destination"] = (

            edges["destination"]

            .map(mapping)

        )

        return (

            nodes,

            edges,

        )

    ##################################################################
    # Normalize Edge Weights
    ##################################################################

    def _normalize_weights(

        self,

        edges,

    ):

        """
        Min-Max normalization of edge weights.
        """

        if "edge_weight" not in edges.columns:

            edges["normalized_weight"] = 1.0

            return edges

        minimum = float(

            edges["edge_weight"].min()

        )

        maximum = float(

            edges["edge_weight"].max()

        )

        ##############################################################

        if maximum == minimum:

            edges["normalized_weight"] = 1.0

            return edges

        ##############################################################

        edges["normalized_weight"] = (

            (

                edges["edge_weight"]

                - minimum

            )

            /

            (

                maximum

                - minimum

            )

        )

        return edges

    ##################################################################
    # Build NetworkX Graph
    ##################################################################

    def _build_graph(

        self,

        nodes,

        edges,

    ):

        """
        Construct a NetworkX directed graph while preserving
        all node and edge metadata.
        """

        graph = nx.DiGraph()

        ##############################################################
        # Nodes
        ##############################################################

        for _, node in nodes.iterrows():

            attributes = node.to_dict()

            node_id = int(

                attributes.pop(

                    "node_id"

                )

            )

            graph.add_node(

                node_id,

                **attributes,

            )

        ##############################################################
        # Edges
        ##############################################################

        for _, edge in edges.iterrows():

            attributes = edge.to_dict()

            source = int(

                attributes.pop(

                    "source"

                )

            )

            destination = int(

                attributes.pop(

                    "destination"

                )

            )

            graph.add_edge(

                source,

                destination,

                **attributes,

            )

        return graph
    
        ##################################################################
    # Graph Validation
    ##################################################################

    def validate(

        self,

        graph,

    ):

        """
        Validate normalized graph.
        """

        if graph.number_of_nodes() == 0:

            raise ValueError(

                "Graph contains no nodes."

            )

        if graph.number_of_edges() == 0:

            raise ValueError(

                "Graph contains no edges."

            )

        return True

    ##################################################################
    # Graph Statistics
    ##################################################################

    def statistics(

        self,

        graph,

    ):

        """
        Compute graph statistics.
        """

        statistics = {

            "nodes":

                graph.number_of_nodes(),

            "edges":

                graph.number_of_edges(),

            "density":

                nx.density(graph),

            "self_loops":

                nx.number_of_selfloops(graph),

            "isolated_nodes":

                len(

                    list(

                        nx.isolates(graph)

                    )

                ),

            "average_degree":

                sum(

                    dict(

                        graph.degree()

                    ).values()

                )

                /

                graph.number_of_nodes(),

        }

        ##############################################################

        if graph.number_of_nodes() > 1:

            undirected = graph.to_undirected()

            statistics["connected_components"] = (

                nx.number_connected_components(

                    undirected

                )

            )

        else:

            statistics["connected_components"] = 1

        return statistics

    ##################################################################
    # Largest Connected Component
    ##################################################################

    def largest_component(

        self,

        graph,

    ):

        """
        Returns the largest connected component.
        """

        if graph.number_of_nodes() == 0:

            return graph

        component = max(

            nx.connected_components(

                graph.to_undirected()

            ),

            key=len,

        )

        return graph.subgraph(

            component

        ).copy()

    ##################################################################
    # Degree Statistics
    ##################################################################

    def degree_statistics(

        self,

        graph,

    ):

        """
        Degree distribution statistics.
        """

        degrees = [

            degree

            for _, degree in graph.degree()

        ]

        return {

            "minimum":

                min(degrees),

            "maximum":

                max(degrees),

            "mean":

                float(

                    pd.Series(

                        degrees

                    ).mean()

                ),

            "median":

                float(

                    pd.Series(

                        degrees

                    ).median()

                ),

            "std":

                float(

                    pd.Series(

                        degrees

                    ).std()

                ),

        }

    ##################################################################
    # Summary
    ##################################################################

    def summary(

        self,

        graph,

    ):

        """
        Print graph summary.
        """

        stats = self.statistics(

            graph

        )

        print("\n")

        print("=" * 70)

        print("GRAPH NORMALIZATION SUMMARY")

        print("=" * 70)

        for key, value in stats.items():

            print(

                f"{key:<25}: {value}"

            )

        print("=" * 70)

    ##################################################################
    # Reset
    ##################################################################

    def reset(self):

        """
        Placeholder for future stateful implementations.
        """

        pass

    ##################################################################
    # Representation
    ##################################################################

    def __repr__(self):

        return (

            "GraphNormalizer()"

        )