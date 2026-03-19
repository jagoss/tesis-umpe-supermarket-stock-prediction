# Trazabilidad de citas y BibTeX

Fecha de verificación: 2026-03-19 (America/Montevideo).

Objetivo: verificar la correspondencia `cita en texto -> entrada BibTeX` para evitar referencias huérfanas o entradas no usadas en el manuscrito actual.

Alcance de esta verificación:
- se revisaron las citas efectivamente usadas en [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md);
- se auditó además la ausencia/presencia de citas en [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md), [metodologia.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/metodologia.md), [eda.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/eda.md), [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md), [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md) y [anexo_reproducibilidad_operativa.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/anexo_reproducibilidad_operativa.md);
- no se contaron como citas del manuscrito los ejemplos normativos de [CITATION_STYLE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/CITATION_STYLE.md);
- [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib) se interpretó como el subconjunto de obras efectivamente citadas hasta la fecha.

## Resultado general

- citas verificadas en manuscrito: `10`
- entradas en [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib): `10`
- citas sin entrada BibTeX correspondiente: `0`
- entradas BibTeX sin uso en el manuscrito actual: `0`
- secciones del manuscrito con citas bibliográficas formales: `6`
- capítulos adicionales auditados sin citas bibliográficas formales: `1`

## Tabla de correspondencia

| Cita en texto | Archivo fuente | Entrada BibTeX | Estado | Observación |
|---|---|---|---|---|
| `Fildes, Ma, & Kolassa (2022)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L11) | `fildes2022retail` | OK | Aparece también en una cita múltiple de la misma sección |
| `Fildes, Kolassa, & Ma (2022)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L13) | `fildes2022postscript` | OK | Complementa la referencia anterior en discusión de retail forecasting |
| `Hewamalage, Bergmeir, & Bandara (2020)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L17) | `hewamalage2020global` | OK | Sostiene el bloque sobre modelos globales |
| `Montero-Manso & Hyndman (2021)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L17) | `monteromanso2021globality` | OK | Complementa la discusión sobre globalidad/localidad |
| `Nixtla (2026)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L19) | `nixtla_mlforecast_docs` | OK | Autor corporativo normalizado según [CITATION_STYLE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/CITATION_STYLE.md) |
| `Huber & Stuckenschmidt (2020)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L23) | `huber2020retail` | OK | Cubre señales calendarias y días especiales |
| `Ke et al. (2017)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L25) | `ke2017lightgbm` | OK | Sostiene la descripción del algoritmo base |
| `Sculley et al. (2015)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L31) | `sculley2015debt` | OK | Aparece en dos bloques sobre consistencia y serving |
| `Breck et al. (2017)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L31) | `breck2017mltestscore` | OK | Aparece en dos bloques sobre readiness productiva |
| `ONNX (2026)` | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L37) | `onnx_overview` | OK | Autor corporativo único para documentación oficial |

## Secciones del manuscrito con citas bibliográficas formales

Las siguientes secciones ya contienen citas autor-anio consistentes con [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib):

| Sección | Estado actual | Referencias usadas |
|---|---|---|
| [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md) | Con citas formales | `fildes2022retail`, `hewamalage2020global`, `sculley2015debt`, `breck2017mltestscore`, `monteromanso2021globality`, `ke2017lightgbm`, `onnx_overview`, `nixtla_mlforecast_docs` |
| [metodologia.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/metodologia.md) | Con citas formales | `hewamalage2020global`, `monteromanso2021globality`, `huber2020retail`, `ke2017lightgbm`, `nixtla_mlforecast_docs`, `onnx_overview`, `sculley2015debt`, `breck2017mltestscore` |
| [eda.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/eda.md) | Con citas formales | `fildes2022retail`, `hewamalage2020global`, `monteromanso2021globality`, `huber2020retail` |
| [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md) | Con citas formales | `fildes2022retail`, `fildes2022postscript`, `hewamalage2020global`, `monteromanso2021globality`, `nixtla_mlforecast_docs`, `huber2020retail`, `ke2017lightgbm`, `sculley2015debt`, `breck2017mltestscore`, `onnx_overview` |
| [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md) | Con citas formales | `sculley2015debt`, `breck2017mltestscore`, `onnx_overview` |
| [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md) | Con citas formales | `sculley2015debt`, `breck2017mltestscore` |

## Entradas BibTeX vigentes

Entradas actualmente presentes en [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib):

1. `breck2017mltestscore`
2. `fildes2022retail`
3. `fildes2022postscript`
4. `huber2020retail`
5. `hewamalage2020global`
6. `ke2017lightgbm`
7. `monteromanso2021globality`
8. `sculley2015debt`
9. `nixtla_mlforecast_docs`
10. `onnx_overview`

## Secciones auditadas sin citas bibliográficas formales

Las siguientes secciones fueron revisadas y actualmente no contienen citas bibliográficas autor-año en el texto:

| Sección | Estado actual | Observación |
|---|---|---|
| [anexo_reproducibilidad_operativa.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/anexo_reproducibilidad_operativa.md) | Sin citas formales | Es un anexo técnico-operativo, no un capítulo argumentativo |

## Observaciones editoriales

1. Las secciones que hoy usan citas bibliográficas formales en el manuscrito son `introduccion.md`, `metodologia.md`, `eda.md`, `estado_arte_conceptos.md`, `arquitectura_implementacion.md` y `validacion_reproducibilidad.md`.
2. [CITATION_STYLE.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/CITATION_STYLE.md) contiene ejemplos de formato, no referencias efectivamente usadas en el manuscrito.
3. La normalización `Nixtla (2026)` sigue siendo válida porque solo una obra de `Nixtla` está citada actualmente.
4. Si luego se incorporan citas en `introduccion.md`, `metodologia.md` u otros capítulos, este archivo debe actualizarse para preservar trazabilidad completa.
