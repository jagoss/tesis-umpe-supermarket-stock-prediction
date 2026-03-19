# Evidencia Documental de CV LightGBM

Fecha de consolidacion: 2026-03-19 (America/Montevideo).

## Hallazgo consolidado

Existe evidencia directa en el repositorio del valor final de `RMSLE` obtenido por el modelo `LightGBM` durante la validacion cruzada documentada en el notebook academico.

| Campo | Valor |
|---|---|
| Modelo | `LGBMRegressor` |
| Metrica visible | `RMSLE` |
| Valor visible | `0.5380629595521763` |
| Fuente primaria | [Global_Simple_LightGBM_Timeseries_Forecast_Final_academic.ipynb](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/Global_Simple_LightGBM_Timeseries_Forecast_Final_academic.ipynb) |
| Ubicacion | celda 35, output embebido del notebook |
| Configuracion observable asociada | `h=16`, `n_windows=5`, `step_size=120`, subconjunto de 100 series |
| Naturaleza de la evidencia | salida `stdout` preservada en el `.ipynb`, no CSV exportado |

## Transcripcion minima del output relevante

```text
LGBM RMSLE: 0.5380629595521763
```

## Limites de esta evidencia

1. La celda fuente contiene actualmente un error de sintaxis en la `f-string`, por lo que la reproducibilidad directa de esa impresion no queda garantizada sin correccion del notebook.
2. No existe en el repositorio un archivo equivalente a [cv_results_baseline_retrained.csv](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/cv_results_baseline_retrained.csv) para `LightGBM`.
3. Esta evidencia permite sostener el `RMSLE` final visible, pero no permite recomputar con la misma trazabilidad `MAE`, `RMSE`, metricas por corte o analisis detallado de errores.
4. La comparacion con los baselines debe formularse con cautela: el `RMSLE` de `LightGBM` proviene del output embebido del notebook, mientras que las metricas baseline provienen de un artefacto tabular versionado.
5. La comparacion numerica tampoco es completamente homogenea en alcance, porque el artefacto baseline auditado contiene 97 series, mientras que la validacion documentada de `LightGBM` se describe sobre un subconjunto de 100 series.
