"""
==========================================================================
AQAGC
Stage 1 : Dataset Preprocessing

UNSW-NB15 Dataset
==========================================================================
"""

from pathlib import Path

import pandas as pd

from .base_dataset import BaseDataset
from .preprocessing_utils import (
    lowercase_labels,
)


class UNSWNB15(BaseDataset):

    def __init__(
        self,
        raw_root: Path,
        processed_root: Path,
    ):

        super().__init__(
            raw_root,
            processed_root,
        )

        self.dataset_dir = self.raw_root / "UNSW-NB15"

    ####################################################################
    # Load
    ####################################################################

    def load(self) -> pd.DataFrame:

        print("\nLoading UNSW-NB15 ...")

        csv_files = sorted(
            [
                f
                for f in self.dataset_dir.glob("*.csv")
                if (
                    "features" not in f.name.lower()
                    and
                    "gt" not in f.name.lower()
                )
            ]
        )

        if len(csv_files) == 0:

            raise FileNotFoundError(
                "No UNSW-NB15 data files found."
            )

        frames = []

        for csv in csv_files:

            print(f"Loading {csv.name}")

            #
            # UNSW-NB15 data files do not contain
            # consistent headers.
            #

            df = pd.read_csv(
                csv,
                header=None,
                low_memory=False,
            )

            df["__source_file__"] = csv.name

            frames.append(df)

        df = pd.concat(
            frames,
            ignore_index=True,
        )

        #
        # Load official feature names
        #

        feature_file = self.dataset_dir / "UNSW-NB15_features.csv"

        if feature_file.exists():

            features = pd.read_csv(
                feature_file
            )

            column_names = list(
                features.iloc[:, 1]
            )

            column_names.append(
                "__source_file__"
            )

            if len(column_names) == len(df.columns):

                df.columns = column_names

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
        # Standardize label column
        #

        if "label" in df.columns:

            df.rename(
                columns={
                    "label": "Label"
                },
                inplace=True,
            )

        df = lowercase_labels(df)

        #
        # Keep original feature values.
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
            "UNSW_NB15_processed.csv"
        )

        df.to_csv(
            output,
            index=False,
        )

        print(f"Saved : {output}")