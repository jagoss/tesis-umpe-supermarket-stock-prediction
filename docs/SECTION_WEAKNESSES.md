# Debilidades por Sección de los Markdown Generados

Fecha de consolidación: 2026-03-18 (America/Montevideo).

## Criterio de lectura

Este documento resume las debilidades detectadas en los archivos Markdown creados hasta el momento. La noción de "debilidad" incluye cuatro tipos de problemas:

- falta de evidencia o trazabilidad;
- riesgo de sobreafirmación;
- vacíos de completitud académica o documental;
- problemas de reproducibilidad o actualización pendiente.

La columna `Acción sugerida` apunta a la siguiente mejora razonable, no necesariamente a la versión final del texto.

## 1. `docs/NOTEBOOKS.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Global_Simple_LightGBM_Timeseries_Forecast_Final.ipynb` | El notebook mezcla exploración, entrenamiento y exportación; además conserva rutas frágiles y outputs no totalmente confiables. | Reduce trazabilidad metodológica y reproducibilidad. | Separar en tesis qué evidencia se toma como pipeline final y qué se trata solo como antecedente técnico. |
| `Global_Simple_LightGBM_Timeseries_Forecast_Final_academic.ipynb` | La métrica final del modelo principal sigue sin quedar exportada como artefacto documental independiente. | Debilita la futura sección de experimentos/resultados. | Exportar resultados de validación a CSV y referenciarlos desde la tesis. |
| `Directorio adicional de notebooks` | Es una sección casi vacía y solo deja constancia de ausencia. | Aporta poco valor narrativo. | Mantenerla breve o moverla a un anexo/inventario técnico si el documento crece. |
| `analisis_exploratorio_ecuador_sales_forecast.ipynb` | Varias conclusiones están formuladas en lenguaje interpretativo dentro del notebook, pero sin tablas exportadas que las respalden directamente. | Riesgo de sobreafirmación al llevar hallazgos a la tesis. | En la tesis, marcar esos hallazgos como observaciones exploratorias basadas en visualización. |
| `analisis_exploratorio_ecuador_sales_forecast_academic.ipynb` | Mejora la estructura, pero no resuelve la falta de figuras exportadas ni la dependencia de outputs embebidos. | La utilidad documental mejora, pero no reemplaza materiales listos para manuscrito final. | Exportar figuras y, si es necesario, construir un anexo visual con numeración estable. |

## 2. `docs/EVIDENCE_MAP.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Mapa principal` | Algunas filas siguen dependiendo de notebooks como fuente casi exclusiva de evidencia, sin artefactos independientes asociados. | La tesis puede quedar demasiado atada a cuadernos difíciles de citar visualmente. | Complementar con tablas exportadas, figuras y anexos estables. |
| `Vacios transversales prioritarios` | Enumera vacíos correctamente, pero no prioriza por dependencia entre secciones futuras. | Puede dificultar la planificación de redacción. | Reordenar por criticidad para tesis: resultados, bibliografía, figuras, reproducibilidad, documentación legacy. |

## 3. `docs/RESULTS_SUMMARY.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Modelos probados` | El inventario está bien trazado, pero aún mezcla modelos de experimentación, serving y backend dummy. | Puede generar ruido conceptual en la tesis. | Separar más claramente modelos experimentales, artefactos de serving y componentes de prueba. |
| `2.1 Metricas directamente visibles en artefactos` | La evidencia para LGBM ya incluye `RMSLE`, pero sigue siendo menos rica que la de los baselines. | Deja asimétrica la comparación experimental. | Exportar o reconstruir tambien `MAE`, `RMSE` y detalle por corte para LGBM. |
| `2.2 Metricas derivadas desde archivo existente` | Las métricas calculadas en auditoría son válidas, pero no provienen de un artefacto original ya preparado para tesis. | Puede requerir una explicación metodológica adicional en el manuscrito. | Mantener la nota de procedencia y, si es posible, guardar un CSV derivado versionado. |
| `2.3 Metricas no recuperables con trazabilidad completa` | El vacío ya no es el `RMSLE`, sino la ausencia de un artefacto tabular completo para `LightGBM`. | Sigue afectando la comparación experimental completa. | Resolver antes de cerrar resultados formales con más de una métrica. |
| `3) Tablas/archivos de resultados disponibles` | Lista artefactos útiles, pero no arma todavía una tabla final integrada de “qué archivo sostiene qué afirmación”. | Puede generar redundancia con `EVIDENCE_MAP.md`. | Mantener este archivo como inventario y usar `EVIDENCE_MAP.md` para la trazabilidad argumental. |
| `4) Figuras disponibles` | La sección evidencia escasez de material gráfico experimental exportado. | Debilita presentación académica. | Crear carpeta de figuras de EDA y resultados antes de cerrar manuscrito. |
| `5) Hallazgos principales observables` | Algunos hallazgos son más técnicos que académicos y requerirán recorte posterior. | Puede recargar futuras conclusiones. | Seleccionar solo los hallazgos que respondan la pregunta de investigación o el problema de negocio. |
| `6) Limitaciones y ambiguedades` | Está bien planteada, pero aún no distingue qué limitaciones son bloqueantes y cuáles son manejables. | Riesgo de dispersión al priorizar mejoras. | Clasificar limitaciones en críticas, importantes y menores. |

