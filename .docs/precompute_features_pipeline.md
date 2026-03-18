# Pipeline de Pre-cómputo de Características para Inferencia en Producción

> **Propósito del Documento:** Descripción técnica y fundamentación académica del
> script `scripts/precompute_features.py`, componente crítico que materializa
> el puente entre la fase de entrenamiento del modelo y su despliegue en
> producción.  Diseñado como insumo para el capítulo de implementación del
> trabajo de titulación.
>
> **Última Actualización:** 2026-03-18

---

## 1. Introducción y Motivación

En el ciclo de vida de un sistema de aprendizaje automático, una de las
fuentes de error más frecuentes y difíciles de diagnosticar es la
**discrepancia entre las características (features) utilizadas durante el
entrenamiento y las que se suministran durante la inferencia en producción**
(Sculley et al., 2015; Breck et al., 2019).  Esta discrepancia, conocida en
la literatura como *training-serving skew*, puede manifestarse de múltiples
formas:

- **Skew de esquema:** el modelo espera 30 columnas pero recibe 21, o los
  nombres de las columnas difieren (e.g., `lag1` vs. `lag_1`).
- **Skew de distribución:** las transformaciones estadísticas (escalado,
  codificación categórica) se computan con parámetros distintos a los del
  entrenamiento.
- **Skew de orden:** el vector de entrada presenta las características en un
  orden diferente al que el modelo aprendió, produciendo predicciones
  silenciosamente incorrectas.

El script `precompute_features.py` fue diseñado específicamente para eliminar
estas tres categorías de *skew*.  Su función es **replicar de manera exacta el
pipeline de ingeniería de características** que el cuaderno de entrenamiento
(`Global_Simple_LightGBM_Timeseries_Forecast_usar.ipynb`) aplicó sobre los
datos del concurso *Corporación Favorita Grocery Sales Forecasting* de Kaggle,
y materializar el resultado en archivos Parquet que el servidor de producción
consulta en tiempo de inferencia.

### 1.1 El Problema Concreto

El modelo de producción (`models/lightgbm_model.onnx`) es un ensamble de
árboles de decisión entrenado con LightGBM a través de la librería MLForecast
de Nixtla.  Durante el entrenamiento, MLForecast construye internamente un
pipeline complejo de transformaciones que incluye:

1. Escalado local por serie temporal (`LocalStandardScaler`).
2. Generación de 6 variables de rezago (*lags*) sobre las ventas escaladas.
3. Transformaciones sobre los rezagos: media expandida y medias móviles.
4. Variables calendáricas extraídas de la fecha.
5. Variables indicadoras de feriados seleccionados por correlación.
6. Codificación categórica de la familia de producto.

Al exportar el modelo entrenado a formato ONNX, se exporta **únicamente el
modelo** — no el pipeline de transformaciones.  El operador
`TreeEnsembleRegressor` del modelo ONNX espera recibir exactamente 30
características numéricas en un orden preciso, pero no tiene conocimiento
de cómo producirlas.

**Sin un mecanismo que reproduzca fielmente estas transformaciones, el modelo
en producción recibiría entradas incorrectas y produciría predicciones sin
valor.**

---

## 2. Diseño de la Solución

### 2.1 Pre-cómputo Offline vs. Cómputo Online

Se evaluaron dos estrategias para proveer las características al modelo en
producción:

| Estrategia | Descripción | Ventajas | Desventajas |
|---|---|---|---|
| **Cómputo online** | Cargar los CSVs crudos (~125 MB) en memoria y recalcular lags, medias móviles y escalado en cada petición HTTP | Sin archivos intermedios | Latencia inaceptable: computar una media móvil de 365 días sobre ~3 millones de filas por petición; alto uso de CPU; duplica lógica del cuaderno con riesgo de divergencia |
| **Pre-cómputo offline** | Ejecutar el pipeline una sola vez como proceso batch, persistir los resultados en Parquet, y servir consultas O(1) por clave primaria | Latencia sub-milisegundo en inferencia; garantía de consistencia con el entrenamiento; el archivo Parquet actúa como contrato entre entrenamiento y producción | Requiere regenerar el Parquet si cambian los datos de entrada o el modelo |

