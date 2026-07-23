"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Configuration Module

==============================================================
"""

from pathlib import Path


####################################################################
# Project Paths
####################################################################

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

RESULT_DIR = PROJECT_ROOT / "results"


STAGE05_OUTPUT_DIR = DATA_DIR / "stage05"

STAGE06_OUTPUT_DIR = DATA_DIR / "stage06"


####################################################################
# Stage-05 Input Files
####################################################################

NODE_RISK_FILE = (
    STAGE05_OUTPUT_DIR /
    "node_risk_scores.csv"
)


EDGE_RISK_FILE = (
    STAGE05_OUTPUT_DIR /
    "edge_risk_scores.csv"
)


PATH_RISK_FILE = (
    STAGE05_OUTPUT_DIR /
    "path_risk_scores.csv"
)


PRIORITY_PATH_FILE = (
    STAGE05_OUTPUT_DIR /
    "priority_attack_paths.csv"
)


GROUND_TRUTH_FILE = (
    STAGE05_OUTPUT_DIR /
    "ground_truth_paths.csv"
)


####################################################################
# Stage-06 Output Files
####################################################################

BASELINE_RESULTS_DIR = (
    STAGE06_OUTPUT_DIR /
    "baseline_results"
)


AQAGC_RESULTS_DIR = (
    STAGE06_OUTPUT_DIR /
    "aqagc_results"
)


METRICS_DIR = (
    STAGE06_OUTPUT_DIR /
    "metrics"
)


STATISTICS_DIR = (
    STAGE06_OUTPUT_DIR /
    "statistics"
)


ROBUSTNESS_DIR = (
    STAGE06_OUTPUT_DIR /
    "robustness"
)


ABLATION_DIR = (
    STAGE06_OUTPUT_DIR /
    "ablation"
)


####################################################################
# Benchmark Methods
####################################################################

BASELINE_METHODS = [

    "BFS",

    "DFS",

    "AStar",

    "Markov",

    "DTQW",

    "CTQW",

    "QAGC",

]


PROPOSED_METHOD = "AQAGC"


####################################################################
# Ranking Parameters
####################################################################

TOP_K = 10


####################################################################
# Statistical Parameters
####################################################################

CONFIDENCE_LEVEL = 0.95

SIGNIFICANCE_LEVEL = 0.05


####################################################################
# Quantum Parameters
####################################################################

DEFAULT_WALK_STEPS = 100

DEFAULT_NOISE_LEVEL = 0.01


####################################################################
# Create Directories
####################################################################

for directory in [

    RESULT_DIR,

    STAGE06_OUTPUT_DIR,

    BASELINE_RESULTS_DIR,

    AQAGC_RESULTS_DIR,

    METRICS_DIR,

    STATISTICS_DIR,

    ROBUSTNESS_DIR,

    ABLATION_DIR,

]:

    directory.mkdir(

        parents=True,

        exist_ok=True

    )