## 4. `docs/thesis_outline.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `0. Criterio de organización` | Define bien el marco, pero no fija aún una convención terminológica cerrada para toda la tesis. | Riesgo de variación de términos entre capítulos. | Definir glosario mínimo y vocabulario controlado antes de redactar más secciones. |
| `1. Elementos preliminares` | La mayoría de sus subsecciones son estructurales, pero todavía no tienen contenido fuente asociado. | No bloquea la tesis técnica, pero deja pendiente la entrega formal. | Tratar estas secciones como checklist editorial de cierre, no como prioridad inmediata. |
| `1.8 Lista de tablas` | Ya existe una base, pero su cobertura sigue siendo mínima porque el manuscrito solo integra una tabla formal hasta ahora. | Riesgo bajo, aunque puede dejar débil el aparato tabular si no crece el capítulo de resultados. | Mantener la lista actual y ampliarla solo cuando ingresen nuevas tablas realmente integradas en el cuerpo de la tesis. |
| `1.13 Resumen` | Ya existe borrador, pero su solidez sigue limitada por el cierre experimental parcial del modelo principal. | Riesgo de inconsistencias si luego cambian los resultados consolidados. | Mantener el resumen prudente actual y ajustarlo solo si se exporta evidencia cuantitativa más completa. |
| `1.14 Palabras clave` | Ya existe una propuesta, pero todavía puede cambiar si la terminología dominante del manuscrito se ajusta en la versión final. | Riesgo bajo de inconsistencia conceptual. | Mantener la propuesta actual y revisarla en la etapa de maquetación final. |
| `2.1 Introducción` | Ya existe formulación cerrada de pregunta, objetivos, hipótesis, alcance y valor operativo esperado, pero aún falta expresar ese valor en indicadores de negocio más formales si se quiere cerrar la dimensión aplicada. | Riesgo moderado de que el caso aplicado siga dependiendo de formulaciones cualitativas. | Mantener el texto actual y, si se dispone de evidencia adicional, traducir el valor esperado a indicadores de negocio más precisos. |
| `2.2.1 Contexto del problema y caso de negocio` | El vínculo con negocio ya fue reforzado en Introducción y Conclusiones, pero todavía no se expresa en un marco de evaluación operativa formal. | Reduce parcialmente la fuerza aplicada del caso. | Incorporar, si la evidencia futura lo permite, criterios de negocio más estructurados para reposición y gestión de stock. |
| `2.2.2 Conceptos teóricos y estado del arte` | Ya existe una base conceptual con citas bibliográficas integradas, pero todavía falta ampliar la comparación con literatura previa y cubrir mejor el frente de inventarios/reposición. | Alto impacto en evaluación de maestría. | Usar la base actual como marco conceptual citado y ampliar cobertura temática antes de cerrar el capítulo. |
| `2.2.3 Metodología` | Ya existe borrador, pero faltan justificaciones más fuertes para algunas decisiones de diseño. | Puede generar preguntas metodológicas en defensa. | Reforzar motivación de selección de feriados, escala, validación y exportación. |
| `2.2.4 EDA` | Ya existe borrador fuerte, con soporte visual exportado e integrado; la debilidad principal ya no es la selección o integración de figuras, sino la necesidad de mantener consistencia de numeración y referencias cruzadas al cerrar el manuscrito. | Riesgo bajo a moderado, no bloqueante. | Ajustar numeración final y cross-references cuando el manuscrito completo quede estabilizado. |
| `2.2.5 Arquitectura e implementación del sistema` | Ya existe borrador fuerte y una figura exportada, pero persiste documentación legacy en paralelo y aún puede faltar un segundo diagrama más fino del pipeline interno. | Riesgo bajo a moderado de mezcla entre arquitectura actual e histórica. | Mantener el capítulo apoyado en código y docs vigentes; solo agregar un diagrama complementario si realmente aporta a la explicación metodológica. |
| `2.2.6 Experimentos` | Ya existe evidencia suficiente para una comparación parcial en `RMSLE`, pero no para una comparación métrica completa ni completamente homogénea en alcance. | Impacto alto, ya no crítico en el mismo grado. | Exportar `cv_results_lgbm` o un resumen equivalente con `MAE`, `RMSE` y detalle por cutoff, aclarando o alineando el conjunto de series comparado. |
| `2.2.7 Validación técnica y reproducibilidad` | Hay evidencia fuerte de tests, pero con fallas de entorno no resueltas del todo. | Puede ser cuestionado como reproducibilidad parcial. | Documentar explícitamente qué corre, qué no corre y bajo qué dependencias. |
| `2.3 Conclusiones` | Ya existe borrador, pero su fuerza interpretativa sigue limitada por la comparación experimental parcial del modelo principal. | Medio a alto. | Mantener el cierre prudente actual y reforzarlo solo si luego se exporta evidencia completa de `LightGBM`. |
| `3. Referencias y cierre documental` | Ya existe una base bibliográfica mínima y una convención de citas para Markdown, pero el cierre final sigue dependiendo de la validación institucional del estilo y de la depuración del set efectivamente citado. | Vacío académico importante, aunque ya parcialmente reducido. | Mantener sincronizados `Markdown` y `.bib`, y confirmar el estilo final antes de maquetar. |
| `4. Material complementario` | La idea está bien, pero aún no están definidos anexos concretos ni piezas visuales estables. | Puede dejar el cierre documental incompleto. | Planificar anexos mínimos: API, arquitectura, figuras EDA, tablas de resultados. |
| `4.1 Anexos` | Ya existe una lista base, pero todavía mezcla un anexo listo con anexos solo candidatos. | Riesgo bajo a medio de sobredimensionar el material complementario final. | Mantener `Anexo A` como anexo seguro y decidir los anexos restantes solo al cierre editorial. |
| `5. Orden de redacción recomendado` | Es útil, pero debería actualizarse cuando se destrabe la evidencia de resultados. | Bajo impacto. | Revisarlo al iniciar la fase de experimentos. |
| `6. Riesgos de completitud todavía abiertos` | Enumera riesgos, pero algunos ya cambiaron tras el nuevo notebook de EDA. | Puede quedar desactualizado. | Sincronizarlo con el estado actual del repositorio documental. |

