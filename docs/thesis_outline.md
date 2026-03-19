# Propuesta de índice integral de tesis

Este índice integra dos fuentes:

1. La evidencia real disponible en el repositorio.
2. La estructura exigida o sugerida por:
   - `C:/Users/juana/Downloads/Pautas para tesis - MCD24.docx`
   - `C:/Users/juana/Downloads/Guía Elaboración Tesinas (1).pdf`

Objetivo: que no falte ninguna sección relevante al momento de redactar la tesis en Markdown.

## 0. Criterio de organización

- `Obligatoria`: aparece como parte de la estructura esperada en las pautas.
- `Opcional`: la guía la marca como opcional o condicional.
- `Con evidencia suficiente`: el repositorio ya ofrece insumos directos para redactar.
- `Con evidencia parcial`: hay insumos, pero faltan definiciones, resultados o referencias para cerrar la redacción.
- `Sólido`: ya existe base documental suficiente y, en algunos casos, borrador inicial utilizable.
- `Parcial`: existe base documental útil, pero hay vacíos que impedirían cerrar una versión final sin trabajo adicional.
- `Pendiente`: la sección está identificada en la estructura, pero todavía no cuenta con base suficiente o no se ha consolidado su soporte documental.
- La numeración global vigente del manuscrito quedó consolidada en [MANUSCRIPT_NUMBERING.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/MANUSCRIPT_NUMBERING.md).

## 0.1 Estado documental actual por sección

