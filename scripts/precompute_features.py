#!/usr/bin/env python3
r"""Offline script: pre-compute features and scaler parameters for production inference.

Reads the Kaggle Ecuador supermarket CSVs, replicates the MLForecast feature
engineering pipeline used to train ``models/lightgbm_model.onnx``, and writes
two Parquet files:

1. ``precomputed_features.parquet`` -- one row per (store_nbr, family, date)
   with all 30 model features pre-computed, in the exact column order the
   ONNX model expects.
2. ``scaler_params.parquet`` -- one row per (store_nbr, family) with the
   LocalStandardScaler ``mean`` and ``std`` for inverse-transforming
   predictions.

Feature order (matches ``lgb_model.feature_name_`` from training notebook):
    0  onpromotion
    1  family_enc                          (pd.factorize encoding of family)
    2  store_nbr_feat                      (store number as float)
    3  description_Cantonizacion_de_Salinas
    4  description_Navidad
    5  description_Navidad_1               (sanitised from "Navidad-1")
    6  description_Navidad_2
    7  description_Navidad_3
    8  description_Navidad_4
    9  description_Primer_dia_del_ano
   10  description_Terremoto_Manabi_1      (sanitised from "Terremoto Manabi+1")
   11  description_Terremoto_Manabi_15
   12  description_Terremoto_Manabi_2
   13  description_Traslado_Primer_dia_del_ano
   14  lag1
   15  lag7
   16  lag14
   17  lag28
   18  lag90
   19  lag365
   20  expanding_mean_lag1
   21  rolling_mean_lag7_window_size7
   22  rolling_mean_lag7_window_size28
   23  rolling_mean_lag7_window_size365
   24  rolling_mean_lag28_window_size7
   25  rolling_mean_lag28_window_size28
   26  rolling_mean_lag28_window_size365
   27  day_of_week
   28  is_month_end
   29  is_month_start

Note: ``family_enc`` and ``store_nbr_feat`` are renamed to avoid conflicts
with the index columns (``family``, ``store_nbr``) that ``ParquetDataRepository``
excludes from feature vectors.  Column names containing ``-`` or ``+`` are
sanitised to ``_`` so that ``itertuples`` / ``getattr`` work correctly.

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

# ---------------------------------------------------------------------------
# Selected holidays (determined by correlation analysis in training notebook).
# Keys are the exact ``description`` strings in holidays_events.csv (after
# punctuation cleaning); values are the sanitised parquet column names.
# ---------------------------------------------------------------------------
_SELECTED_HOLIDAYS: dict[str, str] = {
    "Cantonizacion de Salinas": "description_Cantonizacion_de_Salinas",
    "Navidad": "description_Navidad",
    "Navidad-1": "description_Navidad_1",
    "Navidad-2": "description_Navidad_2",
    "Navidad-3": "description_Navidad_3",
    "Navidad-4": "description_Navidad_4",
    "Primer dia del ano": "description_Primer_dia_del_ano",
    "Terremoto Manabi+1": "description_Terremoto_Manabi_1",
    "Terremoto Manabi+15": "description_Terremoto_Manabi_15",
    "Terremoto Manabi+2": "description_Terremoto_Manabi_2",
    "Traslado Primer dia del ano": "description_Traslado_Primer_dia_del_ano",
}

# Final feature column order (must match lgb_model.feature_name_ from training)
_FEATURE_COLS: list[str] = (
    [
        "onpromotion",
        "family_enc",
        "store_nbr_feat",
    ]
    + list(_SELECTED_HOLIDAYS.values())
    + [
        "lag1",
        "lag7",
        "lag14",
        "lag28",
        "lag90",
        "lag365",
        "expanding_mean_lag1",
        "rolling_mean_lag7_window_size7",
        "rolling_mean_lag7_window_size28",
        "rolling_mean_lag7_window_size365",
        "rolling_mean_lag28_window_size7",
        "rolling_mean_lag28_window_size28",
        "rolling_mean_lag28_window_size365",
        "day_of_week",
        "is_month_end",
        "is_month_start",
    ]
)

_LAG_DAYS = [1, 7, 14, 28, 90, 365]
_LAG_TRANSFORM_BASES = [7, 28]
_ROLLING_WINDOWS = [7, 28, 365]
_INDEX_COLS = ["store_nbr", "family", "date"]


def load_csvs(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load train and holidays CSVs."""
    logger.info("Loading CSVs from %s", data_dir)
    train = pd.read_csv(data_dir / "train.csv", parse_dates=["date"])
    holidays = pd.read_csv(data_dir / "holidays_events.csv", parse_dates=["date"])
    logger.info("train: %d rows, holidays: %d rows", len(train), len(holidays))
    return train, holidays