La naturaleza **estática** del dataset Kaggle (datos históricos de 2013-2017
que no reciben nuevas observaciones) hace que el enfoque de pre-cómputo sea la
elección natural: se ejecuta una vez y el artefacto resultante se monta como
volumen de solo lectura en el contenedor Docker del servidor de predicción.

### 2.2 Artefactos Generados

El script produce dos archivos Parquet:

| Artefacto | Esquema | Tamaño Aprox. | Propósito |
|---|---|---|---|
| `precomputed_features.parquet` | `(store_nbr, family, date)` + 30 columnas de características | 50-100 MB | Vector de entrada completo para cada combinación serie-fecha |
| `scaler_params.parquet` | `(store_nbr, family, mean, std)` | < 1 MB | Parámetros del `LocalStandardScaler` para invertir la transformación de la predicción |

El primer archivo es consumido por `ParquetDataRepository` para consultas de
características.  El segundo es consumido por `ProductionPostprocessor` para
des-escalar las predicciones del modelo (que están en unidades
estandarizadas) y devolver unidades de venta reales.

---

## 3. Replicación del Pipeline de Entrenamiento

El principio rector del script es la **reproducibilidad exacta**: cada
transformación replica el comportamiento del cuaderno de entrenamiento,
utilizando las mismas funciones de pandas/numpy, en el mismo orden y con los
mismos parámetros.

### 3.1 Preparación de los Datos Base

```python
df["sales"] = df["sales"].clip(lower=0).replace(0, 0.01)
```

El cuaderno define la función `clean_sales_data` que:
1. Recorta valores negativos a cero (`clip(lower=0)`).
2. Reemplaza ceros exactos por 0.01 para evitar divisiones por cero en el
   escalado.

El script replica esta limpieza antes de cualquier cálculo estadístico.

### 3.2 Escalado Local por Serie Temporal (LocalStandardScaler)

MLForecast aplica un `LocalStandardScaler` como `target_transform`, lo que
significa que cada serie temporal `(store_nbr, family)` se estandariza
independientemente:

$$
\text{sales\_scaled}_{i,j,t} = \frac{\text{sales}_{i,j,t} - \mu_{i,j}}{\sigma_{i,j}}
$$

donde $i$ es la tienda, $j$ la familia de producto, y $\mu_{i,j}$,
$\sigma_{i,j}$ son la media y desviación estándar de las ventas limpias de
esa serie.

El script computa estos parámetros en `compute_scaler_params()` y los aplica
para escalar las ventas antes de calcular los rezagos.  Los parámetros se
persisten por separado en `scaler_params.parquet` porque son necesarios
durante la post-procesamiento para invertir la transformación.

### 3.3 Codificación Categórica de la Familia de Producto

```python
labels, uniques = pd.factorize(train["family"])
```

La función `pd.factorize` asigna un código entero a cada valor único en el
orden de primera aparición.  Es crítico que el script utilice el DataFrame
en el **mismo orden que el cuaderno de entrenamiento** (orden original del
CSV, sin ordenar) para que los códigos coincidan.  Una familia codificada
como `3` durante el entrenamiento debe recibir el mismo código `3` en
producción; de lo contrario, el nodo de decisión del árbol que evalúa
`family_enc <= 3.5` tomaría la rama incorrecta.

La columna resultante se renombra a `family_enc` (en lugar de `family`) para
evitar un conflicto con la columna de índice `family` que
`ParquetDataRepository` excluye de los vectores de características.

### 3.4 Variables de Rezago (Lag Features)

MLForecast se configuró con `lags=[1, 7, 14, 28, 90, 365]`, generando 6
variables que capturan patrones temporales a diferentes escalas:

| Lag | Interpretación |
|-----|----------------|
| 1 | Venta del día anterior (tendencia de corto plazo) |
| 7 | Venta de hace una semana (estacionalidad semanal) |
| 14 | Venta de hace dos semanas |
| 28 | Venta de hace cuatro semanas (estacionalidad mensual) |
| 90 | Venta de hace tres meses (estacionalidad trimestral) |
| 365 | Venta de hace un año (estacionalidad anual) |

