"""
==============================================================
AQAGC

Stage 05

Risk Prioritization

Complete Risk Prioritization Pipeline

==============================================================
"""

from __future__ import annotations

from graph_loader import GraphLoader

from io_utils import (
    load_propagated_risk,
    load_attack_paths,
)

from node_risk_calculator import NodeRiskCalculator
from edge_risk_calculator import EdgeRiskCalculator
from path_risk_calculator import PathRiskCalculator

from priority_ranker import PriorityRanker
from critical_asset_identifier import CriticalAssetIdentifier
from risk_summary import RiskSummary


class RiskPrioritizationPipeline:
    """
    Complete Stage-05 execution pipeline.
    """

    def __init__(self):

        loader = GraphLoader()

        self.graph = loader.get_graph()

        self.nodes = loader.get_nodes()

        self.edges = loader.get_edges()

        self.propagated_probability = load_propagated_risk()

        self.attack_paths = load_attack_paths()

    ####################################################################
    # Node Risk
    ####################################################################

    def run_node_risk(self):

        calculator = NodeRiskCalculator(

            self.graph,

            self.nodes,

            self.propagated_probability,

        )

        return calculator.run()

    ####################################################################
    # Edge Risk
    ####################################################################

    def run_edge_risk(

        self,

        node_risk,

    ):

        calculator = EdgeRiskCalculator(

            self.graph,

            node_risk,

        )

        return calculator.run()

    ####################################################################
    # Path Risk
    ####################################################################

    def run_path_risk(

        self,

        node_risk,

    ):

        calculator = PathRiskCalculator(

            self.attack_paths,

            node_risk,

        )

        return calculator.run()

    ####################################################################
    # Priority Ranking
    ####################################################################

    def run_priority_ranking(

        self,

        node_risk,

    ):

        ranker = PriorityRanker(

            node_risk,

        )

        return ranker.run()

    ####################################################################
    # Critical Assets
    ####################################################################

    def run_critical_assets(

        self,

        ranking,

    ):

        identifier = CriticalAssetIdentifier(

            ranking,

        )

        return identifier.run()

    ####################################################################
    # Risk Summary
    ####################################################################

    def run_summary(

        self,

        node_risk,

        edge_risk,

        path_risk,

        critical_assets,

    ):

        summary = RiskSummary(

            node_risk,

            edge_risk,

            path_risk,

            critical_assets,

        )

        return summary.run()

    ####################################################################
    # Execute Pipeline
    ####################################################################

    def run(self):

        node_risk = self.run_node_risk()

        edge_risk = self.run_edge_risk(

            node_risk,

        )

        path_risk = self.run_path_risk(

            node_risk,

        )

        ranking = self.run_priority_ranking(

            node_risk,

        )

        critical_assets = self.run_critical_assets(

            ranking,

        )

        summary = self.run_summary(

            node_risk,

            edge_risk,

            path_risk,

            critical_assets,

        )

        return {

            "node_risk": node_risk,

            "edge_risk": edge_risk,

            "path_risk": path_risk,

            "priority_ranking": ranking,

            "critical_assets": critical_assets,

            "summary": summary,

        }


if __name__ == "__main__":

    pipeline = RiskPrioritizationPipeline()

    results = pipeline.run()

    print("\nStage-05 Risk Prioritization Completed Successfully\n")

    print(

        "Total Nodes:",

        len(results["node_risk"])

    )

    print(

        "Total Edges:",

        len(results["edge_risk"])

    )

    print(

        "Total Paths:",

        len(results["path_risk"])

    )

    print(

        "Critical Assets:",

        len(results["critical_assets"])

    )