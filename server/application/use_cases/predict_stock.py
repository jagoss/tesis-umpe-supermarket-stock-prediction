"""PredictStockUseCase orchestrates the prediction workflow.

Flow:
- Validate input time window.
- Preprocess input into features.
- Call model to get raw predictions.
- Postprocess into output DTO.
"""
from __future__ import annotations

from datetime import date

from ...domain.exceptions import ValidationError
from ..dto import PredictStockInput, PredictStockOutput
from ..ports import ModelPort, PostprocessorPort, PreprocessorPort


class PredictStockUseCase:
    """Use case: predict stock for a given product and store over a time window."""

    def __init__(self, *, preprocessor: PreprocessorPort, model: ModelPort, postprocessor: PostprocessorPort) -> None:
        """Create the use case with its dependencies.

        Args:
            preprocessor: Adapter that turns request data into model-ready features.
            model: Predictive model adapter.
            postprocessor: Adapter that maps raw model outputs to output DTOs.
        """
        self._preprocessor = preprocessor
        self._model = model
        self._postprocessor = postprocessor

    def execute(self, data: PredictStockInput) -> PredictStockOutput:
        """Run the prediction workflow and return the forecast.

        Args:
            data: Input parameters for the forecast.

        Returns:
            The predicted quantities for each day in the requested window.
        """
        self._validate_dates(data.start_date, data.end_date)
        pre = self._preprocessor.preprocess(data)
        raw = self._model.predict(pre)
        return self._postprocessor.postprocess(raw, data)

    @staticmethod
    def _validate_dates(start: date, end: date) -> None:
        """Validate that the time window is well-formed.

        Raises:
            ValidationError: If end is before start.
        """
        if end < start:
            raise ValidationError("end_date must be greater than or equal to start_date")
