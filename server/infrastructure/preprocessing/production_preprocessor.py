"""Production preprocessor that looks up pre-computed features from a data repository.

For each date in the requested range, this preprocessor retrieves the feature
vector from a ``DataRepositoryPort`` implementation and assembles them into
a feature matrix suitable for the ONNX model.
"""

from __future__ import annotations

from datetime import timedelta

from server.application import DataRepositoryPort, PredictStockInput, PreprocessedData
from server.domain import DataNotFoundError


class ProductionPreprocessor:
    """Assembles pre-computed feature matrices from a ``DataRepositoryPort``."""

    def __init__(self, data_repo: DataRepositoryPort) -> None:
        """Initialise with a data repository for feature lookups."""
        self._data_repo = data_repo

    def preprocess(self, data: PredictStockInput) -> PreprocessedData:
        """Look up features for every date in the requested range.

        Args:
            data: Application-level input DTO.

        Returns:
            ``PreprocessedData`` with the ``features`` matrix populated.

        Raises:
            DataNotFoundError: If any date in the range has no pre-computed features.

        """
        horizon = (data.end_date - data.start_date).days + 1
        horizon = max(0, horizon)

        min_date, max_date = self._data_repo.get_available_date_range()

        features: list[list[float]] = []
        for step in range(horizon):
            target_date = data.start_date + timedelta(days=step)
            # Clamp to the available range: dates beyond max_date reuse the last
            # pre-computed row (lag features are forward-filled, so this is the
            # best available approximation for future dates).
            lookup_date = min(target_date, max_date)
            vec = self._data_repo.get_feature_vector(data.store_id, data.product_id, lookup_date)
            if vec is None:
                raise DataNotFoundError(
                    f"No pre-computed features for store={data.store_id}, "
                    f"product={data.product_id}, date={target_date}. "
                    f"Available date range: {min_date} to {max_date}."
                )
            features.append(vec)

        return PreprocessedData(
            product_id=data.product_id,
            store_id=data.store_id,
            start_date=data.start_date,
            end_date=data.end_date,
            horizon=horizon,
            history=data.history,
            features=features,
        )