## 5. `docs/introduccion.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Introducción` | La formulación académica central y el valor operativo esperado ya quedaron explicitados, pero la tesis todavía no dispone de indicadores observados de impacto de negocio. | Riesgo moderado, ya más acotado. | Mantener la formulación actual y evitar convertir el valor esperado en impacto medido sin evidencia adicional. |

## 6. `docs/metodologia.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Datos y alcance del problema` | Distingue bien entre datos disponibles y datos usados, pero aún no justifica con suficiente profundidad la exclusión práctica de algunas fuentes auxiliares. | Puede abrir preguntas sobre variables no utilizadas. | Explicar mejor por qué `stores`, `transactions` y `oil` no quedan en el vector final o cómo quedan fuera del pipeline productivo. |
| `Preparación y estructuración de los datos` | Describe la regularización temporal, pero la tesis aún no explica del todo la diferencia entre panel crudo y panel regularizado. | Riesgo de ambigüedad metodológica. | Incorporar nota explícita sobre las cuatro Navidades faltantes y su tratamiento. |
| `Ingeniería de características` | La elección de feriados por correlación y el uso de `LocalStandardScaler` están descritos, pero no del todo defendidos. | Posibles preguntas metodológicas en defensa. | Añadir racionalidad técnica y límites de ambas decisiones. |
| `Modelado y estrategia de validación` | La estrategia está clara, pero el resultado principal sigue incompleto. | Debilidad crítica para experimentos posteriores. | Resolver la trazabilidad de métricas del modelo principal. |
| `Exportación a ONNX y serving en producción` | Está bien fundamentada técnicamente, pero aún puede confundirse implementación con aporte científico si no se matiza después. | Riesgo de desbalance entre ingeniería y análisis científico. | En capítulos posteriores, dejar claro qué es contribución de ingeniería y qué es contribución analítica. |
| `Consideraciones de reproducibilidad y alcance` | Reconoce limitaciones, pero todavía no lista prerequisitos concretos de reejecución. | Reproducibilidad parcial. | Añadir entorno, dependencias mínimas y pasos esperados de reejecución. |

