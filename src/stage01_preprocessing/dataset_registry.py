"""
==========================================================================
AQAGC
Stage 1 : Dataset Preprocessing

Dataset Registry
==========================================================================
"""

from pathlib import Path

from .cic_ids2017 import CICIDS2017
from .unsw_nb15 import UNSWNB15
from .cse_cic_ids2018 import CSECICIDS2018
from .ton_iot import ToNIoT


class DatasetRegistry:

    def __init__(
        self,
        raw_root: Path,
        processed_root: Path,
    ):

        self.datasets = {

            "CIC_IDS2017": CICIDS2017(
                raw_root,
                processed_root,
            ),

            "UNSW_NB15": UNSWNB15(
                raw_root,
                processed_root,
            ),

            "CSE_CIC_IDS2018": CSECICIDS2018(
                raw_root,
                processed_root,
            ),

            "ToN_IoT": ToNIoT(
                raw_root,
                processed_root,
            ),

        }

    ####################################################################
    # Return All Dataset Objects
    ####################################################################

    def get_all(self):

        return self.datasets

    ####################################################################
    # Return One Dataset
    ####################################################################

    def get(
        self,
        name: str,
    ):

        return self.datasets[name]