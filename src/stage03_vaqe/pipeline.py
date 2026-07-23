"""
==============================================================
AQAGC

Stage 03 : Vulnerability-Aware Quantum Encoding (VAQE)

Complete Pipeline

==============================================================
"""

from feature_encoder import FeatureEncoder
from quantum_encoder import QuantumEncoder
from graph_hamiltonian import GraphHamiltonian
from node_encoding import NodeEncoder

from io_utils import (
    load_attack_graph,
    load_nodes,
    load_edges,
    load_metadata,
    save_metadata,
)


class VAQEPipeline:

    def __init__(self):

        self.graph = None
        self.nodes = None
        self.edges = None
        self.metadata = None

        self.encoded_state = None
        self.hamiltonian = None
        self.node_scores = None

    # ----------------------------------------------------------

    def load_inputs(self):

        self.graph = load_attack_graph()

        self.nodes = load_nodes()

        self.edges = load_edges()

        self.metadata = load_metadata()

    # ----------------------------------------------------------

    def run_quantum_encoding(self):

        encoder = QuantumEncoder(

            self.nodes

        )

        self.encoded_state = encoder.run()

    # ----------------------------------------------------------

    def run_hamiltonian(self):

        builder = GraphHamiltonian(

            self.graph

        )

        self.hamiltonian = builder.run()

    # ----------------------------------------------------------

    def run_node_encoding(self):

        encoder = NodeEncoder(

            self.graph,

            self.nodes

        )

        self.node_scores = encoder.run()

    # ----------------------------------------------------------

    def export_metadata(self):

        metadata = {

            "Stage": "Stage03",

            "Module": "VAQE",

            "Nodes": self.graph.number_of_nodes(),

            "Edges": self.graph.number_of_edges(),

            "HamiltonianShape": list(

                self.hamiltonian.shape

            ),

            "DensityMatrixShape": list(

                self.encoded_state.shape

            ),

            "Status": "Completed"

        }

        save_metadata(

            metadata

        )

    # ----------------------------------------------------------

    def run(self):

        self.load_inputs()

        self.run_quantum_encoding()

        self.run_hamiltonian()

        self.run_node_encoding()

        self.export_metadata()

        return {

            "encoded_state": self.encoded_state,

            "hamiltonian": self.hamiltonian,

            "node_scores": self.node_scores

        }