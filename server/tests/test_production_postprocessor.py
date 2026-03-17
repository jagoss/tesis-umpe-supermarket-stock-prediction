"""Tests for ProductionPostprocessor."""

from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from server.application import ModelRawPrediction, PredictStockInput
from server.domain import PredictionError
from server.infrastructure.postprocessing import ProductionPostprocessor


def _make_repo(scaler: tuple[float, float] | None = (100.0, 20.0)) -> MagicMock:
    repo = MagicMock()
    repo.get_scaler_params.return_value = scaler
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


class TestProductionPostprocessor:
    def test_inverse_scale_applied(self) -> None:
        # mean=100, std=20; scaled value=0.5 → real = 0.5 * 20 + 100 = 110
        repo = _make_repo(scaler=(100.0, 20.0))
        post = ProductionPostprocessor(repo)
        raw = ModelRawPrediction(values=[0.5, 1.0, -0.5])
        result = post.postprocess(raw, _make_input())

        assert result.points[0].quantity == pytest.approx(110.0)  # 0.5*20+100
        assert result.points[1].quantity == pytest.approx(120.0)  # 1.0*20+100
        assert result.points[2].quantity == pytest.approx(90.0)  # -0.5*20+100

    def test_negative_clipped_to_zero(self) -> None:
        # mean=0, std=1; scaled=-5 → real=-5 → clipped to 0
        repo = _make_repo(scaler=(0.0, 1.0))
        post = ProductionPostprocessor(repo)
        raw = ModelRawPrediction(values=[-5.0])
        result = post.postprocess(raw, _make_input(start=date(2017, 8, 1), end=date(2017, 8, 1)))
        assert result.points[0].quantity == 0.0

    def test_dates_assigned_correctly(self) -> None:
        repo = _make_repo()
        post = ProductionPostprocessor(repo)
        raw = ModelRawPrediction(values=[0.0, 0.0, 0.0])
        result = post.postprocess(raw, _make_input(start=date(2017, 8, 1), end=date(2017, 8, 3)))

        assert result.points[0].date == date(2017, 8, 1)
        assert result.points[1].date == date(2017, 8, 2)
        assert result.points[2].date == date(2017, 8, 3)

    def test_missing_scaler_raises_prediction_error(self) -> None:
        repo = _make_repo(scaler=None)
        post = ProductionPostprocessor(repo)
        raw = ModelRawPrediction(values=[0.0, 0.0, 0.0])
        with pytest.raises(PredictionError, match="scaler parameters"):
            post.postprocess(raw, _make_input())

    def test_wrong_output_length_raises_prediction_error(self) -> None:
        repo = _make_repo()
        post = ProductionPostprocessor(repo)
        raw = ModelRawPrediction(values=[1.0, 2.0])  # 2 values for 3-day horizon
        with pytest.raises(PredictionError, match="2.*3|3.*2"):
            post.postprocess(raw, _make_input())

    def test_identifiers_in_result(self) -> None:
        repo = _make_repo()
        post = ProductionPostprocessor(repo)
        raw = ModelRawPrediction(values=[0.0])
        result = post.postprocess(
            raw,
            _make_input(
                store_id="5", product_id="DAIRY", start=date(2017, 8, 1), end=date(2017, 8, 1)
            ),
        )
        assert result.product_id == "DAIRY"
        assert result.store_id == "5"

    def test_scaler_params_queried_with_correct_keys(self) -> None:
        repo = _make_repo()
        post = ProductionPostprocessor(repo)
        raw = ModelRawPrediction(values=[0.0])
        post.postprocess(
            raw,
            _make_input(
                store_id="7", product_id="BREAD", start=date(2017, 8, 1), end=date(2017, 8, 1)
            ),
        )
        repo.get_scaler_params.assert_called_once_with("7", "BREAD")