Los rezagos se calculan sobre las **ventas escaladas** (`sales_scaled`), no
sobre las ventas crudas, replicando el comportamiento de MLForecast cuando se
utiliza `target_transforms=[LocalStandardScaler()]`.

```python
df[f"lag{lag}"] = df.groupby(["store_nbr", "family"])["sales_scaled"].shift(lag)
```

### 3.5 Transformaciones sobre Rezagos (Lag Transforms)

MLForecast permite aplicar funciones de ventana sobre las columnas de rezago
ya generadas.  El cuaderno configuró:

```python
lag_transforms = {
    1:  [ExpandingMean()],
    7:  [RollingMean(window_size=7), RollingMean(window_size=28), RollingMean(window_size=365)],
    28: [RollingMean(window_size=7), RollingMean(window_size=28), RollingMean(window_size=365)],
}
```

Esto genera 7 columnas adicionales:

| Columna | Definición |
|---------|------------|
| `expanding_mean_lag1` | Media expandida acumulativa de `lag1` |
| `rolling_mean_lag7_window_size7` | Media móvil de 7 días sobre `lag7` |
| `rolling_mean_lag7_window_size28` | Media móvil de 28 días sobre `lag7` |
| `rolling_mean_lag7_window_size365` | Media móvil de 365 días sobre `lag7` |
| `rolling_mean_lag28_window_size7` | Media móvil de 7 días sobre `lag28` |
| `rolling_mean_lag28_window_size28` | Media móvil de 28 días sobre `lag28` |
| `rolling_mean_lag28_window_size365` | Media móvil de 365 días sobre `lag28` |

Estas transformaciones capturan tendencias suavizadas a distintas escalas
temporales y son particularmente valiosas para modelos de *gradient boosting*,
que no tienen memoria temporal intrínseca como las redes recurrentes.

### 3.6 Variables Calendáricas

```python
date_features = ["day_of_week", "is_month_end", "is_month_start"]
```

Tres variables extraídas directamente del timestamp de la fecha:

- `day_of_week`: entero 0-6 (lunes=0, domingo=6), captura estacionalidad
  semanal.
- `is_month_end`: indicador binario (1.0 si es último día del mes), captura
  patrones de consumo de fin de mes.
- `is_month_start`: indicador binario, captura patrones de inicio de mes.

### 3.7 Variables Indicadoras de Feriados

El análisis de correlación realizado en el cuaderno de entrenamiento identificó
11 feriados ecuatorianos con impacto estadísticamente significativo en las
ventas.  Cada uno se codifica como variable binaria (1.0 en la fecha del
feriado, 0.0 en las demás):

| Variable | Evento |
|----------|--------|
| `description_Cantonizacion_de_Salinas` | Cantonización de Salinas |
| `description_Navidad` | Navidad (25 de diciembre) |
| `description_Navidad_1` | Día previo a Navidad |
| `description_Navidad_2` | 2 días antes de Navidad |
| `description_Navidad_3` | 3 días antes de Navidad |
| `description_Navidad_4` | 4 días antes de Navidad |
| `description_Primer_dia_del_ano` | Año Nuevo (1 de enero) |
| `description_Terremoto_Manabi_1` | Día posterior al terremoto de Manabí (2016) |
| `description_Terremoto_Manabi_15` | 15 días después del terremoto |
| `description_Terremoto_Manabi_2` | 2 días después del terremoto |
| `description_Traslado_Primer_dia_del_ano` | Traslado del feriado de Año Nuevo |

Los nombres de las columnas contienen únicamente caracteres válidos para
identificadores de Python (letras, números y guiones bajos).  Los caracteres
especiales presentes en los datos originales (`-` en `Navidad-1`, `+` en
`Terremoto Manabi+1`) fueron sanitizados a `_` para garantizar compatibilidad
con `pandas.DataFrame.itertuples()` y la función `getattr()`, utilizados por
`ParquetDataRepository` para la extracción eficiente de vectores de
características.

