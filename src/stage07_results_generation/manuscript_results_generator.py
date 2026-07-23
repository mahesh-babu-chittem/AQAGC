"""
==============================================================
AQAGC

Stage 07

Results Generation

Manuscript Results Generator

==============================================================
"""

from __future__ import annotations


import os



from data_loader import BenchmarkDataLoader



class ManuscriptResultsGenerator:


    ##################################################################
    # Initialization
    ##################################################################

    def __init__(

        self,

        data_root="../data/benchmark/CSE_CIC_IDS2018",

        output_root="outputs",

    ):


        self.output_root = output_root


        os.makedirs(

            self.output_root,

            exist_ok=True

        )


        self.loader = BenchmarkDataLoader(

            data_root=data_root

        )



        self.results = {}



    ##################################################################
    # Dataset Initialization
    ##################################################################

    def initialize_dataset(self):

        """
        Loads common dataset information.

        Loaded once and reused by all analyses.
        """


        print(

            "\nLoading AQAGC benchmark data..."

        )


        nodes = self.loader.load_nodes()

        edges = self.loader.load_edges()

        ground_truth = self.loader.load_ground_truth()

        metadata = self.loader.load_metadata()



        self.results["dataset"] = {


            "nodes":

                nodes,


            "edges":

                edges,


            "ground_truth":

                ground_truth,


            "metadata":

                metadata,

        }



        print(

            "Dataset loaded successfully."

        )



    ##################################################################
    # Attack Path Discovery Results
    ##################################################################

    def generate_apdt_results(self):

        """
        Generates:

            Attack Path Discovery Performance

        Corresponds to:

            APDT table
            QSEG analysis
            APDT figures

        """


        from apdt_analysis import APDTAnalysis



        analysis = APDTAnalysis(

            loader=self.loader,

            output_dir=os.path.join(

                self.output_root,

                "apdt"

            )

        )


        self.results["APDT"] = analysis.run()



    ##################################################################
    # Benchmark Comparison Results
    ##################################################################

    def generate_benchmark_results(self):

        """
        Generates classical vs quantum vs AQAGC
        comparison results.
        """


        from benchmark_analysis import BenchmarkAnalysis



        analysis = BenchmarkAnalysis(

            loader=self.loader,

            output_dir=os.path.join(

                self.output_root,

                "benchmark"

            )

        )


        self.results["Benchmark"] = analysis.run()



    ##################################################################
    # Quantum Efficiency Results
    ##################################################################

    def generate_quantum_results(self):

        """
        Generates:

            QSEG
            quantum efficiency
            scheduler analysis

        """


        from quantum_efficiency_analysis import (
            QuantumEfficiencyAnalysis
        )



        analysis = QuantumEfficiencyAnalysis(

            loader=self.loader,

            output_dir=os.path.join(

                self.output_root,

                "quantum"

            )

        )


        self.results["Quantum"] = analysis.run()



    ##################################################################
    # Risk Analysis Results
    ##################################################################

    def generate_risk_results(self):


        from risk_analysis import RiskAnalysis



        analysis = RiskAnalysis(

            loader=self.loader,

            output_dir=os.path.join(

                self.output_root,

                "risk"

            )

        )


        self.results["Risk"] = analysis.run()



    ##################################################################
    # Scalability Results
    ##################################################################

    def generate_scalability_results(self):


        from scalability_analysis import (
            ScalabilityAnalysis
        )


        analysis = ScalabilityAnalysis(

            loader=self.loader,

            output_dir=os.path.join(

                self.output_root,

                "scalability"

            )

        )


        self.results["Scalability"] = analysis.run()



    ##################################################################
    # Robustness Results
    ##################################################################

    def generate_robustness_results(self):


        from robustness_analysis import (
            RobustnessAnalysis
        )


        analysis = RobustnessAnalysis(

            loader=self.loader,

            output_dir=os.path.join(

                self.output_root,

                "robustness"

            )

        )


        self.results["Robustness"] = analysis.run()



    ##################################################################
    # Ablation Results
    ##################################################################

    def generate_ablation_results(self):


        from ablation_analysis import (
            AblationAnalysis
        )


        analysis = AblationAnalysis(

            loader=self.loader,

            output_dir=os.path.join(

                self.output_root,

                "ablation"

            )

        )


        self.results["Ablation"] = analysis.run()



    ##################################################################
    # Complete Manuscript Generation
    ##################################################################

    def run_all(self):


        self.initialize_dataset()



        self.generate_apdt_results()


        self.generate_benchmark_results()


        self.generate_quantum_results()


        self.generate_risk_results()


        self.generate_scalability_results()


        self.generate_robustness_results()


        self.generate_ablation_results()



        return self.results