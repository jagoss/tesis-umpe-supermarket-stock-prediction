# Figuras listas para integrar en EDA

Este archivo reúne las cinco figuras seleccionadas para el capítulo de análisis exploratorio de datos, con numeración sugerida, pie de figura y texto breve de referencia en el cuerpo del capítulo.

## Convención sugerida

- Usar `Figura 1` a `Figura 5` en el orden definido aquí.
- Mantener el orden porque sigue la secuencia argumental actual de [eda.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/eda.md):
  1. covariables agregadas;
  2. feriados nacionales;
  3. feriados regionales;
  4. feriados locales;
  5. patrones de calendario.
- Si el capítulo final cambia de estructura, conviene conservar la numeración relativa y mover solo la posición del bloque.

## Figura 1

Texto de referencia sugerido en el cuerpo:

`La Figura 1 resume la relación descriptiva entre las ventas promedio y tres covariables agregadas de interés: promociones, transacciones y precio del petróleo.`

Bloque listo para pegar:

```md
![Figura 1. Ventas promedio, promociones, transacciones y petróleo](figures/eda/eda_01_sales_covariates.png)

**Figura 1. Ventas promedio, promociones, transacciones y petróleo.** Relación descriptiva entre la evolución temporal de las ventas promedio y las covariables agregadas `onpromotion`, `transactions` y `oil`, junto con sus gráficos de asociación visual. La figura se utiliza como evidencia exploratoria del vínculo descriptivo entre demanda y variables exógenas. Fuente: elaboración propia a partir de `.notebooks/analisis_exploratorio_ecuador_sales_forecast.ipynb`, celda 57.
```

## Figura 2

Texto de referencia sugerido en el cuerpo:

`La Figura 2 muestra que ciertos eventos nacionales presentan diferencias visuales más marcadas entre días festivos y no festivos, lo que respalda su consideración dentro del análisis exploratorio.`

Bloque listo para pegar:

```md
![Figura 2. Distribución de ventas en festividades nacionales](figures/eda/eda_02_national_holidays.png)

**Figura 2. Distribución de ventas en festividades nacionales.** Comparación visual de la distribución de ventas entre días festivos nacionales y días no festivos para eventos seleccionados, incluyendo feriados de alcance nacional y sábados designados como `Work Day`. La figura aporta evidencia exploratoria sobre la relevancia relativa de ciertos eventos nacionales en la dinámica de ventas. Fuente: elaboración propia a partir de `.notebooks/analisis_exploratorio_ecuador_sales_forecast.ipynb`, celda 60.
```

## Figura 3

Texto de referencia sugerido en el cuerpo:

`La Figura 3 sugiere que las festividades regionales presentan diferencias visuales más acotadas que las observadas en los eventos nacionales.`

Bloque listo para pegar:

```md
![Figura 3. Distribución de ventas en festividades regionales](figures/eda/eda_03_regional_holidays.png)

**Figura 3. Distribución de ventas en festividades regionales.** Comparación visual entre días con festividad regional y días sin festividad regional en las provincias para las que el dataset registra este tipo de eventos. La figura se interpreta como evidencia descriptiva y no como prueba causal del efecto de los feriados regionales sobre las ventas. Fuente: elaboración propia a partir de `.notebooks/analisis_exploratorio_ecuador_sales_forecast.ipynb`, celda 63.
```

## Figura 4

Texto de referencia sugerido en el cuerpo:

`La Figura 4 complementa el análisis territorial al mostrar la distribución de ventas en festividades locales para ciudades seleccionadas.`

Bloque listo para pegar:

```md
![Figura 4. Distribución de ventas en festividades locales](figures/eda/eda_04_local_holidays.png)

**Figura 4. Distribución de ventas en festividades locales.** Comparación visual de la distribución de ventas entre días con festividad local y días sin festividad local en ciudades seleccionadas del panel. La figura permite contrastar la heterogeneidad espacial de los eventos locales y su menor impacto relativo frente a los eventos nacionales. Fuente: elaboración propia a partir de `.notebooks/analisis_exploratorio_ecuador_sales_forecast.ipynb`, celda 64.
```

## Figura 5

Texto de referencia sugerido en el cuerpo:

`La Figura 5 concentra los principales patrones de calendario observados en el EDA, incluyendo diferencias por día de la semana, mes y año, así como variaciones intraanuales.`

Bloque listo para pegar:

```md
![Figura 5. Patrones de ventas por variables de calendario](figures/eda/eda_05_calendar_patterns.png)

**Figura 5. Patrones de ventas por variables de calendario.** Distribución y evolución de las ventas según `day_of_week`, `month`, `year`, `day`, `day_of_year` y `week_of_year`, utilizando períodos sin feriados para reducir interferencias del calendario festivo. La figura aporta evidencia visual sobre regularidades semanales, mensuales y anuales que justifican el uso posterior de variables temporales derivadas. Fuente: elaboración propia a partir de `.notebooks/analisis_exploratorio_ecuador_sales_forecast.ipynb`, celda 67.
```

## Orden sugerido de inserción en `EDA`

1. Insertar la `Figura 1` dentro de la sección `Promociones, transacciones, petróleo y patrones de calendario`.
2. Insertar las `Figuras 2`, `3` y `4` dentro de la sección `Feriados, escala territorial y relevancia relativa`.
3. Insertar la `Figura 5` al final de la sección `Promociones, transacciones, petróleo y patrones de calendario`, o inmediatamente antes de `Implicancias para el problema de negocio y el modelado`.

## Nota editorial

Si más adelante se incorporan figuras adicionales de resultados o arquitectura, esta numeración de `EDA` puede mantenerse sin cambios siempre que el manuscrito use numeración global correlativa al momento de la compilación final.