def compute_family_encoding(train: pd.DataFrame) -> dict[str, int]:
    """Replicate the pd.factorize encoding applied during training.

    The training notebook calls ``pd.factorize(df['family'])`` on the raw
    training DataFrame (in original CSV row order, before any sorting).  We
    replicate that here to produce the same integer codes the ONNX model was
    trained with.

    Returns
    -------
    dict mapping family name → integer code

    """
    labels, uniques = pd.factorize(train["family"])
    factors: dict[str, int] = dict(zip(uniques.tolist(), labels.tolist(), strict=False))
    logger.info("Family encoding: %d unique families", len(factors))
    return factors


def compute_scaler_params(train: pd.DataFrame) -> pd.DataFrame:
    """Compute per-series (store_nbr, family) mean and std for LocalStandardScaler.

    Replicates the training pipeline: sales are clipped to ≥0 and zeros are
    replaced with 0.01 before computing statistics (matching ``clean_sales_data``
    in the notebook).
    """
    logger.info("Computing scaler parameters...")
    df = train[["store_nbr", "family", "sales"]].copy()
    df["sales"] = df["sales"].clip(lower=0).replace(0, 0.01)
    stats = df.groupby(["store_nbr", "family"])["sales"].agg(["mean", "std"]).reset_index()
    stats["std"] = stats["std"].fillna(1.0).replace(0.0, 1.0)
    logger.info("Scaler params computed for %d series", len(stats))
    return stats


def _build_holiday_date_sets(holidays: pd.DataFrame) -> dict[str, set[pd.Timestamp]]:
    """Build a mapping from parquet column name → set of dates that are that holiday."""
    # Replicate notebook punctuation cleaning
    hols = holidays.copy()
    hols["description"] = hols["description"].str.replace(r'[.!?,:;"]', "", regex=True)

    result: dict[str, set[pd.Timestamp]] = {}
    for raw_desc, col_name in _SELECTED_HOLIDAYS.items():
        mask = (hols["description"] == raw_desc) & (~hols["transferred"].astype(bool))
        result[col_name] = set(hols.loc[mask, "date"].dt.normalize())
    return result


