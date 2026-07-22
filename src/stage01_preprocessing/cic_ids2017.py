"""
==========================================================================
AQAGC
Stage 1 : Dataset Preprocessing

CIC-IDS2017 Dataset
==========================================================================
"""

from pathlib import Path

import pandas as pd

from .base_dataset import BaseDataset
from .preprocessing_utils import (
    merge_csv_files,
    remove_empty_rows,
    lowercase_labels,
)


class CICIDS2017(BaseDataset):

    def __init__(
        self,
        raw_root: Path,
        processed_root: Path,
    ):

        super().__init__(
            raw_root,
            processed_root,
        )

        self.dataset_dir = self.raw_root / "CIC_IDS2017"

    ####################################################################
    # Load
    ####################################################################

    def load(self) -> pd.DataFrame:

        print("\nLoading CIC-IDS2017 ...")

        df = merge_csv_files(
            self.dataset_dir
        )

        print(f"Loaded Shape : {df.shape}")

        return df

    ####################################################################
    # Preprocess
    ####################################################################

    def preprocess(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        print("Cleaning dataset...")

        df = remove_empty_rows(df)

        df = lowercase_labels(df)

        #
        # NOTE
        # ----
        # Duplicate removal is intentionally NOT performed.
        # The benchmark generation stage will determine
        # whether duplicate flows should be retained.
        #

        print(f"Processed Shape : {df.shape}")

        return df

    ####################################################################
    # Save
    ####################################################################

    def save(
        self,
        df: pd.DataFrame,
    ):

        output = (
            self.processed_root /
            "CIC_IDS2017_processed.csv"
        )

        df.to_csv(
            output,
            index=False,
        )

        print(f"Saved : {output}")