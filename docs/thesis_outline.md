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

### 1.13 Resumen

- Estado: obligatoria.
- Fuente normativa:
  `Pautas para tesis - MCD24.docx`, `Guía Elaboración Tesinas (1).pdf`.
- Requisito:
  entre 150 y 300 palabras.
- Evidencia disponible:
  parcial.
- Insumos del repo:
  [README.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/README.md), [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [EVIDENCE_MAP.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/EVIDENCE_MAP.md).
- Vacío:
  falta una métrica final completamente trazable del modelo principal.

### 1.14 Palabras clave

- Estado: obligatoria.
- Fuente normativa:
  `Pautas para tesis - MCD24.docx`, `Guía Elaboración Tesinas (1).pdf`.

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
  [precompute_features_pipeline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/precompute_features_pipeline.md), [data_serving_architecture.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/data_serving_architecture.md), [onyx_integration.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/onyx_integration.md).
- Vacío:
  falta bibliografía académica consolidada y citas formalmente integradas.

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
  parcial.
- Fuentes:
  notebook académico, [NOTEBOOKS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/NOTEBOOKS.md).
- Vacío:
  no hay figuras EDA exportadas; habrá que construirlas a partir de notebooks o volver a ejecutarlos.

#### 2.2.5 Arquitectura e implementación del sistema

- Estado:
  no nombrada así en las pautas, pero necesaria para una tesis aplicada con repositorio y despliegue.
- Contenido:
  Clean Architecture, capas del sistema, API REST, MCP, ONNX, Onyx y despliegue dockerizado.
- Evidencia:
  suficiente.
- Fuentes:
  [README.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/README.md), [api.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/interface/http/api.py), [docker-compose.yml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docker-compose.yml), [Dockerfile](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/Dockerfile), [ONNX_INTEGRATION_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/ONNX_INTEGRATION_SUMMARY.md).

#### 2.2.6 Experimentos

- Estado: obligatoria en las pautas MCD.
- Contenido:
  diseño experimental, validación temporal, baselines, métrica de selección, resultados y comparación.
- Evidencia:
  parcial.
- Fuentes:
  notebook académico, [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [cv_results_baseline_retrained.csv](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/cv_results_baseline_retrained.csv), [submission.csv](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/submission.csv).
- Vacío:
  la métrica final del modelo LGBM principal sigue sin quedar completamente trazable en el estado actual del repositorio.

#### 2.2.7 Validación técnica y reproducibilidad

- Estado:
  no aparece como capítulo explícito en la pauta, pero es altamente recomendable y consistente con la exigencia de reproducibilidad.
- Contenido:
  tests, cobertura, CI/CD, validación E2E, riesgos de reproducibilidad.
- Evidencia:
  suficiente.
- Fuentes:
  [server/tests](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/tests), [test.yml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.github/workflows/test.yml), [e2e_validation.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/e2e_validation.md), [EVIDENCE_MAP.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/EVIDENCE_MAP.md).

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
- Vacío:
  todavía no existe un archivo bibliográfico consolidado dentro del repo.

### 3.2 Bibliografía consultada

- Estado: contemplada en la guía general.
- Observación:
  puede mantenerse separada de las referencias efectivamente citadas si la institución lo exige.
- Vacío:
  aún no está armada.

### 3.3 Estilo de citas y referencias

- Estado:
  debe alinearse con el estilo aprobado por la unidad académica.
- Fuente normativa:
  `Guía Elaboración Tesinas (1).pdf`.
- Vacío:
  en el material actual no está definido el estilo final a aplicar en Markdown.

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
  [schemas.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/interface/http/schemas.py), [precompute_features.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/scripts/precompute_features.py), [arquitectura_proyecto.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/arquitectura_proyecto.md), [data_serving_architecture.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/data_serving_architecture.md), [precompute_features_pipeline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/precompute_features_pipeline.md).

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
2. Falta decidir si la hipótesis quedará formulada explícitamente o si se trabajará con objetivos y pregunta de investigación.
3. Falta confirmar si se incluirán todos los preliminares institucionales en Markdown o si algunos se incorporarán recién en la versión final maquetada.
4. Falta cerrar la trazabilidad cuantitativa del modelo principal para que la sección de experimentos no dependa de inferencias.

