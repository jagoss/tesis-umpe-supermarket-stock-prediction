"""Tests for ParquetDataRepository."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from server.infrastructure.data import ParquetDataRepository


@pytest.fixture()
def tmp_parquet_files(tmp_path: Path) -> tuple[str, str]:
    """Create small fixture Parquet files and return their paths."""
    # Features Parquet: 2 stores × 2 families × 3 dates = 12 rows, 3 features each
    rows = []
    for store in [1, 2]:
        for family in ["BEVERAGES", "BREAD"]:
            for d in [date(2017, 8, 1), date(2017, 8, 2), date(2017, 8, 3)]:
                rows.append(
                    {
                        "store_nbr": store,
                        "family": family,
                        "date": pd.Timestamp(d),
                        "lag_1": float(store) + 0.1,
                        "lag_7": float(store) + 0.7,
                        "day_of_week": float(d.weekday()),
                    }
                )

    features_df = pd.DataFrame(rows)
    features_path = tmp_path / "features.parquet"
    features_df.to_parquet(features_path, index=False)

    # Scaler Parquet
    scaler_df = pd.DataFrame(
        [
            {"store_nbr": 1, "family": "BEVERAGES", "mean": 100.0, "std": 20.0},
            {"store_nbr": 1, "family": "BREAD", "mean": 50.0, "std": 10.0},
            {"store_nbr": 2, "family": "BEVERAGES", "mean": 200.0, "std": 40.0},
            {"store_nbr": 2, "family": "BREAD", "mean": 80.0, "std": 15.0},
        ]
    )
    scaler_path = tmp_path / "scaler.parquet"
    scaler_df.to_parquet(scaler_path, index=False)

    return str(features_path), str(scaler_path)


class TestParquetDataRepository:
    def test_load_and_feature_names(self, tmp_parquet_files: tuple[str, str]) -> None:
        repo = ParquetDataRepository(*tmp_parquet_files)
        names = repo.get_feature_names()
        assert names == ["lag_1", "lag_7", "day_of_week"]

    def test_get_feature_vector_found(self, tmp_parquet_files: tuple[str, str]) -> None:
        repo = ParquetDataRepository(*tmp_parquet_files)
        vec = repo.get_feature_vector("1", "BEVERAGES", date(2017, 8, 1))
        assert vec is not None
        assert len(vec) == 3
        assert vec[0] == pytest.approx(1.1)  # lag_1 = float(store=1) + 0.1

    def test_get_feature_vector_not_found(self, tmp_parquet_files: tuple[str, str]) -> None:
        repo = ParquetDataRepository(*tmp_parquet_files)
        assert repo.get_feature_vector("1", "BEVERAGES", date(2099, 1, 1)) is None
        assert repo.get_feature_vector("999", "BEVERAGES", date(2017, 8, 1)) is None

    def test_get_scaler_params_found(self, tmp_parquet_files: tuple[str, str]) -> None:
        repo = ParquetDataRepository(*tmp_parquet_files)
        params = repo.get_scaler_params("1", "BEVERAGES")
        assert params == (100.0, 20.0)

    def test_get_scaler_params_not_found(self, tmp_parquet_files: tuple[str, str]) -> None:
        repo = ParquetDataRepository(*tmp_parquet_files)
        assert repo.get_scaler_params("999", "BEVERAGES") is None

    def test_get_available_date_range(self, tmp_parquet_files: tuple[str, str]) -> None:
        repo = ParquetDataRepository(*tmp_parquet_files)
        min_d, max_d = repo.get_available_date_range()
        assert min_d == date(2017, 8, 1)
        assert max_d == date(2017, 8, 3)

    def test_missing_features_file_raises(self, tmp_path: Path) -> None:
        scaler_path = tmp_path / "scaler.parquet"
        pd.DataFrame({"store_nbr": [1], "family": ["X"], "mean": [0.0], "std": [1.0]}).to_parquet(
            scaler_path, index=False
        )
        with pytest.raises(FileNotFoundError, match="Features Parquet"):
            ParquetDataRepository(str(tmp_path / "nonexistent.parquet"), str(scaler_path))

    def test_missing_scaler_file_raises(self, tmp_path: Path) -> None:
        features_path = tmp_path / "features.parquet"
        pd.DataFrame(
            {"store_nbr": [1], "family": ["X"], "date": [pd.Timestamp("2017-01-01")], "f1": [0.0]}
        ).to_parquet(features_path, index=False)
        with pytest.raises(FileNotFoundError, match="Scaler Parquet"):
            ParquetDataRepository(str(features_path), str(tmp_path / "nonexistent.parquet"))
