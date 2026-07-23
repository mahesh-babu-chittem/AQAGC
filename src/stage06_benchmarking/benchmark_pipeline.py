"""
==============================================================
AQAGC

Stage 06

Benchmarking and Evaluation

Complete Benchmark Pipeline

==============================================================
"""

from __future__ import annotations

import pandas as pd


from benchmark_dataset import BenchmarkDataset

from benchmark_manager import BenchmarkManager

from ranking_metrics import RankingMetrics

from quantum_metrics import QuantumMetrics

from runtime_profiler import RuntimeProfiler

from memory_profiler import MemoryProfiler

from statistical_analysis import StatisticalAnalyzer

from effect_size import EffectSizeAnalyzer

from multiple_comparison import MultipleComparisonCorrection

from robustness_analysis import RobustnessAnalyzer

from ablation_study import AblationStudy



class BenchmarkPipeline:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(

        self,

        graph,

        config=None,

    ):

        self.graph = graph

        self.config = config


        self.dataset = BenchmarkDataset()


        self.manager = BenchmarkManager(

            graph=self.graph,

            config=self.config,

        )


        self.results = None

        self.metrics = None



    ####################################################################
    # Load Dataset
    ####################################################################

    def load_dataset(self):

        self.dataset.load()

        return self.dataset.validate()



    ####################################################################
    # Benchmark Execution
    ####################################################################

    def run_benchmark(self):

        output = self.manager.run()


        self.results = output


        return output



    ####################################################################
    # Ranking Evaluation
    ####################################################################

    def evaluate_ranking(

        self,

        predicted,

        ground_truth,

    ):

        evaluator = RankingMetrics(

            predicted_ranking=predicted,

            ground_truth=ground_truth,

        )


        self.metrics = evaluator.calculate_all()


        return self.metrics



    ####################################################################
    # Quantum Evaluation
    ####################################################################

    def evaluate_quantum(

        self,

        **kwargs

    ):

        evaluator = QuantumMetrics()


        return evaluator.calculate(

            **kwargs

        )



    ####################################################################
    # Statistical Evaluation
    ####################################################################

    def statistical_analysis(

        self,

    ):

        return StatisticalAnalyzer()



    ####################################################################
    # Effect Size
    ####################################################################

    def effect_analysis(self):

        return EffectSizeAnalyzer()



    ####################################################################
    # Multiple Comparison
    ####################################################################

    def correction_analysis(self):

        return MultipleComparisonCorrection()



    ####################################################################
    # Robustness
    ####################################################################

    def robustness_analysis(self):

        return RobustnessAnalyzer(

            self.graph

        )



    ####################################################################
    # Complete Pipeline
    ####################################################################

    def run(self):


        self.load_dataset()


        benchmark_output = self.run_benchmark()


        return {

            "Benchmark":

                benchmark_output,


            "Dataset":

                self.dataset.statistics(),

        }