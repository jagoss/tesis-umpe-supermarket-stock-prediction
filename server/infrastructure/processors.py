"""
Concrete data processing implementations for the MCP Prediction Server.

This module provides default implementations of preprocessing and postprocessing
interfaces, handling data transformation for ML model inputs and outputs.
"""

import logging
from typing import Any, Dict, List

from ..domain import Preprocessor, Postprocessor, PreprocessingError, PostprocessingError


class DefaultPreprocessor(Preprocessor):
    """
    Default implementation of input data preprocessing.
    
    This processor handles common preprocessing tasks for supermarket
    stock prediction models, including feature normalization, encoding,
    and data validation.
    
    Assumptions:
    - Input features include product_id, historical_sales, season, etc.
    - Numerical features may need normalization
    - Categorical features may need encoding
    """
    
    def __init__(
        self,
        feature_mapping: Dict[str, str] = None,
        logger: logging.Logger = None
    ) -> None:
        """
        Initialize the preprocessor with configuration.
        
        Args:
            feature_mapping: Optional mapping of input feature names to model features.
            logger: Optional logger for operation tracking.
        """
        self._feature_mapping = feature_mapping or {}
        self._logger = logger or logging.getLogger(__name__)
    
    def transform(self, features: Dict[str, Any]) -> Any:
        """
        Transform input features for model consumption.
        
        This method performs:
        1. Feature validation
        2. Feature mapping/renaming
        3. Data type conversion
        4. Normalization/encoding
        
        Args:
            features: Raw input features from the prediction request.
            
        Returns:
            Transformed data ready for model input.
            
        Raises:
            PreprocessingError: If transformation fails.
        """
        try:
            self._logger.debug(f"Preprocessing features: {list(features.keys())}")
            
            # Step 1: Validate required features
            self._validate_features(features)
            
            # Step 2: Apply feature mapping
            mapped_features = self._apply_feature_mapping(features)
            
            # Step 3: Convert and normalize data
            processed_features = self._normalize_features(mapped_features)
            
            self._logger.debug("Feature preprocessing completed successfully")
            return processed_features
            
        except Exception as e:
            self._logger.error(f"Preprocessing failed: {e}")
            raise PreprocessingError(
                "Failed to preprocess input features",
                details=str(e)
            ) from e
    
    def _validate_features(self, features: Dict[str, Any]) -> None:
        """
        Validate that required features are present and valid.
        
        Args:
            features: Input features to validate.
            
        Raises:
            PreprocessingError: If validation fails.
        """
        # TODO: Define domain-specific required features
        required_features = ["product_id"]  # Placeholder
        
        for feature in required_features:
            if feature not in features:
                raise PreprocessingError(f"Required feature missing: {feature}")
            
            if features[feature] is None:
                raise PreprocessingError(f"Feature cannot be null: {feature}")
    
    def _apply_feature_mapping(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply feature name mapping if configured.
        
        Args:
            features: Original features.
            
        Returns:
            Features with mapped names.
        """
        if not self._feature_mapping:
            return features
        
        mapped = {}
        for original_name, value in features.items():
            mapped_name = self._feature_mapping.get(original_name, original_name)
            mapped[mapped_name] = value
        
        return mapped
    
    def _normalize_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize and encode features for model consumption.
        
        Args:
            features: Features to normalize.
            
        Returns:
            Normalized features.
        """
        # TODO: Implement domain-specific normalization
        # This is a placeholder implementation
        
        normalized = {}
        for feature_name, value in features.items():
            if isinstance(value, (int, float)):
                # Placeholder normalization for numeric features
                normalized[feature_name] = float(value)
            elif isinstance(value, str):
                # Placeholder encoding for categorical features
                normalized[feature_name] = value.lower()
            elif isinstance(value, list):
                # Handle list features (e.g., historical sales)
                normalized[feature_name] = [float(x) for x in value if isinstance(x, (int, float))]
            else:
                normalized[feature_name] = value
        
        return normalized


class DefaultPostprocessor(Postprocessor):
    """
    Default implementation of output data postprocessing.
    
    This processor transforms raw model outputs into business-friendly
    format for API responses, including formatting, unit conversion,
    and confidence calculation support.
    """
    
    def __init__(
        self,
        output_format: str = "json",
        logger: logging.Logger = None
    ) -> None:
        """
        Initialize the postprocessor with configuration.
        
        Args:
            output_format: Desired output format ("json", "array", etc.).
            logger: Optional logger for operation tracking.
        """
        self._output_format = output_format
        self._logger = logger or logging.getLogger(__name__)
    
    def transform(self, raw_output: Any) -> Dict[str, Any]:
        """
        Transform raw model output into response format.
        
        This method performs:
        1. Output validation
        2. Format conversion
        3. Unit conversion if needed
        4. Metadata enrichment
        
        Args:
            raw_output: Raw output from the ML model.
            
        Returns:
            Processed prediction data for the response.
            
        Raises:
            PostprocessingError: If transformation fails.
        """
        try:
            self._logger.debug(f"Postprocessing output of type: {type(raw_output)}")
            
            # Step 1: Validate output
            self._validate_output(raw_output)
            
            # Step 2: Convert to standard format
            formatted_output = self._format_output(raw_output)
            
            # Step 3: Add metadata
            enriched_output = self._enrich_output(formatted_output)
            
            self._logger.debug("Output postprocessing completed successfully")
            return enriched_output
            
        except Exception as e:
            self._logger.error(f"Postprocessing failed: {e}")
            raise PostprocessingError(
                "Failed to postprocess model output",
                details=str(e)
            ) from e
    
    def _validate_output(self, output: Any) -> None:
        """
        Validate that model output is in expected format.
        
        Args:
            output: Raw model output to validate.
            
        Raises:
            PostprocessingError: If validation fails.
        """
        if output is None:
            raise PostprocessingError("Model output cannot be null")
        
        # TODO: Add domain-specific output validation
        # For example, check if output is within expected ranges
    
    def _format_output(self, output: Any) -> Dict[str, Any]:
        """
        Convert raw output to standard dictionary format.
        
        Args:
            output: Raw model output.
            
        Returns:
            Formatted output dictionary.
        """
        # TODO: Implement domain-specific output formatting
        # This is a placeholder implementation
        
        if isinstance(output, dict):
            return output
        elif isinstance(output, (list, tuple)):
            return {"forecast": list(output)}
        elif isinstance(output, (int, float)):
            return {"prediction": float(output)}
        else:
            # Convert other types to string representation
            return {"result": str(output)}
    
    def _enrich_output(self, formatted_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add metadata and business context to the output.
        
        Args:
            formatted_output: Formatted prediction output.
            
        Returns:
            Enriched output with metadata.
        """
        # Add timestamp and additional metadata
        enriched = formatted_output.copy()
        enriched["format"] = self._output_format
        
        # TODO: Add domain-specific metadata
        # For example:
        # - Unit information (e.g., "units": "items per day")
        # - Prediction horizon (e.g., "horizon_days": 7)
        # - Seasonality indicators
        
        return enriched