Solo se incluyen feriados **no trasladados** (`transferred == False`), ya que
el cuaderno aplica esta misma condición al crear las variables indicadoras.

---

## 4. Vector de Características del Modelo

El modelo ONNX (`TreeEnsembleRegressor`) espera un vector de 30 características
en el siguiente orden estricto, extraído de `lgb_model.feature_name_` tras el
entrenamiento:

| Posición | Nombre | Categoría |
|:--------:|--------|-----------|
| 0 | `onpromotion` | Promoción |
| 1 | `family_enc` | Categórica |
| 2 | `store_nbr_feat` | Identificación |
| 3-13 | `description_*` (11 feriados) | Feriados |
| 14-19 | `lag1`, `lag7`, `lag14`, `lag28`, `lag90`, `lag365` | Rezagos |
| 20 | `expanding_mean_lag1` | Transformación de rezago |
| 21-26 | `rolling_mean_lag*_window_size*` (6 combinaciones) | Transformaciones de rezago |
| 27 | `day_of_week` | Calendárica |
| 28 | `is_month_end` | Calendárica |
| 29 | `is_month_start` | Calendárica |

El script impone este orden exacto mediante la constante `_FEATURE_COLS`, que
se utiliza como lista de selección y ordenamiento de columnas antes de escribir
el archivo Parquet.  Todas las columnas se convierten a `float32` para
coincidir con el tipo de entrada del modelo ONNX.

---

## 5. Estrategia de Búfer de Pronóstico

### 5.1 El Problema de las Fechas Futuras

Los datos de entrenamiento del concurso Kaggle terminan el **15 de agosto de
2017**.  Sin embargo, el sistema de producción necesita generar predicciones
para fechas posteriores.  Dado que las características de rezago y medias
móviles dependen de valores históricos de ventas, no es posible calcularlas
de manera convencional para fechas sin datos observados.

### 5.2 Solución: Forward-Fill de Rezagos

El script implementa una estrategia de **búfer temporal**:

1. Se generan filas sintéticas para los `N` días posteriores al último dato
   de entrenamiento (configurable mediante `--buffer-days`, por defecto 90).
2. Las columnas de rezago y medias móviles se inicializan como `NaN`.
3. Se aplica un *forward-fill* por grupo `(store_nbr, family)`, propagando
   los últimos valores conocidos de cada característica.
4. Las variables calendáricas y de feriados se computan normalmente para las
   fechas del búfer.

Esta aproximación asume que los patrones de rezago recientes son
representativos del comportamiento futuro cercano — una hipótesis razonable
para horizontes de pronóstico cortos (días a semanas), que es el caso de uso
principal del sistema.

### 5.3 Extensión a Fechas Lejanas

Para fechas significativamente posteriores al rango del búfer, el
`ProductionPreprocessor` implementa una estrategia de *clamping*: la fecha
solicitada se sustituye por la última fecha disponible en el Parquet.  Esto
permite que el sistema responda a peticiones de cualquier fecha sin errores,
a costa de una menor precisión en las características calendáricas.  En un
escenario de producción real, esta limitación se resolvería con un pipeline
de datos en tiempo real que ingeste ventas actualizadas.

---

## 6. Período de Calentamiento (Warm-up)

Los primeros registros del dataset (enero de 2013 en adelante) producen
valores `NaN` en los rezagos de largo alcance (`lag90`, `lag365`) porque no
existen suficientes observaciones previas.  El script descarta todas las filas
anteriores al **1 de enero de 2014**, asegurando que cada vector de
características contenga al menos 365 días de historia.  Los `NaN` residuales
(e.g., los primeros días de 2014 que aún carecen de `lag365` completo) se
rellenan con 0.0, la convención adoptada por MLForecast cuando
`min_periods < window_size`.

---

## 7. Flujo de Ejecución

