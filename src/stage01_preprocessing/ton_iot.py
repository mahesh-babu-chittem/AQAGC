"""
==========================================================================
AQAGC
Stage 1 : Dataset Preprocessing

ToN-IoT Dataset
==========================================================================
"""

from pathlib import Path

import pandas as pd

from .base_dataset import BaseDataset
from .preprocessing_utils import (
    merge_csv_files,
)


class ToNIoT(BaseDataset):

    def __init__(
        self,
        raw_root: Path,
        processed_root: Path,
    ):

        super().__init__(
            raw_root,
            processed_root,
        )

        self.dataset_dir = self.raw_root / "ToN-IoT"

    ####################################################################
    # Load
    ####################################################################

    def load(self) -> pd.DataFrame:

        print("\nLoading ToN-IoT ...")

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
        # Remove duplicated header rows
        #

        if "Label" in df.columns:

            df = df[
                df["Label"].astype(str).str.lower() != "label"
            ]

        #
        # Standardize binary labels
        #

        if "Label" in df.columns:

            df["Label"] = (
                df["Label"]
                .astype(str)
                .str.strip()
            )

            df["Label"] = df["Label"].replace(
                {
                    "0": "benign",
                    "1": "attack",
                }
            )

        #
        # Remove whitespace from column names
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
            "ToN_IoT_processed.csv"
        )

        df.to_csv(
            output,
            index=False,
        )

        print(f"Saved : {output}")