## 7. `docs/eda.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Alcance y fuentes del análisis` | La dependencia exclusiva de notebooks ya se redujo y las cinco figuras están integradas, pero varios hallazgos siguen dependiendo de evidencia visual agregada. | Bajo a medio. | Mantener referencias explícitas a cada figura y evitar sobreinterpretaciones causales. |
| `Calidad de datos y completitud temporal` | Ya es sólida, pero algunas conclusiones sobre ceros podrían requerir segmentación adicional para ser más útiles al negocio. | Medio. | Complementar con análisis por familia o tienda si luego resulta relevante para resultados. |
| `Heterogeneidad entre series, tiendas y familias` | Se apoya en agregados útiles, pero todavía no entra en clústeres o patrones operativos más finos. | Bajo a medio. | Solo profundizar si luego se usa como argumento central en discusión. |
| `Promociones, transacciones, petróleo y patrones de calendario` | Las correlaciones están bien cuantificadas, pero siguen siendo descriptivas sobre series agregadas. | Medio. | Mantener lenguaje prudente y evitar convertir correlación en causalidad. |
| `Feriados, escala territorial y relevancia relativa` | La evidencia sobre impacto diferencial de feriados sigue siendo principalmente visual y descriptiva, aunque ya cuenta con boxplots exportados y seleccionados. | Medio. | Mantener la formulación como hallazgo exploratorio y acompañarla con referencias explícitas a las figuras. |
| `Implicancias para el problema de negocio y el modelado` | El puente argumental es bueno, pero algunas implicancias siguen siendo inferencias razonables y no pruebas directas. | Bajo a medio. | Mantener la distinción entre observación, interpretación y decisión metodológica. |
| `Limitaciones del análisis exploratorio disponible` | Está bien planteada, pero aún no ofrece un plan explícito de cierre de esas limitaciones. | Bajo. | Añadir, si se desea, una lista corta de figuras y tablas pendientes. |

## 8. `docs/validacion_reproducibilidad.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Alcance de la validación técnica` | La distinción entre validación del sistema y validación del modelo está clara, pero puede requerir refuerzo cuando se redacte `Experimentos` para evitar solapamientos. | Medio. | Mantener una frontera explícita entre robustez del software y desempeño predictivo. |
| `Evidencia de pruebas automatizadas` | El recuento de pruebas es sólido, pero en esta auditoría no pudo reejecutarse `pytest` por ausencia de dependencias locales. | Medio. | Si luego el entorno se completa, agregar una corrida local actualizada como anexo o nota metodológica. |
| `Validación del contenedor y del contrato de servicio` | La evidencia es fuerte para el backend `dummy`, pero no demuestra la operación del backend productivo. | Medio. | Aclarar siempre que el smoke test valida contrato y empaquetado, no calidad del modelo ONNX final. |
| `Validación end-to-end e integración con Onyx` | Existe procedimiento y checklist, pero no artefactos versionados de una corrida final completa. | Medio a alto. | Guardar logs, capturas o un reporte de ejecución E2E si luego se hace una validación final del stack completo. |
| `Condiciones de reproducibilidad del entorno` | Describe prerequisitos y scripts, pero el proyecto sigue sin lockfile estricto de dependencias. | Medio. | Evaluar congelar dependencias críticas o documentar una instalación de referencia más cerrada. |
| `Límites observables de reproducibilidad` | Está bien explicitada, pero hace visible que la reproducibilidad demostrada sigue siendo parcial. | Medio. | Mantener esta honestidad metodológica y evitar afirmaciones más fuertes que la evidencia disponible. |

