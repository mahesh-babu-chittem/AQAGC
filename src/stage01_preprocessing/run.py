"""
==========================================================================
AQAGC
Stage 1 : Dataset Preprocessing

Run Preprocessing Pipeline
==========================================================================
"""

from pathlib import Path
import logging

from .dataset_registry import DatasetRegistry


# ======================================================================
# Logging
# ======================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ======================================================================
# Paths
# ======================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ======================================================================
# Main
# ======================================================================

def main():

    logger.info("=" * 80)
    logger.info("AQAGC STAGE 1 : DATASET PREPROCESSING")
    logger.info("=" * 80)

    registry = DatasetRegistry(
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
    )

    datasets = registry.get_all()

    summary = {}

    for name, dataset in datasets.items():

        logger.info(f"\nProcessing {name}")

        df = dataset.run()

        summary[name] = {

            "Rows": len(df),

            "Columns": len(df.columns),

        }

        logger.info(
            f"{name} Completed "
            f"({len(df):,} rows, {len(df.columns)} columns)"
        )

    logger.info("\n")

    logger.info("=" * 80)
    logger.info("PREPROCESSING SUMMARY")
    logger.info("=" * 80)

    for dataset, stats in summary.items():

        logger.info(
            f"{dataset:20s}"
            f"Rows : {stats['Rows']:,}    "
            f"Columns : {stats['Columns']}"
        )

    logger.info("=" * 80)
    logger.info("STAGE 1 COMPLETED SUCCESSFULLY")
    logger.info("=" * 80)


# ======================================================================

if __name__ == "__main__":

    main()