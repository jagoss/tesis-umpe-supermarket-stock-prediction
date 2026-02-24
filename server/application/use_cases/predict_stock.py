"""PredictStockUseCase orchestrates the prediction workflow.

Flow:
1. Validate input time window.
2. Preprocess input into model-ready features.
3. Call model to get raw predictions.
4. Postprocess into a ``StockForecast`` domain entity.
5. Map the domain entity to a ``PredictStockOutput`` application DTO.
"""
from __future__ import annotations

from datetime import date

from server.application.dto import PredictionPoint, PredictStockInput, PredictStockOutput
from server.application.ports import ModelPort, PostprocessorPort, PreprocessorPort
from server.domain import StockForecast, ValidationError


class PredictStockUseCase:
    """Use case: predict stock for a given product and store over a time window."""

    def __init__(
        self,
        *,
        preprocessor: PreprocessorPort,
        model: ModelPort,
        postprocessor: PostprocessorPort,
    ) -> None:
        """Create the use case with its dependencies.

        Args:
            preprocessor: Adapter that turns request data into model-ready features.
            model: Predictive model adapter.
            postprocessor: Adapter that maps raw model outputs to a domain entity.

        """
        self._preprocessor = preprocessor
        self._model = model
        self._postprocessor = postprocessor

    def execute(self, data: PredictStockInput) -> PredictStockOutput:
        """Run the prediction workflow and return the forecast.

        The pipeline produces a ``StockForecast`` domain entity, which is then
        mapped to the ``PredictStockOutput`` application DTO with rounded
        integer quantities suitable for inventory decisions.

        Args:
            data: Input parameters for the forecast.

        Returns:
            The predicted quantities for each day in the requested window.

        """
        self._validate_dates(data.start_date, data.end_date)
        pre = self._preprocessor.preprocess(data)
        raw = self._model.predict(pre)
        forecast = self._postprocessor.postprocess(raw, data)
        return self._to_output(forecast)

    @staticmethod
    def _to_output(forecast: StockForecast) -> PredictStockOutput:
        """Map a domain ``StockForecast`` to an application DTO.

        Quantities are rounded to the nearest integer because the output
        represents discrete item counts for stock-ordering decisions.

        """
        return PredictStockOutput(
            product_id=forecast.product_id,
            store_id=forecast.store_id,
            predictions=[
                PredictionPoint(
                    date=point.date,
                    quantity=int(round(point.quantity)),
                )
                for point in forecast.points
            ],
        )

    @staticmethod
    def _validate_dates(start: date, end: date) -> None:
        """Validate that the time window is well-formed.

        Raises:
            ValidationError: If end is before start.

        """
        if end < start:
            raise ValidationError("end_date must be greater than or equal to start_date")
