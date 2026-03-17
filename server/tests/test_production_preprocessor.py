"""Tests for ProductionPreprocessor."""

from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from server.application import PredictStockInput
from server.domain import DataNotFoundError
from server.infrastructure.preprocessing import ProductionPreprocessor


def _make_repo(
    feature_vector: list[float] | None = None,
    date_range: tuple[date, date] = (date(2017, 1, 1), date(2017, 12, 31)),
) -> MagicMock:
    repo = MagicMock()
    repo.get_feature_vector.return_value = feature_vector
    repo.get_available_date_range.return_value = date_range
    return repo


def _make_input(
    start: date = date(2017, 8, 1),
    end: date = date(2017, 8, 3),
    store_id: str = "1",
    product_id: str = "BEVERAGES",
) -> PredictStockInput:
    return PredictStockInput(
        product_id=product_id,
        store_id=store_id,
        start_date=start,
        end_date=end,
    )


class TestProductionPreprocessor:
    def test_features_matrix_assembled(self) -> None:
        vec = [1.0, 2.0, 3.0]
        repo = _make_repo(feature_vector=vec)
        pre = ProductionPreprocessor(repo)
        result = pre.preprocess(_make_input(start=date(2017, 8, 1), end=date(2017, 8, 3)))

        assert result.horizon == 3
        assert result.features is not None
        assert len(result.features) == 3
        assert result.features[0] == vec

    def test_calls_repo_for_each_date(self) -> None:
        repo = _make_repo(feature_vector=[0.0])
        pre = ProductionPreprocessor(repo)
        pre.preprocess(_make_input(start=date(2017, 8, 1), end=date(2017, 8, 3)))

        assert repo.get_feature_vector.call_count == 3
        calls = [c.args for c in repo.get_feature_vector.call_args_list]
        assert calls[0] == ("1", "BEVERAGES", date(2017, 8, 1))
        assert calls[1] == ("1", "BEVERAGES", date(2017, 8, 2))
        assert calls[2] == ("1", "BEVERAGES", date(2017, 8, 3))

    def test_missing_date_raises_data_not_found(self) -> None:
        repo = _make_repo(feature_vector=None)
        pre = ProductionPreprocessor(repo)
        with pytest.raises(DataNotFoundError, match="BEVERAGES"):
            pre.preprocess(_make_input())

    def test_error_message_includes_available_range(self) -> None:
        repo = _make_repo(
            feature_vector=None,
            date_range=(date(2014, 1, 1), date(2017, 10, 31)),
        )
        pre = ProductionPreprocessor(repo)
        with pytest.raises(DataNotFoundError, match="2014-01-01"):
            pre.preprocess(_make_input())

    def test_identifiers_forwarded(self) -> None:
        repo = _make_repo(feature_vector=[5.0])
        pre = ProductionPreprocessor(repo)
        result = pre.preprocess(
            _make_input(
                store_id="3", product_id="DAIRY", start=date(2017, 8, 1), end=date(2017, 8, 1)
            )
        )
        assert result.product_id == "DAIRY"
        assert result.store_id == "3"
        assert result.start_date == date(2017, 8, 1)
        assert result.end_date == date(2017, 8, 1)

    def test_single_day_horizon(self) -> None:
        repo = _make_repo(feature_vector=[1.0, 2.0])
        pre = ProductionPreprocessor(repo)
        result = pre.preprocess(_make_input(start=date(2017, 8, 5), end=date(2017, 8, 5)))
        assert result.horizon == 1
        assert result.features is not None
        assert len(result.features) == 1

    def test_history_forwarded(self) -> None:
        repo = _make_repo(feature_vector=[0.0])
        pre = ProductionPreprocessor(repo)
        history = [(date(2017, 7, 31), 42.0)]
        inp = PredictStockInput(
            product_id="BEVERAGES",
            store_id="1",
            start_date=date(2017, 8, 1),
            end_date=date(2017, 8, 1),
            history=history,
        )
        result = pre.preprocess(inp)
        assert result.history == history
