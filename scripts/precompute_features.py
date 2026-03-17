#!/usr/bin/env python3
r"""Offline script: pre-compute features and scaler parameters for production inference.

Reads the Kaggle Ecuador supermarket CSVs, replicates the MLForecast feature
engineering pipeline (lags, rolling means, calendar features, promotions,
holidays, store metadata), and writes two Parquet files:

1. ``precomputed_features.parquet`` -- one row per (store_nbr, family, date)
   with all model features pre-computed.
2. ``scaler_params.parquet`` -- one row per (store_nbr, family) with the
   LocalStandardScaler ``mean`` and ``std`` for inverse-transforming
   predictions.

Usage::

    python scripts/precompute_features.py \
        --data-dir data/ \
        --output-dir data/ \
        --buffer-days 90

Requirements (install with ``pip install -e ".[training]"``)::

    pandas, pyarrow, numpy
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def load_csvs(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the Kaggle CSV files."""
    logger.info("Loading CSVs from %s", data_dir)

    train = pd.read_csv(data_dir / "train.csv", parse_dates=["date"])
    holidays = pd.read_csv(data_dir / "holidays_events.csv", parse_dates=["date"])
    stores = pd.read_csv(data_dir / "stores.csv")
    oil = pd.read_csv(data_dir / "oil.csv", parse_dates=["date"])

    logger.info("train: %d rows, holidays: %d, stores: %d, oil: %d",
                len(train), len(holidays), len(stores), len(oil))
    return train, holidays, stores, oil


def compute_scaler_params(train: pd.DataFrame) -> pd.DataFrame:
    """Compute per-series (store_nbr, family) mean and std of target ``sales``.

    This replicates what ``LocalStandardScaler`` does during MLForecast fitting.
    """
    logger.info("Computing scaler parameters (LocalStandardScaler)...")
    stats = train.groupby(["store_nbr", "family"])["sales"].agg(["mean", "std"]).reset_index()
    # Replace NaN std (single-value series) with 1.0 to avoid division by zero
    stats["std"] = stats["std"].fillna(1.0).replace(0.0, 1.0)
    logger.info("Scaler params computed for %d series", len(stats))
    return stats