| Sección | Estado documental | Base actual | Bloqueo principal |
|---|---|---|---|
| `1.1 Portada` | Pendiente | Solo pauta institucional | Faltan datos formales finales de presentación |
| `1.2 Página de aprobación` | Pendiente | Solo guía institucional | Depende de formato y aprobación institucional |
| `1.3 Fe de erratas` | Pendiente | Solo guía institucional | Se activa solo si corresponde al cierre |
| `1.4 Descargo de responsabilidad` | Pendiente | Solo guía institucional | Falta redacción formal institucional |
| `1.5 Dedicatoria y agradecimientos` | Pendiente | No técnica | Depende de decisión editorial final |
| `1.6 Cláusula de confidencialidad` | Pendiente | No parece necesaria por datos públicos | Confirmar si aplica institucionalmente |
| `1.7 Tabla de contenido o índice` | Parcial | Estructura ya definida | Se consolida al cierre del manuscrito |
| `1.8 Lista de tablas` | Parcial | Ya existe [LISTA_DE_TABLAS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LISTA_DE_TABLAS.md) con la tabla actualmente integrada en el manuscrito | Debe ampliarse si luego se incorporan nuevas tablas al cuerpo de la tesis |
| `1.9 Lista de figuras` | Parcial | Ya existe [LISTA_DE_FIGURAS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LISTA_DE_FIGURAS.md) con `Figura 1` a `Figura 6` | Falta completar con figuras de resultados si luego se incorporan al manuscrito |
| `1.10 Lista de abreviaturas y siglas` | Parcial | Ya existe [ABREVIATURAS_SIGLAS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/ABREVIATURAS_SIGLAS.md) con siglas usadas en el manuscrito | Conviene revisarla al cierre por si ingresan nuevas siglas o cambia el criterio editorial |
| `1.11 Lista de símbolos` | Pendiente | No requerida aún | Depende de nivel de formalización matemática |
| `1.12 Glosario` | Parcial | Ya existe [GLOSARIO_MINIMO.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/GLOSARIO_MINIMO.md) con términos operativos del manuscrito | Puede requerir ampliación si el documento final incorpora conceptos nuevos o mayor formalización |
| `1.13 Resumen` | Parcial | Ya existe [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md) con síntesis del problema, método, resultados parciales y limitaciones | Sigue condicionado por el cierre experimental incompleto del modelo principal |
| `1.14 Palabras clave` | Parcial | Ya existe [PALABRAS_CLAVE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/PALABRAS_CLAVE.md) y [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md) ya incluye una propuesta | Conviene validar la lista final cuando quede cerrada la terminología dominante del manuscrito |
| `2.1 Introducción` | Parcial | Ya existe [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md) | Hipótesis y objetivos aún inferidos |
| `2.2.1 Contexto del problema y caso de negocio` | Parcial | Base documental suficiente | Falta convertir el valor operativo esperado en criterios o indicadores de negocio más formales |
| `2.2.2 Conceptos teóricos y estado del arte` | Parcial | Ya existen [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md), [BIBLIOGRAPHY_SEED.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/BIBLIOGRAPHY_SEED.md), [LITERATURE_MATRIX.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LITERATURE_MATRIX.md), [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib) y [CITATION_STYLE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/CITATION_STYLE.md) | Falta ampliar comparacion sistematica con literatura previa y cubrir mejor inventarios/reposicion |
| `2.2.3 Metodología` | Parcial | Ya existe [metodologia.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/metodologia.md) | Faltan justificaciones metodológicas más fuertes en algunos puntos |
| `2.2.4 Análisis exploratorio de datos (EDA)` | Sólido | Ya existe [eda.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/eda.md), con cinco figuras exportadas, numeradas e integradas en el cuerpo base del capítulo | Solo resta ajustar numeración final y referencias cruzadas cuando se consolide el manuscrito completo; la segmentación adicional es opcional |
| `2.2.5 Arquitectura e implementación del sistema` | Sólido | Ya existe [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md), junto con una figura de arquitectura vigente exportada | Conviene seguir separando documentación legacy de arquitectura actual y decidir si se añadirá un diagrama interno más detallado |
| `2.2.6 Experimentos` | Parcial | Ya existe [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md) con protocolo experimental, baselines trazables, `RMSLE` visible de `LightGBM`, evidencia de ejecución y artefacto `submission.csv` | Falta cerrar comparación equivalente contra baselines con `MAE`, `RMSE` y/o un `cv_results_lgbm` exportado; el alcance documentado hoy tampoco es completamente homogéneo entre baseline y modelo principal |
| `2.2.7 Validación técnica y reproducibilidad` | Sólido | Ya existe [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md) y la evidencia técnica está trazada en tests, CI, smoke tests y guías E2E | No hay corrida local reejecutada en este entorno y falta evidencia archivada de una corrida productiva completa con Onyx |
| `2.3 Conclusiones` | Parcial | Ya existe [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md) con síntesis prudente de hallazgos, limitaciones y trabajo futuro | Sigue condicionada por el cierre experimental incompleto del modelo principal |
| `3.1 Referencias bibliográficas` | Parcial | Ya existe [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib) y [BIBLIOGRAPHY_SEED.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/BIBLIOGRAPHY_SEED.md) | Falta definir set final efectivamente citado y revisar estilo institucional |
| `3.2 Bibliografía consultada` | Parcial | Ya existen [BIBLIOGRAPHY_SEED.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/BIBLIOGRAPHY_SEED.md) y [LITERATURE_MATRIX.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LITERATURE_MATRIX.md) | Falta decidir si la institución exige separación entre consultada y citada |
| `3.3 Estilo de citas y referencias` | Parcial | Ya existe [CITATION_STYLE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/CITATION_STYLE.md) con convención autor-año y reglas operativas para Markdown y BibTeX | Falta validar si la dirección o la unidad académica exige un estilo distinto en la versión final maquetada |
| `4.1 Anexos` | Parcial | Ya existen [LISTA_DE_ANEXOS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LISTA_DE_ANEXOS.md) y [anexo_reproducibilidad_operativa.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/anexo_reproducibilidad_operativa.md) como base concreta | Falta decidir qué anexos candidatos entrarán efectivamente y fijar la numeración final |
| `4.2 Repositorio de soporte` | Sólido | El repositorio ya cumple este rol | Requiere solo referencia ordenada desde el manuscrito |
| `5. Orden de redacción recomendado` | Parcial | Existe propuesta funcional | Debe actualizarse cuando se destraben resultados |
| `6. Riesgos de completitud todavía abiertos` | Parcial | Riesgos ya identificados | Requiere sincronización periódica con el estado documental real |

