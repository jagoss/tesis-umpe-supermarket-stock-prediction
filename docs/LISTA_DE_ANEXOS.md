# Lista de anexos

Esta lista consolida los anexos efectivamente disponibles o claramente candidatos dentro de la base documental actual de la tesis. Se distingue entre anexos ya listos para integrarse al manuscrito y anexos cuya incorporación depende de una decisión editorial final.

## Anexos listos

1. `Anexo A. Reejecución y validación operativa del entorno.`

## Anexos candidatos

1. `Anexo B. Contrato técnico de la API y esquemas de entrada/salida.`
2. `Anexo C. Pipeline de pre-cómputo de características y serving de datos.`
3. `Anexo D. Inventario documental de notebooks y evidencia experimental.`

## Trazabilidad

| Anexo | Estado | Archivo o fuente principal | Observación |
|---|---|---|---|
| `Anexo A` | Listo | [anexo_reproducibilidad_operativa.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/anexo_reproducibilidad_operativa.md) | Puede integrarse ya al manuscrito como anexo técnico operativo. |
| `Anexo B` | Candidato | [schemas.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/interface/http/schemas.py), [api.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/server/interface/http/api.py) | Requiere decidir si conviene exponer el contrato como anexo técnico o dejarlo solo referenciado desde arquitectura. |
| `Anexo C` | Candidato | [precompute_features.py](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/scripts/precompute_features.py), [precompute_features_pipeline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/precompute_features_pipeline.md), [data_serving_architecture.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/data_serving_architecture.md) | Útil si se desea separar detalle técnico extenso del capítulo metodológico o de arquitectura. |
| `Anexo D` | Candidato | [NOTEBOOKS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/NOTEBOOKS.md), [RESULTS_SUMMARY.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/RESULTS_SUMMARY.md), [LGBM_CV_EVIDENCE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LGBM_CV_EVIDENCE.md) | Puede servir como respaldo documental si el tribunal exige trazabilidad técnica ampliada. |

## Recomendación editorial

- Para una versión controlada del manuscrito, el único anexo que hoy puede considerarse plenamente listo es `Anexo A`.
- Los anexos `B`, `C` y `D` son razonables, pero conviene incorporarlos solo si agregan claridad sin recargar el cuerpo principal.
- La numeración vigente quedó consolidada en [MANUSCRIPT_NUMBERING.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/MANUSCRIPT_NUMBERING.md).
- Si la institución no exige una lista de anexos independiente, este archivo puede usarse igualmente como hoja de control editorial para la versión final.
