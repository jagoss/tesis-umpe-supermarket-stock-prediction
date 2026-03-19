# Figura lista para integrar en Arquitectura

Este archivo reúne la figura seleccionada para el capítulo `Arquitectura e implementación del sistema`, con numeración sugerida, pie definitivo y texto breve de referencia en el cuerpo del capítulo.

## Convención sugerida

- Mantener numeración global correlativa respecto de `EDA`.
- Dado que [eda.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/eda.md) ya utiliza `Figura 1` a `Figura 5`, esta figura de arquitectura debe quedar como `Figura 6`.
- Si más adelante se agregan figuras de resultados antes de este capítulo, conviene renumerar globalmente al momento de la compilación final, pero conservar el mismo pie textual.

## Figura 6

Texto de referencia sugerido en el cuerpo:

`La Figura 6 resume la arquitectura vigente del sistema, mostrando la separación por capas del servidor de predicción, su exposición por REST y MCP, y su integración con Onyx y con los artefactos de inferencia.` 

Bloque listo para pegar:

```md
![Figura 6. Arquitectura vigente del sistema de predicción e integración con Onyx](figures/architecture/architecture_01_current_system.svg)

**Figura 6. Arquitectura vigente del sistema de predicción e integración con Onyx.** Diagrama de alto nivel de la arquitectura efectivamente implementada en el repositorio. La figura muestra la interacción entre el usuario, el stack conversacional de Onyx, el servidor de predicción organizado según Clean Architecture, los artefactos de inferencia en `ONNX` y `Parquet`, y los principales controles técnicos observables en la solución. Fuente: elaboración propia a partir de `README.md`, `.docs/data_serving_architecture.md`, `.docs/onyx_integration.md`, `server/infrastructure/container.py`, `server/interface/http/api.py` y `docker-compose.yml`.
```

## Entrada sugerida para la lista de figuras

`Figura 6. Arquitectura vigente del sistema de predicción e integración con Onyx.`

## Nota editorial

- Esta figura ya puede considerarse definitiva para la sección de arquitectura.
- Solo haría falta una figura adicional si luego se decide separar visualmente la topología general del sistema y el pipeline interno de inferencia.