## 1. Elementos preliminares

### 1.1 Portada

- Estado: obligatoria.
- Debe incluir:
  logo institucional, programa, título, autor/es, tutor, lugar y fecha.
- Fuente normativa:
  `Pautas para tesis - MCD24.docx`.
- Evidencia disponible en repo:
  parcial.
- Vacío:
  faltan datos finales de título formal, tutor, lugar/fecha definitiva y criterios institucionales de formato visual.

### 1.2 Página de aprobación

- Estado: obligatoria según la guía general de tesinas.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Evidencia disponible en repo:
  no aplica como contenido técnico; depende del formato institucional.

### 1.3 Fe de erratas

- Estado: opcional.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.

### 1.4 Descargo de responsabilidad

- Estado: obligatoria según la guía general de tesinas.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.

### 1.5 Dedicatoria y agradecimientos

- Estado: opcional o recomendada.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.

### 1.6 Cláusula de confidencialidad

- Estado: opcional, si corresponde.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Observación:
  relevante solo si se usan datos empresariales con restricciones; en este repo la base principal es pública.

### 1.7 Tabla de contenido o índice

- Estado: obligatoria.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.

### 1.8 Lista de tablas

- Estado: opcional.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Recomendación:
  probablemente convenga incluirla si se formalizan tablas de métricas, features y artefactos.
- Base actual:
  [LISTA_DE_TABLAS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LISTA_DE_TABLAS.md).
- Vacío:
  hoy solo hay una tabla integrada en el cuerpo principal; la lista deberá crecer si se agregan tablas metodológicas, de resultados o de anexos.

### 1.9 Lista de figuras

- Estado: opcional.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Recomendación:
  útil si se incorporan diagramas de arquitectura, flujo de serving y figuras EDA.

### 1.10 Lista de abreviaturas y siglas

- Estado: opcional.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Recomendación:
  útil por la cantidad de términos técnicos (`ONNX`, `MCP`, `EDA`, `MLForecast`, `API`, `CI/CD`).
- Base actual:
  [ABREVIATURAS_SIGLAS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/ABREVIATURAS_SIGLAS.md).
- Vacío:
  revisar al cierre si ingresan nuevas siglas o si la maquetación final exige otro criterio de presentación.

### 1.11 Lista de símbolos

- Estado: opcional.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Observación:
  solo necesaria si se formaliza notación matemática de métricas, escalado o funciones objetivo.

### 1.12 Glosario

- Estado: opcional.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Recomendación:
  puede ayudar si se desea distinguir terminología de negocio y de modelado.
- Base actual:
  [GLOSARIO_MINIMO.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/GLOSARIO_MINIMO.md).
- Vacío:
  sigue siendo un glosario mínimo; puede requerir ampliación si crece el aparato conceptual del manuscrito.

### 1.13 Resumen

- Estado: obligatoria.
- Fuente normativa:
  `Pautas para tesis - MCD24.docx`, `Guía Elaboración Tesinas (1).pdf`.
- Requisito:
  entre 150 y 300 palabras.
- Evidencia disponible:
  parcial.