## 9. `docs/anexo_reproducibilidad_operativa.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Prerrequisitos mínimos` | El anexo es operativo y útil, pero depende de documentación externa del propio repo para varios detalles finos. | Bajo. | Mantenerlo breve y usarlo como apoyo, no como reemplazo de la sección principal de reproducibilidad. |
| `Configuración mínima` | Enumera variables y modos de operación, pero no demuestra una ejecución productiva real en este entorno. | Medio. | Si luego se levanta el stack completo, añadir una nota de ejecución efectiva o capturas/logs en anexos. |
| `Comandos de validación técnica` | Documenta procedimientos, pero no agrega resultados nuevos porque `pytest` no está disponible localmente. | Medio. | Reutilizarlo como checklist reproducible y no como evidencia de corrida actual. |
| `Límites conocidos` | Hace visible la fragilidad relativa de la reproducibilidad actual. | Bajo a medio. | Conservarlo tal como está para evitar sobreafirmaciones. |

## 10. `docs/estado_arte_conceptos.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Alcance y criterio de esta sección` | La advertencia metodológica es correcta, pero deja explícito que el estado del arte aún no está completo en sentido académico. | Alto. | Completar luego con bibliografía y una matriz de trabajos previos. |
| `Predicción de demanda y problema de reposición` | Ya cuenta con citas sobre retail forecasting, pero todavía le falta cobertura específica sobre inventarios, stock de seguridad y reposición. | Medio. | Ampliar este bloque con referencias sobre decisiones de inventario orientadas a negocio. |
| `Series temporales multiserie y modelos globales` | Explica el enfoque global, pero no lo compara aún con enfoques alternativos desde literatura especializada. | Medio. | Incorporar comparación bibliográfica entre modelos globales y locales. |
| `Ingeniería de características temporales` | La explicación conceptual es sólida, aunque se apoya casi por completo en documentación interna. | Medio. | Complementar con referencias metodológicas externas sobre lags, rolling windows y escalado por serie. |
| `Consistencia entre entrenamiento e inferencia` | El concepto está bien formulado, pero por ahora se sostiene sobre documentación técnica y no sobre una revisión bibliográfica formal. | Medio. | Agregar citas académicas o de ingeniería reconocidas cuando se cierre el estado del arte. |
| `ONNX como formato de serving` | Describe bien el rol de ONNX en el proyecto, pero aún sin fuentes académicas o técnicas externas formalizadas en la tesis. | Medio. | Incorporar referencias oficiales o literatura técnica del formato al consolidar referencias. |
| `Síntesis del estado del arte disponible en el repositorio` | Es útil y honesta, pero confirma que el capítulo sigue siendo parcial. | Alto. | Usarlo como base del capítulo final y no como versión definitiva hasta resolver bibliografía. |

## 11. `docs/BIBLIOGRAPHY_SEED.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Literatura académica núcleo` | La selección ya cubre forecasting retail, modelos globales, deuda técnica y ONNX, pero sigue siendo una muestra mínima y no una revisión exhaustiva. | Medio a alto. | Mantenerla como semilla y ampliar luego hacia inventarios, reposición y métricas orientadas al negocio. |
| `Documentación oficial técnica` | Aporta sustento instrumental fuerte, pero no reemplaza literatura académica en el estado del arte. | Medio. | Usarla para describir herramientas y formatos, no como base única del marco teórico. |
| `Uso sugerido por tema` | Ordena bien las referencias, pero aún no las ata a pasajes concretos del capítulo. | Medio. | Sincronizar esta semilla con citas explícitas en `estado_arte_conceptos.md`. |
| `Vacíos que siguen abiertos` | Reconoce honestamente lo que falta, pero deja visible que el cierre bibliográfico todavía no es definitivo. | Medio. | Transformar esta semilla en lista final citada cuando se defina el estilo institucional. |

## 12. `docs/LITERATURE_MATRIX.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Matriz principal` | La matriz mejora mucho la trazabilidad, pero por ahora cubre un conjunto acotado de temas y fuentes. | Medio. | Ampliarla solo si el capítulo final incorpora nuevos frentes teóricos relevantes. |
| `Cobertura por subseccion sugerida` | Facilita la escritura, aunque sigue siendo una guia editorial y no una validacion academica cerrada. | Bajo a medio. | Usarla como mapa de redaccion y revisar luego que cada cita quede bien ubicada. |
| `Vacios que la matriz no resuelve` | Expone correctamente que la matriz no sustituye una revision exhaustiva. | Bajo. | Conservar esta advertencia para evitar sobreprometer el alcance del estado del arte. |

