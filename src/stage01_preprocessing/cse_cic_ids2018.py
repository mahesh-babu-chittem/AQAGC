"""
==========================================================================
AQAGC
Stage 1 : Dataset Preprocessing

CSE-CIC-IDS2018 Dataset
==========================================================================
"""

from pathlib import Path

import pandas as pd

from .base_dataset import BaseDataset
from .preprocessing_utils import (
    merge_csv_files,
    lowercase_labels,
)


class CSECICIDS2018(BaseDataset):

    def __init__(
        self,
        raw_root: Path,
        processed_root: Path,
    ):

        super().__init__(
            raw_root,
            processed_root,
        )

        self.dataset_dir = self.raw_root / "CSE-CIC-IDS2018"

    ####################################################################
    # Load
    ####################################################################

    def load(self) -> pd.DataFrame:

        print("\nLoading CSE-CIC-IDS2018 ...")

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

        #
        # Remove completely empty rows
        #

        df = df.dropna(
            how="all"
        )

        #
        # Remove repeated header rows
        #

        if "Label" in df.columns:

            df = df[
                df["Label"].astype(str).str.lower() != "label"
            ]

        #
        # Standardize labels
        #

        df = lowercase_labels(df)

        #
        # Remove leading/trailing spaces
        #

        df.columns = [
            c.strip()
            for c in df.columns
        ]

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
            "CSE_CIC_IDS2018_processed.csv"
        )

        df.to_csv(
            output,
            index=False,
        )

        print(f"Saved : {output}")