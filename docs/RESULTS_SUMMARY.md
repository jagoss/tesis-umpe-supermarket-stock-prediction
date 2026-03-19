# Resumen de Resultados Encontrados

Fecha de auditoria: 2026-03-19 (America/Montevideo).

## 1) Modelos probados (evidencia en repo)

1. `SeasonalNaive` (baseline)
   Fuente: `.notebooks/cv_results_baseline_retrained.csv`.
2. `AutoETS` (baseline)
   Fuente: `.notebooks/cv_results_baseline_retrained.csv`.
3. `LGBMRegressor` global con `MLForecast` + `LocalStandardScaler` + lags/rolling + feriados
   Fuente: notebooks `Global_Simple_LightGBM_Timeseries_Forecast_Final*.ipynb` (celdas de entrenamiento/CV).
4. Adaptador de serving ONNX
   Fuente: `server/infrastructure/models/onnx_model.py`, artefactos `server/models/example_model.onnx` y `server/models/lightgbm_model.onnx`.
5. Backend dummy para pruebas de API
   Fuente: `server/infrastructure/models/dummy_model.py`, tests y workflows CI.

## 2) Metricas encontradas

## 2.1 Metricas directamente visibles en artefactos

- Baseline CV tiene columnas de prediccion para `SeasonalNaive` y `AutoETS` junto a `y`.
  Fuente: `.notebooks/cv_results_baseline_retrained.csv` (7760 filas, 97 series, 5 cortes temporales).
- En notebook existe definicion de RMSLE para LGBM.
  Fuente: notebook academico celda 21.
- En el output embebido del notebook academico se conserva el valor `LGBM RMSLE: 0.5380629595521763`.
  Fuente: [LGBM_CV_EVIDENCE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LGBM_CV_EVIDENCE.md), derivado de notebook academico celda 35 (stdout preservado).

## 2.2 Metricas derivadas desde archivo existente (calculadas en esta auditoria, no inventadas)

Calculadas sobre `.notebooks/cv_results_baseline_retrained.csv`:

| Modelo | RMSLE | MAE | RMSE |
|---|---:|---:|---:|
| SeasonalNaive | 0.6852 | 76.2865 | 269.6715 |
| AutoETS | 0.5814 | 65.1614 | 243.2491 |

Observacion: en ese artefacto baseline, `AutoETS` supera a `SeasonalNaive` en las tres metricas.

## 2.3 Metricas no recuperables con trazabilidad completa

- `MAE` y `RMSE` del modelo LGBM en CV: no recuperables con trazabilidad equivalente a la de los baselines porque no existe un `cv_results_lgbm.csv` exportado ni una tabla versionada con predicciones por corte.
  Fuente: notebook academico celda 35 y ausencia de artefacto tabular equivalente en repo.
- Detalle de errores por ventana/cutoff para LGBM: no recuperable en forma tabular reutilizable desde el estado actual del repositorio.
  Fuente: ausencia de artefacto exportado de CV para LGBM.

## 3) Tablas/archivos de resultados disponibles

1. Baseline CV:
   `.notebooks/cv_results_baseline_retrained.csv`
   - shape: `(7760, 6)`
   - columnas: `unique_id, ds, cutoff, y, SeasonalNaive, AutoETS`
2. Evidencia documental LGBM CV:
   [LGBM_CV_EVIDENCE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LGBM_CV_EVIDENCE.md)
   - metrica visible: `RMSLE = 0.5380629595521763`
   - fuente: output embebido del notebook academico, celda 35
   - limitacion: no reemplaza un CSV exportado de CV
3. Submission:
   `.notebooks/submission.csv`
   - shape: `(28512, 2)`
   - columnas: `id, sales`
   - `id` coincide con `data/sample_submission.csv` (mismo set y cardinalidad)
4. Importancia de variables (tabla en output de notebook):
   notebook academico celda 40 (top-10, p.ej. `lag1`, `family`, `lag7`, `day_of_week`, `onpromotion`).
5. Artefactos de serving de datos:
   - `data/precomputed_features.parquet`: `(1701810, 33)`, 30 features + 3 indices, rango de fechas `2025-01-01` a `2027-08-13`.
   - `data/scaler_params.parquet`: `(1782, 4)`.
6. Artefactos ONNX:
   - `server/models/example_model.onnx`: input `[None,4]`.
   - `server/models/lightgbm_model.onnx`: input `[None,30]`.

## 4) Figuras disponibles

- No se encontraron figuras de resultados ML exportadas como `png/jpg/svg` en notebooks.
- Figura raster versionada encontrada: `app-web/assets/logo.png` (no es figura de resultados experimentales).
- Diagramas tecnicos disponibles en PlantUML:
  `.docs/diagrams/high_level_diagram.puml`, `.docs/diagrams/agent_diagram.puml`, `.docs/diagrams/mcp_server.puml`.

## 5) Hallazgos principales observables

1. Existen resultados baseline tabulados y trazables (`SeasonalNaive`, `AutoETS`) con suficiente detalle para recomputar metricas.
2. El output embebido del notebook permite recuperar un `RMSLE = 0.5380629595521763` para `LGBMRegressor`, inferior a los `RMSLE` observados para `AutoETS` (`0.5814`) y `SeasonalNaive` (`0.6852`) en esa metrica puntual, aunque sobre evidencia no completamente homogenea en alcance.
3. El pipeline LGBM->ONNX esta implementado y hay artefacto ONNX de 30 features en `server/models/lightgbm_model.onnx`.
4. El sistema de serving productivo con features precomputadas esta materializado (`precomputed_features.parquet` + `scaler_params.parquet`) y conectado en el backend `production`.
5. La calidad de codigo backend tiene buena cobertura en corrida local (`TOTAL 98%`) pero la corrida completa falla por dependencia faltante de `trio` en pruebas MCP async parametrizadas.
6. Hay desalineacion documental entre archivos que describen estado "toy-only" y la presencia actual del artefacto `lightgbm_model.onnx`.

## 6) Limitaciones y ambiguedades

1. El valor `RMSLE` final de LGBM queda visible en el output embebido del notebook, pero no en un artefacto tabular exportado y recomputable.
2. No hay archivo exportado de CV del modelo LGBM equivalente a `cv_results_baseline_retrained.csv`, por lo que faltan `MAE`, `RMSE` y detalle por corte con trazabilidad equivalente.
3. La comparación visible entre `RMSLE` de LGBM y baselines no es perfectamente homogénea en alcance, porque el baseline tabulado cubre 97 series y la validación documentada de `LightGBM` se describe sobre 100 series.
4. `openapi.json` en la raiz no es JSON valido (contiene mensaje de error de runtime), por lo que no sirve como evidencia del contrato API.
5. Falta paquete bibliografico estructurado (`.bib`) y falta trazabilidad formal de citas en documentos tecnicos.
6. Parte de la documentacion de arquitectura corresponde a una arquitectura previa/planificada y no refleja de forma exacta el stack actual desplegado.
