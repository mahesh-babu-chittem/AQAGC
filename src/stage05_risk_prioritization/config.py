"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Configuration File

==============================================================
"""

from pathlib import Path

###############################################################
# Directories
###############################################################

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

STAGE04_DIR = DATA_DIR / "stage04"

STAGE05_DIR = DATA_DIR / "stage05"

RESULTS_DIR = PROJECT_ROOT / "results"

LOG_DIR = PROJECT_ROOT / "logs"

###############################################################
# Input Files (Stage 04)
###############################################################

HYBRID_STATE_FILE = (
    STAGE04_DIR / "hybrid_state.npy"
)

DTQW_STATE_FILE = (
    STAGE04_DIR / "dtqw_state.npy"
)

CTQW_STATE_FILE = (
    STAGE04_DIR / "ctqw_state.npy"
)

PROPAGATED_RISK_FILE = (
    STAGE04_DIR / "propagated_risk.npy"
)

ATTACK_PATH_FILE = (
    STAGE04_DIR / "attack_paths.json"
)

GRAPH_FILE = (
    STAGE04_DIR / "attack_graph.graphml"
)

NODE_FILE = (
    STAGE04_DIR / "nodes.csv"
)

EDGE_FILE = (
    STAGE04_DIR / "edges.csv"
)

###############################################################
# Output Files
###############################################################

NODE_RISK_FILE = (
    STAGE05_DIR / "node_risk_scores.csv"
)

EDGE_RISK_FILE = (
    STAGE05_DIR / "edge_risk_scores.csv"
)

PATH_RISK_FILE = (
    STAGE05_DIR / "path_risk_scores.csv"
)

PRIORITY_RANKING_FILE = (
    STAGE05_DIR / "priority_ranking.csv"
)

CRITICAL_ASSETS_FILE = (
    STAGE05_DIR / "critical_assets.csv"
)

RISK_SUMMARY_FILE = (
    STAGE05_DIR / "risk_summary.json"
)

###############################################################
# Risk Weights
###############################################################

QUANTUM_WEIGHT = 0.60

CVSS_WEIGHT = 0.20

CENTRALITY_WEIGHT = 0.10

PATH_WEIGHT = 0.10

###############################################################
# Ranking Parameters
###############################################################

TOP_K_NODES = 20

TOP_K_PATHS = 20

TOP_K_ASSETS = 20

HIGH_RISK_THRESHOLD = 0.80

MEDIUM_RISK_THRESHOLD = 0.50

LOW_RISK_THRESHOLD = 0.20

###############################################################
# Numerical Constants
###############################################################

EPSILON = 1e-12

RANDOM_STATE = 42

###############################################################
# Create Directories
###############################################################

STAGE05_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)