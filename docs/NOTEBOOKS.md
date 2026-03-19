# NOTEBOOKS Auditados

Fecha de auditoria: 2026-03-18 (America/Montevideo).

## 1) `.notebooks/Global_Simple_LightGBM_Timeseries_Forecast_Final.ipynb`

- Objetivo:
  Entrenar un modelo global LightGBM con `MLForecast`, exportarlo a ONNX y generar `submission.csv`.
- Inputs principales:
  `train.csv`, `test.csv`, `transactions.csv`, `holidays_events.csv`, `stores.csv`, `oil.csv`, `sample_submission.csv` (celdas de carga del notebook; rutas relativas al directorio de ejecucion).
- Outputs principales:
  `lightgbm_model.onnx` (export), `final_forecast` y `submission.csv`.
- Metricas o graficos relevantes:
  - Define metrica `RMSLE` y ejecuta `cross_validation` temporal (h=16, n_windows=5, step_size=120, subset=100 series).
  - Muestra importancia de variables (top-10) y muestra de predicciones.
  - No hay figuras PNG embebidas en outputs.
- Clasificacion:
  Mixto (exploratorio + pipeline de salida final).
- Problemas de reproducibilidad detectados:
  - Usa `!pip install` dentro del notebook sin versionado fijo.
  - Las rutas de entrada son relativas al cwd y no usan `data/`; en este repo los CSV estan en `data/`.
  - La celda que imprime RMSLE tiene error de sintaxis en el `f-string` (`actual_col="y"` dentro de comillas dobles), por lo que el valor RMSLE no es reproducible tal como esta guardado.
  - Hay salidas guardadas que no coinciden con el codigo actual (estado no determinista del cuaderno).
  - No exporta `cv_results_lgbm` a archivo.
- Secciones de tesis que puede alimentar:
  Metodologia (pipeline de features/modelo), Experimentos (configuracion CV), Implementacion (export ONNX), Resultados (submission y feature importance), Conclusiones tecnicas.

Fuentes:
- `.notebooks/Global_Simple_LightGBM_Timeseries_Forecast_Final.ipynb` (estructura general, celdas equivalentes a las del notebook academico).

## 2) `.notebooks/Global_Simple_LightGBM_Timeseries_Forecast_Final_academic.ipynb`

- Objetivo:
  Version academizada del cuaderno de entrenamiento/evaluacion/exportacion LightGBM->ONNX y generacion de submission.
- Inputs principales:
  `train.csv`, `test.csv`, `transactions.csv`, `holidays_events.csv`, `stores.csv`, `oil.csv`, `sample_submission.csv`.
- Outputs principales:
  `lightgbm_model.onnx`, `submission.csv`, tablas de features, tablas de importancia de variables, muestra de predicciones.
- Metricas o graficos relevantes:
  - Metrica definida: RMSLE (celda de funcion dedicada).
  - `cross_validation` temporal configurada (h=16, n_windows=5, step_size=120) sobre subset aleatorio de 100 series.
  - Seleccion de feriados por correlacion `abs(corr) > 0.1` (11 feriados seleccionados).
  - Feature importance top-10 disponible en output tabular.
  - No hay graficos PNG embebidos en el notebook.
- Clasificacion:
  Final/documental para tesis (no solo exploratorio).
- Problemas de reproducibilidad detectados:
  - Misma celda con error de sintaxis en impresion RMSLE (valor no trazable en estado actual del codigo).
  - Rutas de datos no parametrizadas y no alineadas con `data/`.
  - Dependencias instaladas en caliente (`!pip install`) sin lockfile del entorno del notebook.
  - Semilla fijada para muestreo (`np.random.seed(42)`), pero el entrenamiento LightGBM no fija explicitamente `random_state`.
  - No se guarda `cv_results_lgbm` en archivo; por eso no hay tabla de metricas LGBM exportada.
