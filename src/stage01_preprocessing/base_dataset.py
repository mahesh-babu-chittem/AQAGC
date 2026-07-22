"""
==========================================================================
AQAGC
Stage 1 : Dataset Preprocessing

Base Dataset Class
==========================================================================

Every cybersecurity dataset preprocessor must inherit from this class.
"""

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class BaseDataset(ABC):

    def __init__(self,
                 raw_root: Path,
                 processed_root: Path):

        self.raw_root = Path(raw_root)
        self.processed_root = Path(processed_root)

        self.processed_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @abstractmethod
    def load(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def preprocess(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    def save(
        self,
        df: pd.DataFrame,
    ):
        pass

    def run(self):

        df = self.load()

        df = self.preprocess(df)

        self.save(df)

        return df