"""Parquet-backed data repository for pre-computed features.

Loads a Parquet file of pre-computed features and a separate scaler-params
Parquet at initialisation, then serves O(1) lookups by
``(store_nbr, family, date)`` via an in-memory dictionary index.
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import cast

import pandas as pd

from server.application import DataRepositoryPort

logger = logging.getLogger(__name__)


class ParquetDataRepository(DataRepositoryPort):
    """Read-only repository backed by pre-computed Parquet files.

    Parameters
    ----------
    features_path:
        Path to the Parquet file containing pre-computed feature rows.
        Expected columns: ``store_nbr``, ``family``, ``date``, plus one column
        per feature.
    scaler_path:
        Path to the Parquet file containing ``(store_nbr, family, mean, std)``
        rows for inverse-scaling predictions.

    """

    # Columns that are used for indexing and must not appear in feature vectors
    _INDEX_COLS = ("store_nbr", "family", "date")

    def __init__(self, features_path: str, scaler_path: str) -> None:
        """Load Parquet files and build in-memory indexes."""
        features_path_obj = Path(features_path)
        scaler_path_obj = Path(scaler_path)

        if not features_path_obj.exists():
            raise FileNotFoundError(f"Features Parquet not found: {features_path_obj}")
        if not scaler_path_obj.exists():
            raise FileNotFoundError(f"Scaler Parquet not found: {scaler_path_obj}")

        logger.info("Loading features from %s", features_path_obj)
        features_df = pd.read_parquet(features_path_obj)

        logger.info("Loading scaler params from %s", scaler_path_obj)
        scaler_df = pd.read_parquet(scaler_path_obj)

        # Validate required columns
        for col in self._INDEX_COLS:
            if col not in features_df.columns:
                raise ValueError(f"Features Parquet missing required column: {col}")
        for col in ("store_nbr", "family", "mean", "std"):
            if col not in scaler_df.columns:
                raise ValueError(f"Scaler Parquet missing required column: {col}")

        # Normalise date column to datetime.date
        features_df["date"] = pd.to_datetime(features_df["date"]).dt.date

        # Build feature-name list (all columns except index columns)
        self._feature_names: list[str] = [
            c for c in features_df.columns if c not in self._INDEX_COLS
        ]

        # Build feature lookup: (store_nbr_str, family, date) -> list[float]
        self._features: dict[tuple[str, str, date], list[float]] = {}
        feature_cols = self._feature_names
        for row in features_df.itertuples(index=False):
            feat_key = (str(row.store_nbr), str(row.family), cast(date, row.date))
            self._features[feat_key] = [float(getattr(row, c)) for c in feature_cols]

        # Build scaler lookup: (store_nbr_str, family) -> (mean, std)
        self._scalers: dict[tuple[str, str], tuple[float, float]] = {}
        for row in scaler_df.itertuples(index=False):
            scaler_key = (str(row.store_nbr), str(row.family))
            self._scalers[scaler_key] = (float(cast(float, row.mean)), float(cast(float, row.std)))

        # Date range
        all_dates = features_df["date"].unique()
        self._min_date: date = min(all_dates)
        self._max_date: date = max(all_dates)

        logger.info(
            "ParquetDataRepository ready: %d feature rows, %d scaler entries, "
            "date range %s to %s, %d features",
            len(self._features),
            len(self._scalers),
            self._min_date,
            self._max_date,
            len(self._feature_names),
        )

    # -- DataRepositoryPort interface ----------------------------------------

    def get_feature_vector(
        self, store_id: str, product_id: str, target_date: date
    ) -> list[float] | None:
        """Return the pre-computed feature vector, or ``None`` if not found."""
        return self._features.get((store_id, product_id, target_date))

    def get_feature_names(self) -> list[str]:
        """Return ordered feature column names."""
        return list(self._feature_names)

    def get_scaler_params(self, store_id: str, product_id: str) -> tuple[float, float] | None:
        """Return ``(mean, std)`` for the series, or ``None``."""
        return self._scalers.get((store_id, product_id))

    def get_available_date_range(self) -> tuple[date, date]:
        """Return ``(min_date, max_date)`` in the dataset."""
        return (self._min_date, self._max_date)
