"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Stage Execution Entry Point

==============================================================
"""

from __future__ import annotations

import networkx as nx


from benchmark_pipeline import BenchmarkPipeline



####################################################################
# Load Attack Graph
####################################################################

def load_attack_graph():


    graph_path = (

        "../data/stage05/attack_graph.gpickle"

    )


    graph = nx.read_gpickle(

        graph_path

    )


    return graph



####################################################################
# Main Stage 06 Execution
####################################################################

def main():


    print(

        "=" * 70

    )

    print(

        "AQAGC Stage 06 Benchmarking Started"

    )

    print(

        "=" * 70

    )



    ################################################################
    # Load Graph
    ################################################################

    graph = load_attack_graph()



    print(

        f"Loaded Graph: "

        f"{graph.number_of_nodes()} nodes, "

        f"{graph.number_of_edges()} edges"

    )



    ################################################################
    # Create Pipeline
    ################################################################

    pipeline = BenchmarkPipeline(

        graph=graph

    )



    ################################################################
    # Execute Benchmark
    ################################################################

    results = pipeline.run()



    ################################################################
    # Summary
    ################################################################

    print()

    print(

        "=" * 70

    )

    print(

        "Stage 06 Completed"

    )

    print(

        "=" * 70

    )


    print()

    print(

        "Dataset Statistics:"

    )


    print(

        results["Dataset"]

    )


    print()

    print(

        "Benchmark Methods Executed:"

    )


    for method in results["Benchmark"]["summary"]["Methods"]:

        print(

            " -",

            method

        )



####################################################################
# Run
####################################################################

if __name__ == "__main__":

    main()