```
┌──────────────────────────────────────────────────────────────────┐
│                  precompute_features.py                          │
│                                                                  │
│  1. load_csvs()                                                  │
│     └── Lee train.csv (~3M filas) y holidays_events.csv          │
│                                                                  │
│  2. compute_family_encoding()                                    │
│     └── pd.factorize(train["family"]) → dict[str, int]          │
│                                                                  │
│  3. compute_scaler_params()                                      │
│     └── groupby(store_nbr, family).agg(mean, std) → DataFrame   │
│                                                                  │
│  4. build_features()                                             │
│     ├── 4a. Limpiar ventas (clip + replace)                      │
│     ├── 4b. Escalar ventas con parámetros del scaler             │
│     ├── 4c. Codificar familia y tienda                           │
│     ├── 4d. Calcular 6 rezagos sobre ventas escaladas            │
│     ├── 4e. Calcular 7 transformaciones de rezagos               │
│     ├── 4f. Agregar 3 variables calendáricas                     │
│     ├── 4g. Agregar 11 variables de feriados                     │
│     ├── 4h. Generar búfer de fechas futuras + forward-fill       │
│     ├── 4i. Descartar período de calentamiento (< 2014-01-01)   │
│     └── 4j. Seleccionar y ordenar las 30 columnas finales        │
│                                                                  │
│  5. Escribir precomputed_features.parquet                        │
│  6. Escribir scaler_params.parquet                               │
└──────────────────────────────────────────────────────────────────┘
```

### Uso

```bash
python scripts/precompute_features.py \
    --data-dir data/ \
    --output-dir data/ \
    --buffer-days 3650 \
    --min-output-date 2025-01-01
```

| Argumento | Descripción | Valor por defecto |
|-----------|-------------|:-----------------:|
| `--data-dir` | Directorio que contiene los CSVs de Kaggle (`train.csv`, `holidays_events.csv`) | `data/` |
| `--output-dir` | Directorio donde se escriben los archivos Parquet | `data/` |
| `--buffer-days` | Días de pronóstico a pre-computar más allá del último dato de entrenamiento | `3650` (~10 años, cubre hasta ~2027) |
| `--min-output-date` | Fecha mínima a incluir en el Parquet de salida (YYYY-MM-DD). La historia completa se usa para el cómputo de lags; solo las filas ≥ esta fecha se escriben en disco. | `2025-01-01` |

---

## 8. Integración en la Arquitectura de Producción

El script `precompute_features.py` opera como un proceso **offline** (batch)
que se ejecuta una única vez antes del despliegue.  Sus artefactos se integran
en la arquitectura de producción de la siguiente manera:

```
     Offline (una vez)                         Online (por petición)
┌─────────────────────┐               ┌─────────────────────────────────┐
│  train.csv          │               │  Petición HTTP / MCP            │
│  holidays_events.csv│               │  (store, family, fecha_inicio,  │
│         │           │               │   fecha_fin)                    │
│         ▼           │               │         │                       │
│  precompute_        │               │         ▼                       │
│  features.py        │               │  ProductionPreprocessor         │
│         │           │               │  ┌──────────────────────────┐   │
│         ├──► precomputed_features   │  │ Para cada fecha:         │   │
│         │    .parquet ──────────────────► get_feature_vector()    │   │
│         │                           │  │ → lookup O(1) en dict    │   │
│         └──► scaler_params          │  └──────────────────────────┘   │
│              .parquet ──────────┐   │         │                       │
│                                │   │         ▼                       │
└────────────────────────────────┘   │  ONNXModel.predict()            │
                                 │   │  (30 features → predicción)     │
                                 │   │         │                       │
                                 │   │         ▼                       │
                                 └────► ProductionPostprocessor        │
                                     │  (des-escalar: pred*σ + μ)      │
                                     │         │                       │
                                     │         ▼                       │
                                     │  Respuesta: unidades de venta   │
                                     └─────────────────────────────────┘
```

### 8.1 Componentes del Servidor que Consumen los Artefactos

| Componente | Artefacto consumido | Función |
|---|---|---|
| `ParquetDataRepository` | `precomputed_features.parquet` | Carga el Parquet al iniciar el servidor y construye un índice en memoria `dict[(store, family, date)] → list[float]` para consultas O(1) |
| `ProductionPreprocessor` | (vía `ParquetDataRepository`) | Para cada fecha del horizonte de pronóstico, obtiene el vector de 30 características pre-computadas |
| `ProductionPostprocessor` | `scaler_params.parquet` | Obtiene `(μ, σ)` de la serie para invertir la estandarización: `predicción_real = predicción_escalada × σ + μ` |

