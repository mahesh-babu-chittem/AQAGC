"""
===========================================================================
AQAGC

Stage 2

Graph Sampler

Implements deterministic benchmark graph generation.

Unlike random graph sampling, this module extracts
reproducible benchmark graphs of predefined sizes.

Benchmark Sizes

50
200
500
1000
2000
5000

===========================================================================

"""

from __future__ import annotations

from pathlib import Path

import networkx as nx


class GraphSampler:

    """
    Deterministic benchmark graph generator.

    Input

        Complete normalized attack graph

    Output

        {

            50   : [graph],

            200  : [graph],

            500  : [graph],

            1000 : [graph],

            2000 : [graph],

            5000 : [graph]

        }

    """

    ##################################################################

    def __init__(

        self,

        output_directory,

        graph_sizes=None,

    ):

        self.output_directory = Path(

            output_directory

        )

        self.output_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        ##############################################################

        if graph_sizes is None:

            graph_sizes = [

                50,

                200,

                500,

                1000,

                2000,

                5000,

            ]

        ##############################################################

        self.graph_sizes = sorted(

            graph_sizes

        )

            ##################################################################
    # Public API
    ##################################################################

    def generate(

        self,

        graph: nx.DiGraph,

        instance=1,

    ):

        """
        Generate deterministic benchmark graphs.

        Returns

        {

            50   : [graph],

            200  : [graph],

            ...

        }
        """

        print("\nGenerating Benchmark Graph Collection...")

        ##############################################################

        ranked_nodes = self._rank_nodes(

            graph,

        )

        ##############################################################

        benchmark_graphs = {}

        ##############################################################

        for size in self.graph_sizes:

            if size > graph.number_of_nodes():

                print(

                    f"Skipping {size} nodes "

                    f"(graph contains only "

                    f"{graph.number_of_nodes()} nodes)"

                )

                continue

            ##########################################################

            benchmark_graphs[size] = []

            ##########################################################

            subgraph = self._extract_subgraph(

                graph,

                ranked_nodes,

                size,

                instance,

            )

            benchmark_graphs[size].append(

                subgraph

            )

            print(

                f"Generated benchmark "

                f"{size:>5} nodes"

            )

        ##############################################################

        return benchmark_graphs

    ##################################################################
    # Node Ranking
    ##################################################################

    def _rank_nodes(

        self,

        graph,

    ):

        """
        Deterministically rank nodes.

        Ranking Priority

        1. Risk Score
        2. Degree
        3. Node ID
        """

        ranked = []

        ##############################################################

        for node in graph.nodes():

            attributes = graph.nodes[node]

            ranked.append(

                (

                    node,

                    float(

                        attributes.get(

                            "risk_score",

                            0.0,

                        )

                    ),

                    graph.degree(

                        node

                    ),

                )

            )

        ##############################################################

        ranked = sorted(

            ranked,

            key=lambda x:

            (

                -x[1],      # highest risk first

                -x[2],      # highest degree first

                x[0],       # deterministic

            ),

        )

        ##############################################################

        return [

            node

            for node, _, _

            in ranked

        ]
    
        ##################################################################
    # Extract Benchmark Subgraph
    ##################################################################

    def _extract_subgraph(

        self,

        graph,

        ranked_nodes,

        target_size,

        instance,

    ):

        """
        Deterministically extract a connected benchmark graph.

        Strategy

        1. Select highest-ranked unused seed
        2. Perform BFS expansion
        3. Continue until target size is reached
        4. If BFS finishes early, restart from the next
           highest-ranked remaining node
        """

        ##############################################################

        selected = set()

        visited = set()

        queue = []

        ##############################################################
        # Highest-ranked seed
        ##############################################################

        instance_index = max(
            0,
            min(
                instance - 1,

                len(ranked_nodes) - 1,
            )
        )

        seed = ranked_nodes[instance_index]

        queue.append(

            seed

        )

        visited.add(

            seed

        )

        ##############################################################

        while (

            queue

            and

            len(selected) < target_size

        ):

            current = queue.pop(0)

            selected.add(

                current

            )

            ##########################################################

            neighbours = sorted(

                graph.successors(

                    current

                )

            )

            ##########################################################

            for neighbour in neighbours:

                if (

                    neighbour not in visited

                    and

                    len(selected) < target_size

                ):

                    visited.add(

                        neighbour

                    )

                    queue.append(

                        neighbour

                    )

                            ##############################################################
        # Continue from remaining ranked nodes if BFS ended early
        ##############################################################

        if len(selected) < target_size:

            for node in ranked_nodes:

                if len(selected) >= target_size:

                    break

                if node in selected:

                    continue

                queue = [node]

                visited.add(node)

                while (

                    queue

                    and

                    len(selected) < target_size

                ):

                    current = queue.pop(0)

                    if current not in selected:

                        selected.add(current)

                    neighbours = sorted(

                        graph.successors(current)

                    )

                    for neighbour in neighbours:

                        if (

                            neighbour not in visited

                            and

                            len(selected) < target_size

                        ):

                            visited.add(neighbour)

                            queue.append(neighbour)

        ##############################################################
        # Create induced subgraph
        ##############################################################

        selected = list(selected)[:target_size]

        subgraph = graph.subgraph(

            selected

        ).copy()

        return subgraph
    
    ##################################################################
    # Validate Benchmark Graph
    ##################################################################

    def validate(

        self,

        graph: nx.DiGraph,

    ):

        """
        Validate a generated benchmark graph.
        """

        if graph.number_of_nodes() == 0:

            raise ValueError(

                "Benchmark graph contains no nodes."

            )

        if graph.number_of_edges() == 0:

            raise ValueError(

                "Benchmark graph contains no edges."

            )

        ##############################################################

        if not nx.is_directed(

            graph

        ):

            raise ValueError(

                "Benchmark graph must be directed."

            )

        return True

    ##################################################################
    # Graph Statistics
    ##################################################################

    def graph_statistics(

        self,

        graph,

    ):

        """
        Compute benchmark graph statistics.
        """

        statistics = {

            "nodes":

                graph.number_of_nodes(),

            "edges":

                graph.number_of_edges(),

            "density":

                nx.density(

                    graph

                ),

            "average_degree":

                sum(

                    dict(

                        graph.degree()

                    ).values()

                )

                /

                graph.number_of_nodes(),

            "self_loops":

                nx.number_of_selfloops(

                    graph

                ),

        }

        ##############################################################

        try:

            statistics[

                "connected_components"

            ] = nx.number_connected_components(

                graph.to_undirected()

            )

        except Exception:

            statistics[

                "connected_components"

            ] = 1

        ##############################################################

        return statistics

    ##################################################################
    # Benchmark Collection Statistics
    ##################################################################

    def benchmark_statistics(

        self,

        benchmark_graphs,

    ):

        """
        Compute statistics for the complete benchmark collection.
        """

        summary = {}

        ##############################################################

        for size, graphs in benchmark_graphs.items():

            graph = graphs[0]

            summary[size] = self.graph_statistics(

                graph

            )

        ##############################################################

        return summary

    ##################################################################
    # Verify Benchmark Sizes
    ##################################################################

    def verify(

        self,

        benchmark_graphs,

    ):

        """
        Verify that every benchmark graph has the
        expected number of nodes.
        """

        for size, graphs in benchmark_graphs.items():

            graph = graphs[0]

            if graph.number_of_nodes() != size:

                raise ValueError(

                    f"Expected {size} nodes "

                    f"but obtained "

                    f"{graph.number_of_nodes()}."

                )

        return True
    
        ##################################################################
    # Benchmark Summary
    ##################################################################

    def summary(

        self,

        benchmark_graphs,

    ):

        """
        Print benchmark summary.
        """

        print("\n")

        print("=" * 70)

        print("AQAGC BENCHMARK COLLECTION")

        print("=" * 70)

        ##############################################################

        for size in sorted(

            benchmark_graphs.keys()

        ):

            graph = benchmark_graphs[size][0]

            stats = self.graph_statistics(

                graph

            )

            print(

                f"{size:>5} Nodes"

                f" | "

                f"Edges: {stats['edges']:>7}"

                f" | "

                f"Density: {stats['density']:.6f}"

                f" | "

                f"Components: "

                f"{stats['connected_components']}"

            )

        ##############################################################

        print("=" * 70)

    ##################################################################
    # Export Benchmark Metadata
    ##################################################################

    def benchmark_metadata(

        self,

        benchmark_graphs,

    ):

        """
        Create benchmark metadata dictionary.
        """

        metadata = {}

        ##############################################################

        for size, graphs in benchmark_graphs.items():

            graph = graphs[0]

            stats = self.graph_statistics(

                graph

            )

            ##########################################################

            metadata[str(size)] = {

                "nodes":

                    graph.number_of_nodes(),

                "edges":

                    graph.number_of_edges(),

                "density":

                    stats["density"],

                "average_degree":

                    stats["average_degree"],

                "components":

                    stats["connected_components"],

            }

        ##############################################################

        return metadata

    ##################################################################
    # Available Benchmark Sizes
    ##################################################################

    def available_sizes(

        self,

    ):

        """
        Return configured benchmark sizes.
        """

        return list(

            self.graph_sizes

        )

    ##################################################################
    # Largest Benchmark
    ##################################################################

    def largest_graph(

        self,

        benchmark_graphs,

    ):

        """
        Return largest generated benchmark graph.
        """

        if len(

            benchmark_graphs

        ) == 0:

            return None

        ##############################################################

        size = max(

            benchmark_graphs.keys()

        )

        return benchmark_graphs[size][0]

    ##################################################################
    # Smallest Benchmark
    ##################################################################

    def smallest_graph(

        self,

        benchmark_graphs,

    ):

        """
        Return smallest generated benchmark graph.
        """

        if len(

            benchmark_graphs

        ) == 0:

            return None

        ##############################################################

        size = min(

            benchmark_graphs.keys()

        )

        return benchmark_graphs[size][0]
    
        ##################################################################
    # Update Configuration
    ##################################################################

    def update_configuration(

        self,

        graph_sizes=None,

    ):

        """
        Update benchmark graph sizes.

        Sizes are automatically sorted and duplicates removed.
        """

        if graph_sizes is not None:

            graph_sizes = sorted(

                set(

                    int(size)

                    for size in graph_sizes

                    if int(size) > 0

                )

            )

            if len(graph_sizes) == 0:

                raise ValueError(

                    "At least one benchmark size is required."

                )

            self.graph_sizes = graph_sizes

    ##################################################################
    # Future Multi-Instance Generator
    ##################################################################

    ##################################################################
    # Reset
    ##################################################################

    def reset(

        self,

    ):

        """
        Restore default AQAGC benchmark sizes.
        """

        self.graph_sizes = [

            50,

            200,

            500,

            1000,

            2000,

            5000,

        ]

    ##################################################################
    # String Representation
    ##################################################################

    def __repr__(

        self,

    ):

        return (

            "GraphSampler("

            f"graph_sizes={self.graph_sizes}"

            ")"

        )