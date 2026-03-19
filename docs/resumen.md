# Resumen

Esta tesis aborda el problema de predicción de demanda en supermercados a partir de series temporales diarias por tienda y familia de producto. El trabajo se apoya en datos históricos del desafío público Store Sales de Kaggle y desarrolla un pipeline que combina preparación de datos, ingeniería de características, validación del modelo y despliegue del servicio de inferencia.

Metodológicamente, la solución implementa un enfoque global basado en `LightGBM` y `MLForecast`, utilizando rezagos, variables de calendario, promociones y feriados, junto con escalado local por serie. En paralelo, el proyecto materializa una arquitectura de serving que exporta el modelo a `ONNX`, precomputa características en artefactos `Parquet` y expone la funcionalidad de predicción mediante API REST y `MCP`, con integración prevista hacia Onyx.

La evidencia experimental preservada en el repositorio permite recuperar resultados baseline para `SeasonalNaive` y `AutoETS`, así como un `RMSLE = 0.5380629595521763` visible para `LightGBM`. Este valor constituye una señal favorable frente a los baselines disponibles. No obstante, la interpretación cuantitativa debe formularse con cautela, dado que no existe un artefacto tabular exportado de validación cruzada para `LightGBM`, no quedan trazables `MAE` ni `RMSE` equivalentes y la comparación documentada no está cerrada sobre el mismo conjunto de series.

En consecuencia, el principal aporte del trabajo radica en demostrar la viabilidad metodológica y de ingeniería de una solución de predicción de demanda desplegable, más que en presentar una validación cuantitativa exhaustiva del modelo final. La tesis concluye que el proyecto constituye una base sólida para apoyo a decisiones de reposición en un contexto supermercadista, aunque requiere un cierre experimental más homogéneo y reproducible para fortalecer sus afirmaciones finales.

**Palabras clave:** predicción de demanda, series temporales multiserie, supermercados, LightGBM, MLForecast, ONNX, serving de modelos.
