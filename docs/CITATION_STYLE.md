# Estilo de citas y referencias

Fecha de decisión editorial: 2026-03-18 (America/Montevideo).

## Criterio de decisión

Las pautas institucionales revisadas no fijan explícitamente un estilo nominal único del tipo `APA`, `IEEE` o `Chicago`. El documento `Pautas para tesis - MCD24.docx` sí exige, de forma expresa, "correcto manejo de citas, bibliografía, etc.". Dado ese marco y el estado actual del manuscrito en Markdown, se adopta para esta tesis una convención autor-año compatible con escritura académica de maestría y adecuada para capítulos conceptuales, metodológicos y aplicados.

Decisión operativa:
- usar estilo autor-año en el cuerpo del texto;
- mantener una lista final de referencias alfabética por autor;
- gestionar la base bibliográfica en [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib);
- conservar [BIBLIOGRAPHY_SEED.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/BIBLIOGRAPHY_SEED.md) y [LITERATURE_MATRIX.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LITERATURE_MATRIX.md) como artefactos de trabajo editorial.

## Regla de citación en el texto

### Cita parentética

Usar:
- un autor: `(Apellido, 2021)`
- dos autores: `(Apellido & Apellido, 2021)`
- tres o más autores: `(Apellido et al., 2021)`
- autor corporativo: `(Nixtla, 2026)` o `(ONNX, 2026)`

### Cita narrativa

Usar:
- un autor: `Apellido (2021)`
- dos autores: `Apellido y Apellido (2021)` en redacción española
- tres o más autores: `Apellido et al. (2021)`
- autor corporativo: `Nixtla (2026)` o `ONNX (2026)`

### Múltiples referencias en una misma cita

Usar orden semántico o cronológico razonable, separado por punto y coma:

`(Sculley et al., 2015; Breck et al., 2017)`

## Regla para autores corporativos y años repetidos

En el estado actual del manuscrito:
- `Nixtla (2026)` refiere a `MLForecast Documentation`;
- `ONNX (2026)` refiere a `Overview`.

Regla de normalización:
- si solo se cita una fuente de `Nixtla` en un capítulo, usar `Nixtla (2026)`;
- si luego se citan dos fuentes distintas de `Nixtla` del mismo año en una misma sección o capítulo, usar sufijos manuales `2026a` y `2026b` tanto en el texto como en la lista final de referencias;
- mientras esa segunda cita no exista en el manuscrito, no usar sufijos innecesarios.

## Regla para la lista final de referencias

- ordenar alfabéticamente por autor o autor corporativo;
- usar una única entrada por obra efectivamente citada;
- mantener DOI y URL cuando estén disponibles y ya estén verificados;
- no inventar paginación, editorial, venue ni DOI faltantes;
- distinguir referencias efectivamente citadas de bibliografía solo consultada si la institución finalmente exige esa separación.

## Convención práctica para Markdown

1. Redactar citas en texto plano con formato autor-año.
2. Mantener la fuente maestra en `references_seed.bib`.
3. Si se exporta luego con Pandoc o un flujo equivalente, este archivo funciona como política editorial base aunque el CSL final cambie.
4. Hasta definir un pipeline automático de citas, evitar mezclar estilos numéricos y autor-año en distintos capítulos.

## Normalizaciones ya aplicadas

- En [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md) se usa `Nixtla (2026)` en lugar de `Nixtla (2026a)`, porque actualmente solo se cita una fuente de `Nixtla`.
- Se mantiene `ONNX (2026)` como autor corporativo único para la documentación oficial citada.

## Límites de esta decisión

1. Esta convención fija consistencia editorial, pero no sustituye una futura validación formal con la dirección de tesis si la unidad académica exige un estilo específico.
2. Si la versión final maquetada se arma en Word, LaTeX o Pandoc con otro CSL, habrá que mapear esta convención al formato definitivo.
3. La decisión no amplía por sí sola la cobertura bibliográfica; solo ordena cómo citar la evidencia ya consolidada.