- Secciones de tesis que puede alimentar:
  Resumen metodologico, Metodologia, EDA (tablas de exploracion), Experimentos, Resultados, Implementacion (export ONNX), Conclusiones.

Fuentes (celdas):
- Carga de datos: celda 5.
- Preparacion/features: celdas 8-18.
- Metrica RMSLE: celda 21.
- Configuracion CV: celda 23.
- Modelo MLForecast+LightGBM: celdas 25, 37.
- Export ONNX: celda 30.
- Lista de 30 features: celda 31 (output).
- Inferencia ONNX de validacion puntual: celda 32.
- CV LGBM (con error de sintaxis en print): celda 35.
- Importancia de variables: celda 40 (output).
- Forecast final y shape: celda 44 (output).
- Generacion de submission: celda 47.

## 3) Directorio adicional de notebooks

- `.notebooks/store-sales-time-series-forecasting/` existe pero esta vacio.

Implicancia:
- No aporta evidencia adicional para resultados/modelado en el estado actual.

## 4) `.notebooks/analisis_exploratorio_ecuador_sales_forecast.ipynb`

- Objetivo:
  Desarrollar un EDA específico del problema de ventas en supermercados de Ecuador, con énfasis en completitud temporal, ceros estructurales, promociones, transacciones, petróleo, feriados y variables de calendario.
- Inputs principales:
  `data/train.csv`, `data/test.csv`, `data/oil.csv`, `data/stores.csv`, `data/transactions.csv`, `data/holidays_events.csv`.
- Outputs principales:
  Tablas impresas de cobertura y faltantes, tablas de holidays procesados, visualizaciones embebidas de correlación/boxplots/series temporales.
- Metricas o graficos relevantes:
  - `Number of target series: 1782`.
  - Fechas faltantes en el panel crudo: `2013-12-25`, `2014-12-25`, `2015-12-25`, `2016-12-25`.
  - `Number of missing oil dates: 486`, todas en fines de semana.
  - `transactions`: 91.152 registros esperados, 83.488 observados, 7.546 ausencias asociadas a cero ventas y 118 faltantes adicionales.
  - Gráficos de asociación visual entre ventas promedio, promociones, transacciones y petróleo.
  - Boxplots de feriados nacionales, regionales y locales.
  - Gráficos de patrones por `day`, `month`, `year`, `day_of_week`, `day_of_year`, `week_of_year`.
- Clasificacion:
  Exploratorio/documental, con valor directo para la sección EDA de la tesis.
- Problemas de reproducibilidad detectados:
  - Varias conclusiones están en markdown interpretativo y no siempre acompañadas de tablas exportadas.
  - Las figuras existen solo como outputs embebidos del notebook, no como archivos PNG/SVG versionados.
  - Mezcla decisiones de preprocesamiento con EDA, lo que exige lectura cuidadosa para separar descripción de transformación.
- Secciones de tesis que puede alimentar:
  EDA, Metodología (preparación de datos auxiliares), Justificación de variables de calendario y feriados, Limitaciones de datos.

## 5) `.notebooks/analisis_exploratorio_ecuador_sales_forecast_academic.ipynb`

- Objetivo:
  Versión académicamente estructurada del notebook exploratorio anterior, enriquecida con abstract, introducción, contexto metodológico por sección y conclusiones.
- Inputs principales:
  Los mismos que el notebook exploratorio original.
- Outputs principales:
  Conserva outputs del notebook original y agrega celdas markdown formales para facilitar su reutilización documental.
- Metricas o graficos relevantes:
  Hereda los del notebook base; no añade métricas nuevas.
- Clasificacion:
  Documental/tesis.
- Problemas de reproducibilidad detectados:
  - Comparte las limitaciones de ejecución y exportación visual del notebook base.
  - Mejora la estructura argumental, pero no reemplaza la necesidad de figuras exportadas si se desean insertar directamente en el manuscrito.
- Secciones de tesis que puede alimentar:
  EDA, Metodología descriptiva, Apéndice documental.