### 8.2 Configuración de Despliegue

Los artefactos se montan como volúmenes de solo lectura en Docker:

```yaml
# docker-compose.yml (fragmento)
prediction_server:
  environment:
    PREPROCESSOR_BACKEND: production
    DATA_PATH: data/precomputed_features.parquet
    SCALER_PATH: data/scaler_params.parquet
  volumes:
    - ${DATA_ARTIFACTS_PATH:-./data}:/app/data:ro
```

---

## 9. Garantías de Consistencia

El script implementa varias salvaguardas para garantizar la consistencia
entre entrenamiento y producción:

| Salvaguarda | Implementación | Riesgo mitigado |
|---|---|---|
| **Orden de columnas explícito** | Constante `_FEATURE_COLS` con las 30 columnas en el orden exacto de `lgb_model.feature_name_` | Skew de orden |
| **Misma limpieza de datos** | `clip(lower=0).replace(0, 0.01)` idéntico al cuaderno | Skew de distribución |
| **Misma codificación categórica** | `pd.factorize` sobre el DataFrame en orden original del CSV | Códigos divergentes |
| **Rezagos sobre ventas escaladas** | Los rezagos se computan después de aplicar `LocalStandardScaler`, no antes | Skew de escala |
| **Parámetros del scaler persistidos** | `scaler_params.parquet` contiene `(μ, σ)` computados con la misma limpieza | Inversión incorrecta de la predicción |
| **Tipo de dato uniforme** | Todas las características se convierten a `float32` | Errores de tipo en ONNX Runtime |
| **Sanitización de nombres** | Caracteres `-` y `+` → `_` en nombres de columnas de feriados | Incompatibilidad con `itertuples`/`getattr` |

---

## 10. Limitaciones y Trabajo Futuro

1. **Dataset estático:** El pipeline asume datos de entrenamiento inmutables.
   En un sistema de producción real, sería necesario un pipeline de datos
   incremental que incorpore nuevas ventas y regenere las características
   periódicamente.

2. **Forward-fill para fechas futuras:** La propagación de los últimos
   valores conocidos de rezagos es una aproximación que pierde precisión
   conforme el horizonte de pronóstico se aleja de los datos observados.
   Un enfoque recursivo (donde la predicción del día *t* alimenta el rezago
   del día *t+1*) mejoraría la calidad pero requeriría modificar el flujo
   de inferencia.

3. **Volumen del artefacto y consumo de RAM:** El `ParquetDataRepository`
   construye al iniciar el servidor un diccionario Python en memoria con todas
   las filas del Parquet.  Sin filtrado, el artefacto completo (2014-2017 +
   búfer) contiene ~2.5 millones de filas y expande a ~800 MB por proceso
   uvicorn.  Con múltiples workers, el consumo se multiplica
   proporcionalmente.  Esta limitación se abordó mediante el argumento
   `--min-output-date`, que restringe el output al rango de fechas
   relevante para el sistema en producción (ver Sección 12).

4. **Ausencia de validación cruzada en producción:** El script no verifica
   que las predicciones generadas con los artefactos coincidan con las del
   cuaderno de entrenamiento.  Un test de regresión que compare predicciones
   para un subconjunto de fechas conocidas fortalecería la garantía de
   consistencia.

---

## 11. Relación con los Objetivos del Trabajo de Titulación

Este componente contribuye directamente a los siguientes aspectos del trabajo
de titulación:

- **Despliegue de modelos de ML en producción:** Demuestra cómo se
  operacionaliza un modelo entrenado en un cuaderno Jupyter hacia un servicio
  REST contenedorizado, abordando el desafío práctico de la ingeniería de
  características en producción.

- **Arquitectura limpia y separación de responsabilidades:** El pre-cómputo
  offline desacopla la lógica de transformación de datos del flujo de
  inferencia en tiempo real, respetando el principio de responsabilidad única.