## 13. `docs/CITATION_STYLE.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Criterio de decisión` | La convención quedó fijada con base en pauta general, no en una norma institucional nominal explícita. | Medio. | Confirmar con dirección o reglamento final si debe mantenerse autor-año o migrar a un estilo específico. |
| `Regla para autores corporativos y años repetidos` | La regla de sufijos `a/b` es correcta como política editorial, pero solo se validará plenamente si luego se cita más de una fuente del mismo autor y año. | Bajo. | Aplicarla solo cuando efectivamente ocurra ese caso en el manuscrito. |
| `Convención práctica para Markdown` | Ordena el trabajo actual, pero todavía depende de una futura decisión sobre el pipeline final de exportación o maquetado. | Bajo a medio. | Mantener esta política hasta que se defina el flujo final de compilación del manuscrito. |

## 14. `docs/CITATION_TRACEABILITY.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Resultado general` | La verificación es sólida, pero por ahora solo cubre el capítulo teórico y no el manuscrito completo futuro. | Bajo a medio. | Reejecutar esta trazabilidad cuando se agreguen citas en introducción, metodología, experimentos o conclusiones. |
| `Tabla de correspondencia` | La tabla cubre bien el estado actual, pero depende de mantenimiento manual mientras no exista automatización de citas. | Bajo. | Actualizarla cada vez que entre o salga una referencia del texto. |
| `Observaciones editoriales` | Explicita correctamente el alcance limitado de la auditoría. | Bajo. | Mantener esa advertencia para evitar asumir cobertura total del manuscrito. |

## 15. `docs/experimentos.md`

| Sección | Debilidad principal | Impacto | Acción sugerida |
|---|---|---|---|
| `Diseño experimental y criterio de evaluación` | El protocolo está claro, pero sigue dependiendo del notebook como fuente primaria del detalle operativo. | Medio. | Mantener trazabilidad a celdas concretas y, si es posible, exportar un artefacto intermedio adicional. |
| `Baselines disponibles y resultados trazables` | La evidencia de baseline es sólida, aunque solo cubre 97 series y no el conjunto completo del problema. | Medio. | Explicitar siempre ese alcance cuando se compare con el modelo principal. |
| `Configuración experimental del modelo global LightGBM` | La configuración está bien reconstruida, pero no todos los hiperparámetros quedan discutidos ni justificados en el repositorio. | Medio. | Si se desea mayor profundidad, agregar una nota metodológica sobre uso de parámetros por defecto o selección de hiperparámetros. |
| `Resultados disponibles del modelo LightGBM y límites de trazabilidad` | El `RMSLE` ya es trazable desde el output del notebook, pero faltan artefactos equivalentes para el resto de la comparación y el alcance no es perfectamente homogéneo con el baseline tabulado. | Medio a alto. | Exportar `cv_results_lgbm` o un resumen de métricas equivalente para cerrar la comparación experimental y dejar explícito el conjunto de series comparado. |
| `Entrenamiento final y generación de predicciones para el conjunto de prueba` | La existencia de `submission.csv` prueba completitud operativa, pero no informa desempeño externo ni ranking. | Medio. | Mantener esta distinción y evitar equiparar entrega de submission con validación final del modelo. |
| `Síntesis crítica de la evidencia experimental disponible` | El cierre es honesto, pero confirma que la sección seguirá parcial hasta resolver métricas del modelo principal. | Alto. | Usar esta sección como base y no como versión final cerrada hasta completar el artefacto faltante. |

## 16. Prioridades de corrección

Orden sugerido de ataque, por impacto real en la tesis:

1. Exportar un artefacto comparable de resultados de `LightGBM` para completar `MAE`, `RMSE` y comparacion por cutoff en `Experimentos` y `Resumen`, alineando tambien el alcance de series comparadas.
2. Integrar la bibliografía mínima ya creada dentro del capítulo de estado del arte y ampliar solo los frentes teóricos que falten.
3. Integrar en el manuscrito las cinco figuras ya exportadas de `EDA` y luego exportar las de resultados.
4. Refinar pregunta de investigación, hipótesis y objetivos para que dejen de ser inferidos.
5. Documentar prerequisitos concretos de reproducibilidad.
