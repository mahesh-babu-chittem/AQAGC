"""
===========================================================================
AQAGC
Adaptive Quantum Attack Graph Compiler

Stage 2

Run Graph Construction

This script executes the complete deterministic benchmark construction
pipeline.

Pipeline

Processed Dataset
        ↓
Attack Graph Construction
        ↓
Benchmark Generation
        ↓
Export

===========================================================================

"""

from pathlib import Path
import logging
from numpy import rint
import pandas as pd
from scipy import datasets

from .benchmark_builder import BenchmarkBuilder


###############################################################################
# Logging
###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger("AQAGC")


###############################################################################
# Dataset Loader
###############################################################################

PROCESSED_DATASETS = {

    "CSE_CIC_IDS2018":
        "data/processed/CSE_CIC_IDS2018_processed.csv",

}


###############################################################################
# Load datasets
###############################################################################

def load_processed_datasets():

    datasets = {}

    LOGGER.info("Loading processed datasets...")

    for name, path in PROCESSED_DATASETS.items():

        path = Path(path)

        if not path.exists():

            raise FileNotFoundError(path)

        LOGGER.info(f"Loading {name}")

        df = pd.read_csv(path)

        LOGGER.info(

            f"{name} Shape : {df.shape}"

        )

        datasets[name] = df

    LOGGER.info("")

    LOGGER.info("All datasets loaded successfully.")

    return datasets


###############################################################################
# Main
###############################################################################

def main():

    LOGGER.info("")

    LOGGER.info("=" * 80)

    LOGGER.info("AQAGC GRAPH CONSTRUCTION STARTED")

    LOGGER.info("=" * 80)

    ###########################################################################
    # Load processed datasets
    ###########################################################################

    datasets = load_processed_datasets()

    ###########################################################################
    # Builder
    ###########################################################################

    builder = BenchmarkBuilder(

        output_directory="data/benchmark",

    )

    ###########################################################################
    # Build graphs
    ###########################################################################

    results = builder.build_all(
        datasets=datasets,
    )

    ###########################################################################
    # Summary
    ###########################################################################

    LOGGER.info("")

    LOGGER.info("=" * 80)

    LOGGER.info("GRAPH CONSTRUCTION SUMMARY")

    LOGGER.info("=" * 80)

    for dataset, result in results.items():

        graph = result["graph"]

        LOGGER.info(

            f"{dataset:<20}"

            f"Nodes : {graph.number_of_nodes():>8,}"

            f"    "

            f"Edges : {graph.number_of_edges():>8,}"

        )

    LOGGER.info("=" * 80)

    LOGGER.info("STAGE 2 COMPLETED SUCCESSFULLY")

    LOGGER.info("=" * 80)

    LOGGER.info("")

    print("\n")

    print("=" * 80)

    print("AQAGC ATTACK GRAPH BENCHMARKS GENERATED SUCCESSFULLY")

    print("=" * 80)

    print("\nBenchmark directory")

    print("data/benchmark/")

    print("\nGenerated files")

    print("---------------------------")

    print("nodes.csv")

    print("edges.csv")

    print("ground_truth.csv")

    print("metadata.json")

    print("AQAGC_Attack_Graph.graphml")

    print("benchmark_graphs/")

    print("\nReady for Stage 3 (VAQE).")

    print("=" * 80)


###############################################################################

if __name__ == "__main__":

    main()