def _add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add day_of_week, is_month_end, is_month_start from the date column."""
    df["day_of_week"] = df["date"].dt.dayofweek.astype(np.float32)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(np.float32)
    df["is_month_start"] = df["date"].dt.is_month_start.astype(np.float32)
    return df


def _add_holiday_features(
    df: pd.DataFrame, holiday_dates: dict[str, set[pd.Timestamp]]
) -> pd.DataFrame:
    """Add one-hot holiday indicator columns."""
    for col_name, dates in holiday_dates.items():
        df[col_name] = df["date"].isin(dates).astype(np.float32)
    return df


def build_features(
    train: pd.DataFrame,
    holidays: pd.DataFrame,
    scaler_params: pd.DataFrame,
    family_factors: dict[str, int],
    buffer_days: int,
) -> pd.DataFrame:
    """Build the full 30-feature matrix matching the ONNX model's expected input.

    Parameters
    ----------
    train:
        Raw training DataFrame from train.csv.
    holidays:
        Raw holidays DataFrame from holidays_events.csv.
    scaler_params:
        Per-series mean/std from ``compute_scaler_params``.
    family_factors:
        Family → integer code mapping from ``compute_family_encoding``.
    buffer_days:
        Number of forecast days to generate beyond the training end date.

    """
    logger.info("Building features (buffer_days=%d)...", buffer_days)

    # --- Prepare base training data (match notebook's clean_sales_data) ---
    df = train[["store_nbr", "family", "date", "onpromotion", "sales"]].copy()
    df["sales"] = df["sales"].clip(lower=0).replace(0, 0.01)
    df = df.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)

    # --- Merge scaler params and scale sales ---
    df = df.merge(scaler_params, on=["store_nbr", "family"], how="left")
    df["sales_scaled"] = (df["sales"] - df["mean"]) / df["std"]

    # --- Family encoding and store_nbr as features ---
    df["family_enc"] = df["family"].map(family_factors).fillna(-1).astype(np.float32)
    df["store_nbr_feat"] = df["store_nbr"].astype(np.float32)

    # --- Onpromotion ---
    df["onpromotion"] = df["onpromotion"].fillna(0).astype(np.float32)

    # --- Lag features on scaled sales ---
    for lag in _LAG_DAYS:
        df[f"lag{lag}"] = (
            df.groupby(["store_nbr", "family"])["sales_scaled"].shift(lag).astype(np.float32)
        )

    # --- Lag transforms ---
    # expanding_mean_lag1: expanding mean of the lag1 series
    df["expanding_mean_lag1"] = (
        df.groupby(["store_nbr", "family"])["lag1"]
        .transform(lambda x: x.expanding().mean())
        .astype(np.float32)
    )

    # rolling_mean_lag{base}_window_size{w}: rolling mean of lag{base} series
    for base in _LAG_TRANSFORM_BASES:
        lag_col = f"lag{base}"
        for window in _ROLLING_WINDOWS:
            col_name = f"rolling_mean_lag{base}_window_size{window}"
            df[col_name] = (
                df.groupby(["store_nbr", "family"])[lag_col]
                .transform(lambda x, w=window: x.rolling(w, min_periods=1).mean())
                .astype(np.float32)
            )

    # --- Calendar features ---
    df = _add_calendar_features(df)

    # --- Holiday indicator features ---
    holiday_dates = _build_holiday_date_sets(holidays)
    df = _add_holiday_features(df, holiday_dates)

    # --- Generate forecast buffer dates ---
    if buffer_days > 0:
        max_train_date = df["date"].max()
        logger.info("Generating %d-day forecast buffer beyond %s", buffer_days, max_train_date)
        buffer_dates = pd.date_range(
            max_train_date + pd.Timedelta(days=1),
            max_train_date + pd.Timedelta(days=buffer_days),
        )
        series_keys = df[
            ["store_nbr", "family", "family_enc", "store_nbr_feat", "mean", "std"]
        ].drop_duplicates(["store_nbr", "family"])
        buffer_rows = []
        for _, row in series_keys.iterrows():
            for bdate in buffer_dates:
                buffer_rows.append(
                    {
                        "store_nbr": row["store_nbr"],
                        "family": row["family"],
                        "date": bdate,
                        "onpromotion": 0.0,
                        "family_enc": row["family_enc"],
                        "store_nbr_feat": row["store_nbr_feat"],
                        "mean": row["mean"],
                        "std": row["std"],
                        "sales": np.nan,
                        "sales_scaled": np.nan,
                    }
                )
        buffer_df = pd.DataFrame(buffer_rows)

        # Add NaN placeholders for lag/rolling cols (will be forward-filled)
        lag_roll_cols = (
            [f"lag{lag}" for lag in _LAG_DAYS]
            + ["expanding_mean_lag1"]
            + [
                f"rolling_mean_lag{base}_window_size{w}"
                for base in _LAG_TRANSFORM_BASES
                for w in _ROLLING_WINDOWS
            ]
        )
        for col in lag_roll_cols:
            buffer_df[col] = np.nan

        # Calendar and holiday features for buffer dates
        buffer_df = _add_calendar_features(buffer_df)
        buffer_df = _add_holiday_features(buffer_df, holiday_dates)

        df = pd.concat([df, buffer_df], ignore_index=True)
        df = df.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)

        # Forward-fill lag/rolling features within each series
        df[lag_roll_cols] = df.groupby(["store_nbr", "family"])[lag_roll_cols].ffill()

    # --- Drop warm-up period (need 365-day history) ---
    min_feature_date = pd.Timestamp("2014-01-01")
    before = len(df)
    df = df[df["date"] >= min_feature_date].copy()
    logger.info("Dropped %d warm-up rows (before %s)", before - len(df), min_feature_date)

    # --- Fill any remaining NaN (e.g. early lags) with 0 ---
    lag_roll_cols = (
        [f"lag{lag}" for lag in _LAG_DAYS]
        + ["expanding_mean_lag1"]
        + [
            f"rolling_mean_lag{base}_window_size{w}"
            for base in _LAG_TRANSFORM_BASES
            for w in _ROLLING_WINDOWS
        ]
    )
    df[lag_roll_cols] = df[lag_roll_cols].fillna(0.0)

    # --- Select and order final columns ---
    result = df[_INDEX_COLS + _FEATURE_COLS].copy()

    # Ensure float32 for all feature columns
    for col in _FEATURE_COLS:
        result[col] = result[col].astype(np.float32)

    logger.info(
        "Feature matrix: %d rows × %d feature columns (+ %d index columns)",
        len(result),
        len(_FEATURE_COLS),
        len(_INDEX_COLS),
    )
    return result


def main() -> None:
    """Run the pre-computation pipeline."""
    parser = argparse.ArgumentParser(description="Pre-compute features for production inference.")
    parser.add_argument(
        "--data-dir", type=str, default="data/", help="Directory containing Kaggle CSV files"
    )
    parser.add_argument(
        "--output-dir", type=str, default="data/", help="Directory to write output Parquet files"
    )
    parser.add_argument(
        "--buffer-days",
        type=int,
        default=90,
        help="Number of forecast buffer days beyond training data end",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train, holidays = load_csvs(data_dir)

    family_factors = compute_family_encoding(train)
    scaler_params = compute_scaler_params(train)
    features = build_features(train, holidays, scaler_params, family_factors, args.buffer_days)

    features_path = output_dir / "precomputed_features.parquet"
    scaler_path = output_dir / "scaler_params.parquet"

    logger.info("Writing features to %s", features_path)
    features.to_parquet(features_path, index=False, engine="pyarrow")

    logger.info("Writing scaler params to %s", scaler_path)
    scaler_params.to_parquet(scaler_path, index=False, engine="pyarrow")

    logger.info(
        "Done! Features: %s (%.1f MB), Scalers: %s",
        features_path,
        features_path.stat().st_size / 1024 / 1024,
        scaler_path,
    )


if __name__ == "__main__":
    main()
