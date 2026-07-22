"""
===========================================================================
AQAGC

Stage 2

Benchmark Builder

Pipeline

Processed Dataset
        │
        ▼
Node Extraction
        ▼
Edge Construction
        ▼
Vulnerability Assignment
        ▼
Edge Weight Assignment
        ▼
Graph Normalization
        ▼
Ground Truth Generation
        ▼
Benchmark Sampling
        ▼
Export

===========================================================================

"""

from pathlib import Path

import pandas as pd

from .node_extractor import NodeExtractor
from .edge_constructor import EdgeConstructor
from .vulnerability_mapper import VulnerabilityMapper
from .edge_weighter import EdgeWeighter
from .graph_normalizer import GraphNormalizer
from .ground_truth import GroundTruthGenerator
from .graph_sampler import GraphSampler
from .graph_exporter import GraphExporter


class BenchmarkBuilder:
    """
    Complete AQAGC Stage-2 benchmark pipeline.
    """

    ####################################################################
    # Constructor
    ####################################################################

    def __init__(

        self,

        output_directory="data/benchmark",

    ):

        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        ###############################################################

        self.node_extractor = NodeExtractor()

        self.vulnerability_mapper = VulnerabilityMapper()

        self.edge_weighter = EdgeWeighter()

        self.graph_normalizer = GraphNormalizer()

        self.ground_truth_generator = GroundTruthGenerator()

            ####################################################################
    # Build Single Dataset
    ####################################################################

    def build(

        self,

        dataframe: pd.DataFrame,

        dataset_name: str,

    ):

        print("\n")

        print("=" * 80)

        print(f"Building Benchmark : {dataset_name}")

        print("=" * 80)

        ################################################################
        # STEP 1
        ################################################################

        print("\n[1/8] Dataset-specific Node Extraction")

        nodes = self.node_extractor.extract(

            dataframe,

            dataset_name,

        )

        print(

            f"Generated Nodes : {len(nodes):,}"

        )

        ################################################################
        # STEP 2
        ################################################################

        print("\n[2/8] Dataset-specific Edge Construction")

        edge_constructor = EdgeConstructor(

            nodes,

        )

        edges = edge_constructor.build(

            dataframe,

            dataset_name,

        )

        print(

            f"Generated Edges : {len(edges):,}"

        )

        ################################################################
        # STEP 3
        ################################################################

        print("\n[3/8] Vulnerability Assignment")

        nodes = self.vulnerability_mapper.assign(

            nodes,

            edges,

        )

        print(

            "Assigned vulnerability attributes."

        )

        ###############################################################

        print(

            f"Average Risk Score : "

            f"{nodes['risk_score'].mean():.4f}"

        )

        print(

            f"Average Severity   : "

            f"{nodes['severity'].mean():.4f}"

        )

        print(

            f"Average Exploitability : "

            f"{nodes['exploitability'].mean():.4f}"

        )

        print(

            f"Average Privilege  : "

            f"{nodes['privilege'].mean():.4f}"

        )

        print(

            f"Average Communication Frequency : "

            f"{nodes['communication_frequency'].mean():.4f}"

        )

                ################################################################
        # STEP 4
        ################################################################

        print("\n[4/8] Edge Weight Assignment")

        edges = self.edge_weighter.assign(

            nodes,

            edges,

        )

        ###############################################################

        self.edge_weighter.validate(

            edges,

        )

        ###############################################################

        edge_stats = self.edge_weighter.statistics(

            edges,

        )

        print(

            f"Average Edge Weight : "

            f"{edge_stats['mean']:.4f}"

        )

        print(

            f"Maximum Edge Weight : "

            f"{edge_stats['maximum']:.4f}"

        )

        print(

            f"Minimum Edge Weight : "

            f"{edge_stats['minimum']:.4f}"

        )

        ###############################################################

        edges = self.edge_weighter.rank_edges(

            edges,

        )

        ################################################################
        # STEP 5
        ################################################################

        print("\n[5/8] Graph Normalization")

        (

            graph,

            nodes,

            edges,

        ) = self.graph_normalizer.normalize(

            nodes,

            edges,

        )

        ###############################################################

        self.graph_normalizer.validate(

            graph,

        )

        ###############################################################

        graph_stats = (

            self.graph_normalizer.statistics(

                graph,

            )

        )

        print(

            f"Nodes                : "

            f"{graph_stats['nodes']:,}"

        )

        print(

            f"Edges                : "

            f"{graph_stats['edges']:,}"

        )

        print(

            f"Density              : "

            f"{graph_stats['density']:.6f}"

        )

        print(

            f"Connected Components : "

            f"{graph_stats['connected_components']}"

        )

        ###############################################################

        largest_component = (

            self.graph_normalizer.largest_component(

                graph,

            )

        )

        print(

            f"Largest Component    : "

            f"{largest_component.number_of_nodes():,} nodes"

        )

        ###############################################################

        degree_stats = (

            self.graph_normalizer.degree_statistics(

                graph,

            )

        )

        print(

            f"Average Degree       : "

            f"{degree_stats['mean']:.2f}"

        )

                ################################################################
        # STEP 6
        ################################################################

        print("\n[6/8] Ground Truth Generation")

        ground_truth = (

            self.ground_truth_generator.generate(

                graph,

            )

        )

        ###############################################################

        self.ground_truth_generator.validate(

            ground_truth,

        )

        ###############################################################

        ground_truth_stats = (

            self.ground_truth_generator.statistics(

                ground_truth,

            )

        )

        print(

            f"Critical Paths        : "

            f"{ground_truth_stats['critical_paths']:,}"

        )

        print(

            f"Average Path Length   : "

            f"{ground_truth_stats['average_path_length']:.2f}"

        )

        print(

            f"Average Path Risk     : "

            f"{ground_truth_stats['average_risk']:.4f}"

        )

        ################################################################
        # STEP 7
        ################################################################

        print("\n[7/8] Benchmark Graph Sampling")

        sampler = GraphSampler(

            self.output_directory

            /

            dataset_name,

        )

        ###############################################################

        benchmark_graphs = {}

        ###############################################################
        # Generate 20 deterministic benchmark instances
        ###############################################################

        for instance in range(1, 21):

            print(

                f"\nGenerating Instance {instance:02d}/20"

            )

            instance_graphs = sampler.generate(

                graph,

                instance=instance,

            )

            ###########################################################

            for size, graphs in instance_graphs.items():

                benchmark_graphs.setdefault(

                    size,

                    []

                ).extend(

                    graphs

                )

        ###############################################################

        sampler.verify(

            benchmark_graphs,

        )

        ###############################################################

        sampler.summary(

            benchmark_graphs,

        )

                ################################################################
        # STEP 8
        ################################################################

        print("\n[8/8] Export Benchmark")

        exporter = GraphExporter(

            self.output_directory

            /

            dataset_name,

        )

        ###############################################################

        exporter.validate(

            graph,

            nodes,

            edges,

        )

        ###############################################################

        exporter.export_all(

            graph=graph,

            nodes=nodes,

            edges=edges,

            ground_truth=ground_truth,

            benchmark_graphs=benchmark_graphs,

        )

        ###############################################################

        print("\n")

        print("=" * 80)

        print(

            f"{dataset_name} benchmark completed successfully."

        )

        print("=" * 80)

        print("\n")

        ###############################################################

        return {

            "dataset": dataset_name,

            "graph": graph,

            "nodes": nodes,

            "edges": edges,

            "ground_truth": ground_truth,

            "benchmark_graphs": benchmark_graphs,

        }
    
        ####################################################################
    # Build Multiple Datasets
    ####################################################################

    def build_all(

        self,

        datasets,

    ):

        """
        Build AQAGC benchmarks for all processed datasets.

        Parameters
        ----------
        datasets : dict

            {

                dataset_name : dataframe

            }

        Returns
        -------
        dict

            Benchmark results.
        """

        results = {}

        successful = 0

        failed = 0

        print("\n")

        print("=" * 80)

        print("AQAGC STAGE 2")

        print("Attack Graph Benchmark Construction")

        print("=" * 80)

        ###############################################################

        for dataset_name, dataframe in datasets.items():

            try:

                result = self.build(

                    dataframe,

                    dataset_name,

                )

                results[dataset_name] = result

                successful += 1

            except Exception as error:

                failed += 1

                print("\n")

                print("=" * 80)

                print(

                    f"ERROR while processing {dataset_name}"

                )

                print(error)

                print("=" * 80)

                print("\n")

        ###############################################################

        print("\n")

        print("=" * 80)

        print("AQAGC STAGE 2 SUMMARY")

        print("=" * 80)

        print(

            f"Datasets Processed : {len(datasets)}"

        )

        print(

            f"Successful         : {successful}"

        )

        print(

            f"Failed             : {failed}"

        )

        print("=" * 80)

        print("\n")

        return results

    ####################################################################
    # Output Directory
    ####################################################################

    @property

    def output_path(

        self,

    ):

        return self.output_directory

    ####################################################################
    # Reset
    ####################################################################

    def reset(

        self,

    ):

        """
        Reset builder state.

        Current implementation is stateless.
        """

        self.node_extractor = NodeExtractor()

        self.vulnerability_mapper = VulnerabilityMapper()

        self.edge_weighter = EdgeWeighter()

        self.graph_normalizer = GraphNormalizer()

        self.ground_truth_generator = GroundTruthGenerator()

    ####################################################################
    # Representation
    ####################################################################

    def __repr__(

        self,

    ):

        return (

            "BenchmarkBuilder("

            f"output_directory='{self.output_directory}'"

            ")"

        )