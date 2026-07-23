"""
==============================================================
AQAGC

Stage 04

Adaptive Hybrid DTQW–CTQW Scheduler

Complete Scheduler Pipeline

==============================================================
"""

from __future__ import annotations

import numpy as np

from io_utils import (
    load_attack_graph,
)

from graph_converter import GraphConverter
from adjacency_matrix import AdjacencyMatrix
from laplacian_builder import LaplacianBuilder

from hybrid_scheduler import HybridScheduler
from probability_propagator import ProbabilityPropagator
from attack_path_extractor import AttackPathExtractor


class SchedulerPipeline:
    """
    Complete Stage-04 Pipeline.
    """

    def __init__(self):

        self.graph = load_attack_graph()

    ####################################################################
    # Graph Preparation
    ####################################################################

    def prepare_graph(self):

        converter = GraphConverter(

            self.graph

        )

        converter.summary()

        adjacency = AdjacencyMatrix(

            self.graph

        )

        adjacency_matrix = adjacency.build()

        laplacian = LaplacianBuilder(

            adjacency_matrix

        )

        laplacian.build()

        return adjacency_matrix

    ####################################################################
    # Hybrid Scheduler
    ####################################################################

    def run_scheduler(self):

        scheduler = HybridScheduler(

            number_of_nodes=self.graph.number_of_nodes()

        )

        hybrid_state = scheduler.run()

        hybrid_probability = scheduler.probabilities(

            hybrid_state

        )

        return hybrid_probability

    ####################################################################
    # Probability Propagation
    ####################################################################

    def propagate_probability(

        self,

        probability,

    ):

        propagator = ProbabilityPropagator(

            self.graph

        )

        propagated_probability = propagator.run(

            probability

        )

        return propagated_probability

    ####################################################################
    # Attack Path Extraction
    ####################################################################

    def extract_attack_paths(

        self,

        propagated_probability,

    ):

        extractor = AttackPathExtractor(

            self.graph

        )

        attack_paths = extractor.run(

            propagated_probability

        )

        return attack_paths

    ####################################################################
    # Execute Pipeline
    ####################################################################

    def run(self):

        self.prepare_graph()

        hybrid_probability = self.run_scheduler()

        propagated_probability = self.propagate_probability(

            hybrid_probability

        )

        attack_paths = self.extract_attack_paths(

            propagated_probability

        )

        return {

            "hybrid_probability": hybrid_probability,

            "propagated_probability": propagated_probability,

            "attack_paths": attack_paths,

        }

    ####################################################################
    # Pipeline Summary
    ####################################################################

    def summary(self):

        results = self.run()

        return {

            "nodes":

                self.graph.number_of_nodes(),

            "edges":

                self.graph.number_of_edges(),

            "attack_paths":

                len(

                    results["attack_paths"]

                ),

            "maximum_probability":

                float(

                    np.max(

                        results["propagated_probability"]

                    )

                ),

            "minimum_probability":

                float(

                    np.min(

                        results["propagated_probability"]

                    )

                ),

        }


if __name__ == "__main__":

    pipeline = SchedulerPipeline()

    results = pipeline.run()

    print("\nStage 04 Completed Successfully\n")

    print(

        "Number of attack paths:",

        len(results["attack_paths"])

    )