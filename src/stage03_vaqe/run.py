"""
==============================================================
AQAGC

Stage 03

Vulnerability-Aware Quantum Encoding (VAQE)

Entry Point

==============================================================
"""

import traceback

from pipeline import VAQEPipeline


def main():

    print("\n")
    print("=" * 80)
    print("AQAGC")
    print("Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)")
    print("=" * 80)

    try:

        pipeline = VAQEPipeline()

        outputs = pipeline.run()

        print("\n")
        print("=" * 80)
        print("Stage 03 Completed Successfully")
        print("=" * 80)

        print(
            f"Encoded State Shape : {outputs['encoded_state'].shape}"
        )

        print(
            f"Hamiltonian Shape   : {outputs['hamiltonian'].shape}"
        )

        print(
            f"Encoded Nodes       : {len(outputs['node_scores'])}"
        )

        print("=" * 80)

    except KeyboardInterrupt:

        print("\nExecution Interrupted.")

    except Exception:

        print("\nStage 03 Failed.\n")

        traceback.print_exc()


if __name__ == "__main__":

    main()