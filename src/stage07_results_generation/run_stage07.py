"""
==============================================================
AQAGC

Stage 07

Results Generation Pipeline Runner

==============================================================
"""


from __future__ import annotations



import os
import json
from datetime import datetime



from results_loader import ResultsLoader



from apdt_analysis import (
    APDTAnalysis
)


from ranking_analysis import (
    RankingAnalysis
)


from scalability_analysis import (
    ScalabilityAnalysis
)


from quantum_dynamics_analysis import (
    QuantumDynamicsAnalysis
)


from ablation_analysis import (
    AblationAnalysis
)


from hyperparameter_analysis import (
    HyperparameterAnalysis
)


from explainability_analysis import (
    ExplainabilityAnalysis
)


from statistical_analysis import (
    StatisticalAnalysis
)





class Stage07Runner:
    """
    Complete AQAGC manuscript
    result generation pipeline.

    """



    ##############################################################
    # Initialization
    ##############################################################

    def __init__(

        self,

        data_root="../data/benchmark/CSE_CIC_IDS2018",

        output_dir="outputs/stage07"

    ):


        self.output_dir = output_dir


        os.makedirs(

            output_dir,

            exist_ok=True

        )


        self.loader = ResultsLoader(

            data_root=data_root

        )


        self.summary = {}



    ##############################################################
    # Run APDT
    ##############################################################

    def run_apdt(self):


        print(

            "\n[1/8] Attack Path Discovery Performance"

        )


        result = APDTAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "apdt"

            )

        ).run()



        self.summary["APDT"] = "Completed"



    ##############################################################
    # Run Ranking
    ##############################################################

    def run_ranking(self):


        print(

            "\n[2/8] Attack Path Ranking Performance"

        )


        RankingAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "ranking"

            )

        ).run()



        self.summary["Ranking"] = "Completed"



    ##############################################################
    # Run Scalability
    ##############################################################

    def run_scalability(self):


        print(

            "\n[3/8] Scalability Evaluation"

        )


        ScalabilityAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "scalability"

            )

        ).run()



        self.summary["Scalability"] = "Completed"



    ##############################################################
    # Run Quantum Dynamics
    ##############################################################

    def run_quantum_dynamics(self):


        print(

            "\n[4/8] Quantum Exploration Dynamics"

        )


        QuantumDynamicsAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "quantum_dynamics"

            )

        ).run()



        self.summary["Quantum Dynamics"] = "Completed"



    ##############################################################
    # Run Ablation
    ##############################################################

    def run_ablation(self):


        print(

            "\n[5/8] Ablation Study"

        )


        AblationAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "ablation"

            )

        ).run()



        self.summary["Ablation"] = "Completed"



    ##############################################################
    # Run Hyperparameter
    ##############################################################

    def run_hyperparameter(self):


        print(

            "\n[6/8] Hyperparameter Sensitivity"

        )


        HyperparameterAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "hyperparameter"

            )

        ).run()



        self.summary["Hyperparameter"] = "Completed"



    ##############################################################
    # Run Explainability
    ##############################################################

    def run_explainability(self):


        print(

            "\n[7/8] Explainability Analysis"

        )


        ExplainabilityAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "explainability"

            )

        ).run()



        self.summary["Explainability"] = "Completed"



    ##############################################################
    # Run Statistics
    ##############################################################

    def run_statistics(self):


        print(

            "\n[8/8] Statistical Significance Analysis"

        )


        StatisticalAnalysis(

            self.loader,

            os.path.join(

                self.output_dir,

                "statistical"

            )

        ).run()



        self.summary["Statistics"] = "Completed"



    ##############################################################
    # Save Pipeline Summary
    ##############################################################

    def save_summary(self):


        self.summary["Execution_Time"] = str(

            datetime.now()

        )



        with open(

            os.path.join(

                self.output_dir,

                "stage07_summary.json"

            ),

            "w"

        ) as file:


            json.dump(

                self.summary,

                file,

                indent=4

            )



    ##############################################################
    # Execute Complete Pipeline
    ##############################################################

    def run(self):


        print(

            """

==============================================================

AQAGC Stage 07

Results Generation Pipeline

==============================================================

"""

        )



        self.run_apdt()


        self.run_ranking()


        self.run_scalability()


        self.run_quantum_dynamics()


        self.run_ablation()


        self.run_hyperparameter()


        self.run_explainability()


        self.run_statistics()



        self.save_summary()



        print(

            """

==============================================================

Stage 07 Completed Successfully

All manuscript results generated.

==============================================================

"""

        )





if __name__ == "__main__":


    runner = Stage07Runner()


    runner.run()