- **Reproducibilidad científica:** La replicación exacta del pipeline de
  entrenamiento, documentada en código y en este documento, permite que
  cualquier evaluador reproduzca los resultados partiendo de los mismos datos
  de entrada.

- **Trazabilidad del pipeline de datos:** Los artefactos Parquet actúan como
  un contrato verificable entre la fase de entrenamiento y la de producción,
  facilitando la auditoría del sistema.

---

## 12. Incidencias de Despliegue y Soluciones Aplicadas

Esta sección registra los problemas encontrados durante el despliegue del
sistema en producción y las decisiones técnicas adoptadas para resolverlos.
Su inclusión tiene valor académico como evidencia del proceso iterativo
inherente a la ingeniería de software aplicada a sistemas de ML.

---

### 12.1 OOM al Iniciar el Servidor — Ciclo de Reinicios Continuos

**Fecha:** 2026-03-18

**Síntoma observado:**

Los logs del contenedor `prediction_server` mostraban un patrón de sierra
repetitivo: el servidor cargaba los archivos Parquet, el proceso hijo moría
silenciosamente, y el ciclo se reiniciaba sin llegar nunca a
`Application startup complete`:

```
INFO:  Started server process [1]
INFO:  Waiting for application startup.
INFO:  Loading features from /app/data/precomputed_features.parquet
INFO:  Loading scaler params from /app/data/scaler_params.parquet
INFO:  Child process [1016] died
INFO:  Started server process [1084]
INFO:  Waiting for application startup.
INFO:  Loading features from /app/data/precomputed_features.parquet
...
```

Las métricas de Docker (`docker stats`) confirmaron una curva de RAM en
diente de sierra que alcanzaba el límite disponible antes de caer a cero,
indicando que el proceso era terminado por el OOM killer del kernel Linux.

**Causa raíz:**

El `ParquetDataRepository` construye al inicio un diccionario Python de la
forma `dict[(store_nbr, family, date) → list[float]]` con la totalidad de
las filas del Parquet.  El Parquet original cubría el período 2014-2017 más
el búfer de 90 días, resultando en aproximadamente:

```
54 tiendas × 33 familias × 1.490 días ≈ 2,65 millones de filas
```

Cada entrada del diccionario requiere del orden de 300-400 bytes en memoria
Python (overhead del objeto `tuple` como clave, `list` de 30 `float`, tabla
hash interna del `dict`), lo que totaliza aproximadamente **800 MB por
proceso uvicorn**.  El `Dockerfile` configuraba **dos workers** uvicorn, cada
uno cargando su propia copia independiente del diccionario, elevando el
consumo real a ~1,6 GB — superando la memoria disponible para el contenedor
en el entorno de despliegue con Docker Desktop, donde los recursos son
compartidos con los múltiples servicios del stack Onyx (≥10 GB requeridos).

**Solución aplicada — dos cambios en paralelo:**

**a) Reducción de workers uvicorn a 1** (`Dockerfile`):

FastAPI opera sobre el event loop asíncrono de asyncio, lo que le permite
atender múltiples peticiones concurrentes desde un único proceso sin bloqueo.
Para un servidor de inferencia con I/O asíncrono y cómputo ONNX de corta
duración, un solo worker es suficiente y elimina la duplicación de memoria:

