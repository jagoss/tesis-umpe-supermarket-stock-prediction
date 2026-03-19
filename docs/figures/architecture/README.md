# Figuras de arquitectura

| Archivo | Título sugerido | Fuente | Nota de uso |
|---|---|---|---|
| `architecture_01_current_system.png` | Figura 6. Arquitectura vigente del sistema de predicción e integración con Onyx | Código actual del repositorio y documentos `README.md`, `.docs/data_serving_architecture.md`, `.docs/onyx_integration.md`, `server/infrastructure/container.py`, `server/interface/http/api.py`, `docker-compose.yml` | Diagrama de alto nivel de la arquitectura efectivamente implementada: usuario, stack Onyx, servidor de predicción por capas, artefactos ONNX/Parquet y controles técnicos. Evita el esquema legacy de `arquitectura_proyecto.md`. |

## Archivos fuente asociados

- `.docs/diagrams/current_system_architecture.puml`: fuente PlantUML editable del diagrama actual.
- `architecture_01_current_system.png`: exportación raster lista para insertar en el manuscrito Word.
- `architecture_01_current_system.svg`: fuente vectorial maestra del diagrama.