def build_features(
    train: pd.DataFrame,
    holidays: pd.DataFrame,
    stores: pd.DataFrame,
    oil: pd.DataFrame,
    scaler_params: pd.DataFrame,
    buffer_days: int,
) -> pd.DataFrame:
    """Build the full feature matrix.

    Features include:
    - Lag features: sales at t-1, t-7, t-14, t-28, t-90, t-365
    - Rolling means: 7-day, 28-day, 365-day windows on lagged sales
    - Calendar: day_of_week, month, day_of_month, is_weekend, week_of_year
    - Promotions: onpromotion flag
    - Oil price (forward-filled)
    - Store metadata: city, state, type, cluster (label-encoded)
    - Holiday indicator
    """
    logger.info("Building features (buffer_days=%d)...", buffer_days)

    df = train.copy()
    df = df.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)

    # --- Merge store metadata ---
    store_cat_cols = ["city", "state", "type"]
    for col in store_cat_cols:
        stores[f"store_{col}_enc"] = stores[col].astype("category").cat.codes
    store_features = stores[["store_nbr", "store_city_enc", "store_state_enc",
                             "store_type_enc", "cluster"]].copy()
    df = df.merge(store_features, on="store_nbr", how="left")

    # --- Oil price (forward-fill gaps) ---
    oil = oil.rename(columns={"dcoilwtico": "oil_price"}).dropna(subset=["oil_price"])
    oil = oil.sort_values("date")
    # Create a full date range and forward-fill
    full_dates = pd.DataFrame({"date": pd.date_range(oil["date"].min(), df["date"].max())})
    oil = full_dates.merge(oil, on="date", how="left")
    oil["oil_price"] = oil["oil_price"].ffill().bfill()
    df = df.merge(oil, on="date", how="left")
    df["oil_price"] = df["oil_price"].fillna(df["oil_price"].median())

    # --- Holiday indicator ---
    # Keep only national holidays and transferred holidays
    nat_holidays = holidays[
        (holidays["locale"] == "National") & (holidays["type"] != "Work Day")
    ][["date"]].drop_duplicates()
    nat_holidays["is_holiday"] = 1
    df = df.merge(nat_holidays, on="date", how="left")
    df["is_holiday"] = df["is_holiday"].fillna(0).astype(np.float32)

    # --- Calendar features ---
    df["day_of_week"] = df["date"].dt.dayofweek.astype(np.float32)
    df["month"] = df["date"].dt.month.astype(np.float32)
    df["day_of_month"] = df["date"].dt.day.astype(np.float32)
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(np.float32)
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(np.float32)

    # --- Scale target before computing lag/rolling features ---
    df = df.merge(scaler_params, on=["store_nbr", "family"], how="left")
    df["sales_scaled"] = (df["sales"] - df["mean"]) / df["std"]

    # --- Lag features (on scaled sales) ---
    lag_days = [1, 7, 14, 28, 90, 365]
    for lag in lag_days:
        df[f"lag_{lag}"] = df.groupby(["store_nbr", "family"])["sales_scaled"].shift(lag)

    # --- Rolling mean features (computed on lag_1 to avoid leakage) ---
    rolling_windows = [7, 28, 365]
    for window in rolling_windows:
        w = window  # capture loop variable for lambda closure

        def _rolling_mean(s: pd.Series[float], _w: int = w) -> pd.Series[float]:
            return s.rolling(_w, min_periods=1).mean()

        df[f"rolling_mean_{window}"] = (
            df.groupby(["store_nbr", "family"])["lag_1"].transform(_rolling_mean)
        )

    # --- Promotion ---
    df["onpromotion"] = df["onpromotion"].fillna(0).astype(np.float32)

    # --- Generate forecast buffer dates ---
    max_train_date = df["date"].max()
    if buffer_days > 0:
        logger.info("Generating %d-day forecast buffer beyond %s", buffer_days, max_train_date)
        buffer_dates = pd.date_range(
            max_train_date + pd.Timedelta(days=1),
            max_train_date + pd.Timedelta(days=buffer_days),
        )
        # For buffer dates, we extrapolate the last known feature values per series
        series_keys = df[["store_nbr", "family"]].drop_duplicates()
        buffer_rows = []
        for _, row in series_keys.iterrows():
            for bdate in buffer_dates:
                buffer_rows.append({
                    "store_nbr": row["store_nbr"],
                    "family": row["family"],
                    "date": bdate,
                })
        buffer_df = pd.DataFrame(buffer_rows)

        # Merge static features for buffer
        buffer_df = buffer_df.merge(store_features, on="store_nbr", how="left")
        buffer_df = buffer_df.merge(oil[["date", "oil_price"]], on="date", how="left")
        buffer_df["oil_price"] = buffer_df["oil_price"].fillna(df["oil_price"].iloc[-1])
        buffer_df = buffer_df.merge(nat_holidays, on="date", how="left")
        buffer_df["is_holiday"] = buffer_df["is_holiday"].fillna(0).astype(np.float32)

        # Calendar features for buffer
        buffer_df["day_of_week"] = buffer_df["date"].dt.dayofweek.astype(np.float32)
        buffer_df["month"] = buffer_df["date"].dt.month.astype(np.float32)
        buffer_df["day_of_month"] = buffer_df["date"].dt.day.astype(np.float32)
        buffer_df["is_weekend"] = (buffer_df["day_of_week"] >= 5).astype(np.float32)
        buffer_df["week_of_year"] = buffer_df["date"].dt.isocalendar().week.astype(np.float32)
        buffer_df["onpromotion"] = 0.0

        # For lag/rolling features on buffer dates, use the last available values
        buffer_df = buffer_df.merge(scaler_params, on=["store_nbr", "family"], how="left")
        buffer_df["sales_scaled"] = 0.0  # placeholder — model handles this

        for lag in lag_days:
            buffer_df[f"lag_{lag}"] = np.nan
        for window in rolling_windows:
            buffer_df[f"rolling_mean_{window}"] = np.nan

        # Concatenate and re-sort
        df = pd.concat([df, buffer_df], ignore_index=True)
        df = df.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)

        # Forward-fill lag/rolling features within each series for buffer dates
        lag_roll_cols = (
            [f"lag_{lag}" for lag in lag_days]
            + [f"rolling_mean_{win}" for win in rolling_windows]
        )
        df[lag_roll_cols] = df.groupby(["store_nbr", "family"])[lag_roll_cols].ffill()

    # --- Drop rows where lag features are NaN (warm-up period) ---
    # Keep rows from 2014 onwards (1 year warm-up for lag_365)
    min_feature_date = pd.Timestamp("2014-01-01")
    before = len(df)
    df = df[df["date"] >= min_feature_date].copy()
    logger.info("Dropped %d warm-up rows (before %s)", before - len(df), min_feature_date)

    # Fill any remaining NaN in lag/rolling with 0
    lag_roll_cols = (
        [f"lag_{lag}" for lag in lag_days]
        + [f"rolling_mean_{win}" for win in rolling_windows]
    )
    df[lag_roll_cols] = df[lag_roll_cols].fillna(0.0)

    # --- Select final feature columns ---
    feature_cols = [
        "day_of_week", "month", "day_of_month", "is_weekend", "week_of_year",
        "onpromotion", "oil_price", "is_holiday",
        "store_city_enc", "store_state_enc", "store_type_enc", "cluster",
    ] + [f"lag_{lag}" for lag in lag_days] + [f"rolling_mean_{win}" for win in rolling_windows]

    index_cols = ["store_nbr", "family", "date"]
    output_cols = index_cols + feature_cols

    result = df[output_cols].copy()

    # Cast feature columns to float32 for compact storage
    for col in feature_cols:
        result[col] = result[col].astype(np.float32)

    logger.info("Feature matrix: %d rows × %d columns", len(result), len(output_cols))
    return result


def main() -> None:
    """Run the pre-computation pipeline."""
    parser = argparse.ArgumentParser(description="Pre-compute features for production inference.")
    parser.add_argument("--data-dir", type=str, default="data/",
                        help="Directory containing Kaggle CSV files")
    parser.add_argument("--output-dir", type=str, default="data/",
                        help="Directory to write output Parquet files")
    parser.add_argument("--buffer-days", type=int, default=90,
                        help="Number of forecast buffer days beyond training data end")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train, holidays, stores, oil = load_csvs(data_dir)

    scaler_params = compute_scaler_params(train)

    features = build_features(train, holidays, stores, oil, scaler_params, args.buffer_days)

    # Write outputs
    features_path = output_dir / "precomputed_features.parquet"
    scaler_path = output_dir / "scaler_params.parquet"

    logger.info("Writing features to %s", features_path)
    features.to_parquet(features_path, index=False, engine="pyarrow")

    logger.info("Writing scaler params to %s", scaler_path)
    scaler_params.to_parquet(scaler_path, index=False, engine="pyarrow")

    logger.info("Done! Features: %s (%.1f MB), Scalers: %s",
                features_path,
                features_path.stat().st_size / 1024 / 1024,
                scaler_path)


if __name__ == "__main__":
    main()