- Insumos del repo:
  [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md), [README.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/README.md), [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [EVIDENCE_MAP.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/EVIDENCE_MAP.md).
- Vacío:
  el texto ya existe, pero sigue condicionado por la falta de un artefacto final completamente homogéneo y trazable del modelo principal.

### 1.14 Palabras clave

- Estado: obligatoria.
- Fuente normativa:
  `Pautas para tesis - MCD24.docx`, `Guía Elaboración Tesinas (1).pdf`.
- Base actual:
  [PALABRAS_CLAVE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/PALABRAS_CLAVE.md), [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md).
- Vacío:
  validar al cierre si conviene mantener la lista principal o la variante breve según el formato final exigido.

## 2. Cuerpo del trabajo

### 2.1 Introducción

- Estado: obligatoria.
- Según pauta debe contener:
  presentación del problema de negocio, relevancia, motivación, antecedentes, objetivos generales e hipótesis, y metodología utilizada para alcanzar los objetivos.
- Evidencia disponible:
  parcial, pero suficiente para un primer borrador honesto.
- Fuentes base:
  [EVIDENCE_MAP.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/EVIDENCE_MAP.md), [NOTEBOOKS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/NOTEBOOKS.md), [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [README.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/README.md), [Tesis Maestría Ciencia de Datos Levy Gossweiler.docx](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/Tesis%20Maestr%C3%ADa%20Ciencia%20de%20Datos%20Levy%20Gossweiler.docx).
- Vacío:
  debe explicitarse con cuidado la hipótesis o, si no está formulada formalmente, declararla como pendiente o inferida.

### 2.2 Exposición sistemática del trabajo de investigación

- Estado: obligatoria según la guía general.
- En esta tesis conviene desagregarla en capítulos temáticos.

#### 2.2.1 Contexto del problema y caso de negocio

- Estado:
  obligatoria dentro del desarrollo, aunque no siempre separada en la pauta.
- Contenido:
  descripción del problema aplicado, relevancia operativa, alcance y restricciones.
- Evidencia:
  parcial.
- Fuentes:
  [README.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/README.md), [EVIDENCE_MAP.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/EVIDENCE_MAP.md), notebook académico, [Tesis Maestría Ciencia de Datos Levy Gossweiler.docx](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/Tesis%20Maestr%C3%ADa%20Ciencia%20de%20Datos%20Levy%20Gossweiler.docx).

#### 2.2.2 Conceptos teóricos y estado del arte

- Estado: obligatoria en las pautas MCD.
- Contenido:
  literatura sobre el problema de negocio y fundamentos teóricos de las técnicas utilizadas.
- Evidencia:
  parcial.
- Fuentes:
  [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md), [BIBLIOGRAPHY_SEED.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/BIBLIOGRAPHY_SEED.md), [LITERATURE_MATRIX.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LITERATURE_MATRIX.md), [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib), [precompute_features_pipeline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/precompute_features_pipeline.md), [data_serving_architecture.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/data_serving_architecture.md), [onyx_integration.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/onyx_integration.md), [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md), [metodologia.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/metodologia.md), [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md).
- Vacío:
  ya existe una base bibliográfica mínima con citas integradas en el capítulo, pero falta ampliar la comparación sistemática con literatura previa y cubrir mejor inventarios/reposición.

#### 2.2.3 Metodología

- Estado: obligatoria.
- La pauta exige:
  descripción detallada y justificada de técnicas y herramientas.
- Evidencia:
  suficiente para un borrador técnico fuerte.
- Subbloques recomendados:
  - datos y origen;
  - preparación y limpieza;
  - ingeniería de características;
  - selección y configuración del modelo;
  - exportación a ONNX;
  - serving e integración en arquitectura de producción.
- Fuentes:
  [scripts/precompute_features.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/scripts/precompute_features.py), [Global_Simple_LightGBM_Timeseries_Forecast_Final_academic.ipynb](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/Global_Simple_LightGBM_Timeseries_Forecast_Final_academic.ipynb), [precompute_features_pipeline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/precompute_features_pipeline.md), [data_serving_architecture.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/data_serving_architecture.md), [NOTEBOOKS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/NOTEBOOKS.md).

#### 2.2.4 Análisis exploratorio de datos (EDA)

- Estado: obligatoria en las pautas MCD.
- Contenido:
  datos disponibles, descripción estadística inicial, hallazgos exploratorios y soporte visual.
- Evidencia:
  suficiente.
- Fuentes:
  notebook académico, notebook exploratorio, [NOTEBOOKS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/NOTEBOOKS.md), [eda_01_sales_covariates.png](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/figures/eda/eda_01_sales_covariates.png), [eda_02_national_holidays.png](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/figures/eda/eda_02_national_holidays.png), [eda_03_regional_holidays.png](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/figures/eda/eda_03_regional_holidays.png), [eda_04_local_holidays.png](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/figures/eda/eda_04_local_holidays.png), [eda_05_calendar_patterns.png](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/figures/eda/eda_05_calendar_patterns.png).
- Vacío:
  la base visual ya está integrada; solo resta ajustar la numeración y las referencias cruzadas definitivas cuando se cierre el manuscrito completo. La segmentación adicional por tienda o familia queda como mejora opcional, no como bloqueo.

#### 2.2.5 Arquitectura e implementación del sistema

- Estado:
  no nombrada así en las pautas, pero necesaria para una tesis aplicada con repositorio y despliegue.
- Contenido:
  Clean Architecture, capas del sistema, API REST, MCP, ONNX, Onyx y despliegue dockerizado.
- Evidencia:
  suficiente.
- Fuentes:
  [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md), [architecture_01_current_system.svg](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/figures/architecture/architecture_01_current_system.svg), [README.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/README.md), [api.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/interface/http/api.py), [docker-compose.yml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docker-compose.yml), [Dockerfile](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/Dockerfile), [ONNX_INTEGRATION_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/ONNX_INTEGRATION_SUMMARY.md), [.docs/onyx_integration.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/onyx_integration.md), [.docs/data_serving_architecture.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/data_serving_architecture.md).
- Vacío:
  la base visual ya existe; resta decidir si se incorporará además un diagrama complementario más detallado del pipeline interno.

#### 2.2.6 Experimentos

- Estado: obligatoria en las pautas MCD.
- Contenido:
  diseño experimental, validación temporal, baselines, métrica de selección, resultados y comparación.
- Evidencia:
  parcial.
- Fuentes:
  notebook académico, [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [LGBM_CV_EVIDENCE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LGBM_CV_EVIDENCE.md), [cv_results_baseline_retrained.csv](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/cv_results_baseline_retrained.csv), [submission.csv](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/submission.csv).
- Vacío:
  el `RMSLE` de LGBM ya queda visible, pero faltan `MAE`, `RMSE` y una tabla de CV exportada para comparación equivalente contra baselines; además, la comparación hoy documentada no está cerrada sobre exactamente el mismo conjunto de series.

#### 2.2.7 Validación técnica y reproducibilidad

- Estado:
  no aparece como capítulo explícito en la pauta, pero es altamente recomendable y consistente con la exigencia de reproducibilidad.
- Contenido:
  tests, cobertura, CI/CD, validación E2E, riesgos de reproducibilidad.
- Evidencia:
  suficiente.
- Fuentes:
  [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md), [server/tests](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/tests), [test.yml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.github/workflows/test.yml), [container-smoke-test.yml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.github/workflows/container-smoke-test.yml), [e2e_validation.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/e2e_validation.md), [e2e_validate.sh](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/scripts/e2e_validate.sh), [containers.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/containers.md), [.env.example](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.env.example), [pyproject.toml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/pyproject.toml), [EVIDENCE_MAP.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/EVIDENCE_MAP.md).
- Vacío:
  falta una corrida local reejecutada en este workspace y una evidencia archivada de validación productiva completa con Onyx.

### 2.3 Conclusiones

- Estado: obligatoria.
- La pauta pide:
  discusión de eficacia de las soluciones propuestas y recomendaciones para futuras investigaciones o aplicaciones en el negocio.
- Evidencia:
  parcial, pero suficiente para conclusiones técnicas prudentes.
- Fuentes:
  [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [EVIDENCE_MAP.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/EVIDENCE_MAP.md), [precompute_features_pipeline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/precompute_features_pipeline.md).
- Vacío:
  faltan conclusiones cuantitativas finales del modelo principal con respaldo completamente reproducible.

## 3. Referencias y cierre documental

### 3.1 Referencias bibliográficas

- Estado: obligatoria según la guía general.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Base actual:
  [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib), [BIBLIOGRAPHY_SEED.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/BIBLIOGRAPHY_SEED.md).
- Vacío:
  el archivo existente es semilla; falta decidir el subconjunto final efectivamente citado y adecuarlo al estilo institucional.

### 3.2 Bibliografía consultada

- Estado: contemplada en la guía general.
- Observación:
  puede mantenerse separada de las referencias efectivamente citadas si la institución lo exige.
- Base actual:
  [BIBLIOGRAPHY_SEED.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/BIBLIOGRAPHY_SEED.md), [LITERATURE_MATRIX.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LITERATURE_MATRIX.md).
- Vacío:
  falta decidir si se presentará separada de las referencias citadas y ampliar cobertura hacia inventarios y métricas de forecast orientadas a negocio.

### 3.3 Estilo de citas y referencias

- Estado:
  debe alinearse con el estilo aprobado por la unidad académica.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Base actual:
  [CITATION_STYLE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/CITATION_STYLE.md), [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib).
- Vacío:
  la convención ya está fijada para el manuscrito en Markdown, pero resta confirmar si la versión final institucional exigirá un estilo específico distinto.

## 4. Material complementario

### 4.1 Anexos

- Estado: recomendados y explícitamente contemplados por la guía general.
- Candidatos naturales para este proyecto:
  - contrato API y esquemas;
  - lista completa de features;
  - tablas extendidas de métricas;
  - evidencia de cobertura y pruebas;
  - diagramas de arquitectura;
  - detalles de configuración docker y variables de entorno.
- Fuentes:
  [LISTA_DE_ANEXOS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LISTA_DE_ANEXOS.md), [anexo_reproducibilidad_operativa.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/anexo_reproducibilidad_operativa.md), [schemas.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/interface/http/schemas.py), [precompute_features.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/scripts/precompute_features.py), [data_serving_architecture.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/data_serving_architecture.md), [precompute_features_pipeline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/precompute_features_pipeline.md), [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md), [NOTEBOOKS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/NOTEBOOKS.md), [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [LGBM_CV_EVIDENCE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LGBM_CV_EVIDENCE.md).
- Base actual:
  [LISTA_DE_ANEXOS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LISTA_DE_ANEXOS.md).
- Vacío:
  ya existe una lista base, pero falta decidir qué anexos candidatos entrarán efectivamente y fijar la numeración final del manuscrito.

### 4.2 Repositorio de soporte

- Estado:
  no es una sección del manuscrito, pero sí un requisito práctico sugerido por las pautas MCD para asegurar reproducibilidad.
- Evidencia:
  el repositorio ya cumple ese rol de soporte técnico y documental.

## 5. Orden de redacción recomendado

1. Introducción
2. Metodología
3. Arquitectura e implementación del sistema
4. EDA
5. Experimentos
6. Conclusiones
7. Resumen
8. Referencias, anexos y elementos preliminares finales

## 6. Riesgos de completitud todavía abiertos

1. Falta consolidar bibliografía formal y sistema de citas.
2. Falta traducir la formulación ya cerrada de pregunta, objetivos e hipótesis en criterios de valor de negocio más operativos.
3. Falta confirmar si se incluirán todos los preliminares institucionales en Markdown o si algunos se incorporarán recién en la versión final maquetada.
4. Falta cerrar la trazabilidad cuantitativa del modelo principal para que la sección de experimentos no dependa de inferencias.