```dockerfile
# Antes
CMD ["uvicorn", "server.interface.http.api:app",
     "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

# Después
CMD ["uvicorn", "server.interface.http.api:app",
     "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

**b) Filtrado del Parquet por fecha de salida** (`--min-output-date`):

Se añadió el argumento `--min-output-date` al script de pre-cómputo.  La
historia completa sigue siendo necesaria para computar correctamente los
rezagos (e.g., `lag365` requiere 365 días de antecedentes), por lo que el
pipeline interno no se modifica.  El filtrado se aplica únicamente al momento
de escribir el Parquet final en disco:

```python
# Aplicado después de build_features(), antes de to_parquet()
min_output_date = pd.Timestamp(args.min_output_date)
features = features[features["date"] >= min_output_date].copy()
```

Con `--min-output-date 2025-01-01` y `--buffer-days 3650`, el Parquet
resultante cubre el rango 2025-01-01 a ~2027-08, reduciendo las filas de
~2.65 millones a ~650.000 (~75% de reducción) y el consumo de RAM en el
servidor de ~800 MB a ~200 MB.

**Resultado de la comparación antes/después:**

| Métrica | Configuración original | Configuración optimizada |
|---------|----------------------|--------------------------|
| Filas en Parquet | ~2,65 millones | ~650.000 |
| Tamaño en disco | ~80 MB | ~20 MB |
| RAM por worker uvicorn | ~800 MB | ~200 MB |
| Workers uvicorn | 2 | 1 |
| RAM total del servidor | ~1.600 MB | ~200 MB |
| Resultado al iniciar | OOM → crash loop | Startup exitoso (~30 s) |

**Lección aprendida:**

La estrategia de indexación en memoria del `ParquetDataRepository` (O(1) por
consulta) presenta una disyuntiva clásica de espacio-tiempo: maximiza la
velocidad de inferencia a costa de memoria proporcional al tamaño del
dataset.  En entornos con restricciones de memoria, la reducción del rango
temporal del Parquet de salida es el mecanismo de control más directo, ya
que la precisión del cómputo de rezagos no se ve afectada.

---

### 12.2 Error de Conexión MCP por Servidor No Disponible

**Fecha:** 2026-03-18

**Síntoma observado:**

El servidor Onyx (`api_server`) reportaba el siguiente error al intentar
invocar la herramienta `predict_stock`:

```
ERROR: mcp_client.py: Failed to call MCP client function:
       unhandled errors in a TaskGroup (1 sub-exception)
ERROR: mcp_client.py: All connection attempts failed
ERROR: mcp_tool.py: Failed to execute MCP tool 'predict_stock':
       All connection attempts failed
```

**Causa raíz:**

El error era una consecuencia directa del crash loop descrito en la
Sección 12.1.  El contenedor `prediction_server` nunca completaba su
secuencia de inicio (`Application startup complete`) y por lo tanto no
aceptaba conexiones en el puerto 8000.  El cliente MCP de Onyx intentaba
conectarse a `http://prediction-server.local:8000/mcp` y fallaba al no
encontrar un socket TCP activo.

Adicionalmente, el `start_period` del healthcheck en `docker-compose.yml`
estaba configurado en 15 segundos, insuficiente para dar tiempo al servidor
de completar la carga del Parquet antes de que Docker comenzara a registrar
fallos de salud.

**Solución aplicada:**

La solución principal fue la descrita en la Sección 12.1.  Como medida
complementaria, se aumentó el `start_period` del healthcheck de 15 a 90
segundos para dar margen a la carga del Parquet en el inicio del servidor:

```yaml
# docker-compose.yml — healthcheck del prediction_server
healthcheck:
  interval: 30s
  timeout: 5s
  start_period: 90s   # antes: 15s
  retries: 3
```

**Resultado:** Una vez que el servidor de predicción completa su inicio
exitosamente, el error de conexión MCP desaparece en el siguiente intento
del agente Onyx, sin requerir ningún cambio adicional en la configuración
de la integración.

---

## Referencias

- Sculley, D., Holt, G., Golovin, D., et al. (2015). *Hidden Technical Debt
  in Machine Learning Systems.* Advances in Neural Information Processing
  Systems (NeurIPS), 28.
- Breck, E., Cai, S., Nielsen, E., Salib, M., & Sculley, D. (2019). *The ML
  Test Score: A Rubric for ML Production Readiness and Technical Debt
  Reduction.* Proceedings of the IEEE International Conference on Big Data.
- Nixtla (2024). *MLForecast: Scalable Machine Learning for Time Series.*
  Documentación oficial. https://nixtla.github.io/mlforecast/
- Ke, G., Meng, Q., Finley, T., et al. (2017). *LightGBM: A Highly Efficient
  Gradient Boosting Decision Tree.* Advances in Neural Information Processing
  Systems (NeurIPS), 30.
- ONNX Runtime Contributors (2024). *ONNX Runtime: Cross-platform, High
  Performance ML Inferencing and Training Accelerator.* https://onnxruntime.ai/
