"""
==========================================================================
AQAGC

Stage 1 Utility Functions
==========================================================================
"""

from pathlib import Path

import pandas as pd


def merge_csv_files(
    folder: Path,
):

    csv_files = sorted(folder.glob("*.csv"))

    frames = []

    for csv in csv_files:

        print(f"Loading {csv.name}")

        df = pd.read_csv(
            csv,
            low_memory=False,
        )

        df["__source_file__"] = csv.name

        frames.append(df)

    return pd.concat(
        frames,
        ignore_index=True,
    )


def remove_empty_rows(
    df: pd.DataFrame,
):

    return df.dropna(
        how="all"
    )


def lowercase_labels(
    df: pd.DataFrame,
):

    if "Label" not in df.columns:
        return df

    df["Label"] = (
        df["Label"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return df