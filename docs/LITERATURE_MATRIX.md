# Matriz de literatura para estado del arte

Objetivo: conectar la bibliografia minima disponible con usos concretos dentro del capitulo de estado del arte y conceptos teoricos, sin inflar afirmaciones ni mezclar soporte conceptual con evidencia empirica propia del repositorio.

Criterio de uso:
- solo fuentes primarias o documentacion oficial;
- cada fila indica que puede sostener y que no;
- esta matriz no reemplaza la redaccion del capitulo, sino que evita citas decorativas o mal ubicadas.

## Matriz principal

| Tema del capitulo | Fuente | Tipo | Aporte verificable | Afirmaciones que puede sostener | Relacion con el repo | Limites de uso |
|---|---|---|---|---|---|---|
| Forecasting minorista y demanda | `Fildes, Ma y Kolassa (2022)` | Articulo de revista | Sintetiza problemas y practicas de retail forecasting | Relevancia del forecasting en retail y tension entre investigacion y practica | Justifica por que el caso de supermercado es pertinente como problema aplicado | No usar para afirmar resultados del proyecto ni para describir la arquitectura implementada |
| Forecasting minorista y cierre critico | `Fildes, Kolassa y Ma (2022)` | Post-script / articulo corto | Complementa y actualiza el balance sobre forecasting minorista | Puede sostener un cierre critico sobre brechas persistentes entre practica y evaluacion | Ayuda a posicionar el trabajo como caso aplicado con restricciones reales | No reemplaza una revision sistematica amplia |
| Dias especiales y calendario en retail | `Huber y Stuckenschmidt (2020)` | Articulo de revista | Estudia demanda retail diaria con enfasis en dias especiales de calendario | Uso relevante de senales calendarias y dias especiales en forecasting retail | Refuerza la inclusion de feriados, calendario y promociones en la metodologia | No justifica por si sola el criterio exacto de seleccion de feriados usado en el repo |
| Modelos globales para multiples series | `Hewamalage, Bergmeir y Bandara (2020)` | Preprint academico | Discute modelos globales para forecasting de multiples series | Puede sostener la pertinencia conceptual de modelos globales en entornos multiserie | Se alinea con el uso de `MLForecast` y `LightGBM` sobre 1782 series | Al ser preprint, conviene usarlo junto con otra fuente consolidada |
| Localidad vs globalidad en grupos de series | `Montero-Manso y Hyndman (2021)` | Articulo de revista | Formaliza principios para forecasting de grupos de series y discute globalidad/localidad | Puede sostener la discusion teorica sobre por que un enfoque global es razonable | Refuerza el enfoque de modelado conjunto observado en notebooks | No justifica parametros especificos del modelo final |
| Algoritmo base del modelo | `Ke et al. (2017)` | Paper de conferencia | Presenta LightGBM como algoritmo de gradient boosting eficiente | Puede sostener la descripcion tecnica del algoritmo elegido | Ayuda a fundamentar la eleccion de `LGBMRegressor` como base del modelo | No permite afirmar que LightGBM sea optimo para este caso sin comparaciones propias |
| Deuda tecnica en sistemas ML | `Sculley et al. (2015)` | Paper de conferencia | Describe riesgos de deuda tecnica en sistemas de machine learning | Puede sostener la necesidad de separar entrenamiento, serving y artefactos | Dialoga con la arquitectura de serving, precomputo de features y cuidado de consistencia | No valida la arquitectura concreta del repo por si misma |
| Readiness productiva de sistemas ML | `Breck et al. (2017)` | Paper / rubrica industrial | Propone criterios de readiness y reduccion de deuda tecnica | Puede sostener la importancia de pruebas, contratos y validacion operativa | Refuerza la seccion de validacion tecnica y reproducibilidad | No sustituye evidencia de pruebas realmente ejecutadas en este repo |
| Framework de forecasting con features | `MLForecast Documentation` | Documentacion oficial | Describe abstracciones, API y enfoque de `MLForecast` | Puede sostener la descripcion operacional de la libreria usada | Conecta directamente con el notebook y la metodologia implementada | Es documentacion tecnica, no literatura academica de estado del arte por si sola |
| Ecosistema Nixtla para forecasting | `Nixtla tutorial: Statistical, Machine Learning and Neural Forecasting methods` | Tutorial oficial | Muestra posicionamiento del enfoque dentro del ecosistema Nixtla | Puede apoyar explicaciones instrumentales y de contexto de herramientas | Ayuda a explicar por que el proyecto usa herramientas de forecasting modernas | No debe usarse como prueba empirica ni como fuente teorica principal |
| Interoperabilidad de modelos | `ONNX Overview` | Documentacion oficial | Define el objetivo y alcance general de ONNX | Puede sostener la descripcion de ONNX como formato portable para modelos | Refuerza la decision de exportar el modelo para serving | No justifica por si sola la superioridad del stack elegido |

## Cobertura por subseccion sugerida

| Subseccion de `2.2.2` | Fuentes base sugeridas | Uso recomendado |
|---|---|---|
| Prediccion de demanda y problema de reposicion | `Fildes et al. (2022)`, `Fildes et al. (2022, post-script)`, `Huber y Stuckenschmidt (2020)` | Contextualizar relevancia del problema y variables de calendario en retail |
| Series temporales multiserie y modelos globales | `Hewamalage et al. (2020)`, `Montero-Manso y Hyndman (2021)`, `MLForecast Documentation` | Definir el enfoque global y vincularlo con la solucion implementada |
| Algoritmo base y pipeline de features | `Ke et al. (2017)`, `MLForecast Documentation` | Describir el rol de LightGBM y de la ingenieria de variables temporales |
| Consistencia entre entrenamiento e inferencia | `Sculley et al. (2015)`, `Breck et al. (2017)` | Justificar por que la tesis incorpora arquitectura, pruebas y serving, no solo entrenamiento |
| Exportacion e interoperabilidad | `ONNX Overview` | Sustentar el uso de ONNX en la seccion conceptual y de implementacion |

## Vacios que la matriz no resuelve

1. No reemplaza una revision bibliografica exhaustiva ni sistematica.
2. No incorpora aun literatura especifica de inventarios, politicas de reposicion o stock de seguridad.
3. No define el estilo final de citacion exigido por la institucion.
4. No resuelve el vacio cuantitativo del capitulo de experimentos.
