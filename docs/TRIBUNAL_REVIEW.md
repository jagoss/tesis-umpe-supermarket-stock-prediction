# Revisión global tipo tribunal del manuscrito numerado

## 0. Marco de evaluación aplicado

La revisión se realizó como auditoría de tesis completa de maestría con enfoque aplicado en ciencia de datos. Se utilizaron como marco operativo los criterios ya integrados en la base documental del repositorio, en particular [thesis_outline.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/thesis_outline.md), [MANUSCRIPT_NUMBERING.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/MANUSCRIPT_NUMBERING.md) y la revisión previa del manuscrito. Dado que el trabajo se presenta como tesis aplicada con componente fuerte de ingeniería, se asignó mayor peso a los siguientes criterios: rigor metodológico, calidad experimental, trazabilidad de resultados, reproducibilidad y capacidad de conectar la solución técnica con el problema de negocio.

## 1. Diagnóstico general

El manuscrito se encuentra en un estado avanzado y ya es reconocible como tesis completa: dispone de resumen, introducción, estado del arte, metodología, EDA, experimentos, arquitectura, validación técnica, conclusiones, bibliografía semilla, figuras, tablas, anexos y numeración global coherente. La mejora más importante respecto de la revisión anterior es que la introducción ya formula de manera explícita la pregunta de investigación, el objetivo general, los objetivos específicos, la hipótesis de trabajo y el alcance del estudio, y además traduce mejor el valor esperado hacia decisiones de reposición y planificación operativa.

Aun así, el manuscrito sigue teniendo tres frentes de debilidad reales desde una mirada de tribunal: el capítulo experimental continúa incompleto para una comparación cuantitativa cerrada, el estado del arte todavía es parcial en su cobertura de inventarios y reposición, y la reproducibilidad demostrada sigue por debajo de la reproducibilidad declarada. En consecuencia, el trabajo ya es defendible como tesis aplicada orientada a un sistema de predicción desplegable, pero todavía no alcanza un cierre académico óptimo para una defensa muy exigente.

## 2. Checklist de cumplimiento estructural

| Componente | Estado | Observación |
|---|---|---|
| Resumen | ✅ Cumple sólido | Presenta problema, enfoque, hallazgo principal y cautelas experimentales en [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md#L3). |
| Introducción | ✅ Cumple sólido | Ya fija pregunta, objetivos, hipótesis, alcance y valor esperado en negocio en [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md#L9). |
| Estado del arte / conceptos teóricos | ⚠️ Cumple con debilidades | Tiene citas y posicionamiento inicial, pero el propio texto admite cobertura parcial de inventarios y reposición en [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L57). |
| Metodología | ⚠️ Cumple con debilidades | El flujo metodológico está bien descrito, aunque algunas decisiones siguen más descritas que justificadas. |
| EDA | ✅ Cumple sólido | Presenta hallazgos, soporte visual integrado y conexión con el problema de negocio. |
| Arquitectura e implementación | ✅ Cumple sólido | Está bien documentada y respaldada por código, artefactos y figura de arquitectura. |
| Experimentos / resultados | 🔶 Cumple parcialmente | Tiene señal cuantitativa favorable y protocolo visible, pero no una comparación métrica homogénea y cerrada en [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md#L55). |
| Validación técnica y reproducibilidad | ⚠️ Cumple con debilidades | Hay evidencia seria de validación software, pero la reproducibilidad demostrada sigue siendo parcial en [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L55). |
| Conclusiones | ✅ Cumple sólido | Responden con prudencia al problema, distinguen límites y no sobreafirman resultados en [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md#L13). |
| Bibliografía y sistema de citas | ⚠️ Cumple con debilidades | Existe aparato bibliográfico funcional, pero el estado del arte todavía necesita ampliación temática. |
| Figuras y tablas | ✅ Cumple sólido | La numeración ya está consolidada y las figuras principales están integradas en el cuerpo del manuscrito. |
| Anexos | ⚠️ Cumple con debilidades | Hay un anexo claro y varios candidatos, pero todavía falta congelar la selección final. |

## 3. Hallazgos por criterio de evaluación

### 3.1 Claridad y relevancia del problema — ⚠️ Cumple con debilidades

**Hallazgos:**
- La formulación central quedó resuelta de forma satisfactoria: la introducción ya fija pregunta de investigación, objetivo general, objetivos específicos, alcance e hipótesis en [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md#L9), [#L11](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md#L11) y [#L13](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md#L13).
- El valor esperado en negocio también quedó mejor formulado en [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md#L11) y [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md#L33), pero todavía se expresa en términos cualitativos y no en indicadores operativos formalizados.

**Acciones correctivas:**
- Mantener la formulación actual de pregunta, objetivos e hipótesis.
- Si se busca un cierre más fuerte, traducir el valor esperado ya formulado en 2 o 3 criterios de negocio explícitos, aunque no medidos empíricamente.

### 3.2 Rigor metodológico — ⚠️ Cumple con debilidades

**Hallazgos:**
- La metodología es coherente con la pregunta planteada y con la estructura del problema, especialmente en la combinación de series multiserie, validación temporal, serving y consistencia entrenamiento-inferencia, tal como se resume en [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md#L15).
- Sin embargo, el manuscrito sigue más fuerte en descripción del pipeline que en justificación de algunas decisiones metodológicas específicas, en particular la selección final de variables y la transición entre datos disponibles y vector de entrada productivo. Esa debilidad no invalida la metodología, pero sí deja espacio para preguntas finas en defensa.

**Acciones correctivas:**
- Reforzar, si se decide un último ajuste, la justificación de inclusión/exclusión de covariables y la racionalidad de algunas decisiones de ingeniería de características.
- No ampliar más la metodología si no se agregará evidencia nueva; en ese caso, conviene sostener el texto actual y defenderlo como metodología aplicada.

### 3.3 Calidad de experimentos y resultados — 🔶 Cumple parcialmente

**Hallazgos:**
- El manuscrito ya puede sostener una señal cuantitativa favorable para `LightGBM`: [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md#L25) y [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md#L13) documentan un `RMSLE = 0.5380629595521763` inferior al de los dos baselines tabulados disponibles.
- El problema central sigue abierto: la comparación no es cerrada ni homogénea. En [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md#L23), [#L39](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md#L39) y [#L55](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md#L55) se reconoce que no hay `MAE`/`RMSE` equivalentes para `LightGBM`, no existe un artefacto exportado de validación cruzada del modelo principal y el baseline visible cubre `97` series mientras que la validación documentada de `LightGBM` se describe sobre `100` series.
- La propia tesis interpreta correctamente ese límite y evita convertir la señal favorable en una afirmación de superioridad global. Esto es un punto fuerte de honestidad académica, pero no resuelve el vacío experimental.

**Acciones correctivas:**
- Decidir explícitamente que la tesis se defenderá como solución aplicada con evidencia cuantitativa parcial, no como benchmark experimental cerrado.
- Si todavía hay margen de trabajo, exportar un artefacto comparable para `LightGBM`; si no lo hay, no forzar afirmaciones más fuertes que las ya presentes.

### 3.4 Solidez teórica y posicionamiento bibliográfico — 🔶 Cumple parcialmente

**Hallazgos:**
- El capítulo teórico ya tiene citas formales, una bibliografía base y articulación razonable con forecasting minorista, modelos globales, ML productivo y ONNX.
- El vacío sigue siendo el mismo, aunque hoy está mejor acotado: [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md#L57) reconoce que el componente de estado del arte todavía es parcial porque no cubre con amplitud suficiente inventarios, stock de seguridad ni métricas orientadas al negocio.

**Acciones correctivas:**
- Ampliar el capítulo con literatura específica de inventarios y reposición si todavía habrá una ronda más de fortalecimiento.
- Si no habrá más expansión bibliográfica, ajustar el discurso del capítulo para presentarlo como marco conceptual suficiente, no como revisión exhaustiva.

### 3.5 Coherencia interna — ✅ Cumple sólido

**Hallazgos:**
- El resumen, la introducción, los experimentos y las conclusiones son coherentes entre sí: [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md#L7), [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md#L55) y [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md#L47) sostienen la misma tesis prudente sobre una señal favorable de `LightGBM` con cierre experimental incompleto.
- La distinción entre hecho observado, interpretación y limitación está mejor cuidada que en muchas tesis aplicadas, lo que reduce riesgos de contradicción interna.

**Acciones correctivas:**
- Mantener la línea actual y evitar introducir frases nuevas que eleven la fuerza de la conclusión cuantitativa.

### 3.6 Reproducibilidad — ⚠️ Cumple con debilidades

**Hallazgos:**
- La tesis documenta bien la reproducibilidad operativa del sistema, su stack de pruebas y sus prerequisitos, en [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L7), [#L13](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L13) y [#L37](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L37).
- La debilidad real sigue estando en la reproducibilidad demostrada: [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L43), [#L45](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L45), [#L47](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L47) y [#L55](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md#L55) dejan claro que no hubo reejecución local de `pytest`, no hay lockfile estricto y la validación fuerte se apoya más en `dummy` que en una corrida productiva completa con Onyx.

**Acciones correctivas:**
- Si habrá defensa técnica, preparar una explicación clara de la diferencia entre reproducibilidad declarada, reproducibilidad operativa y reproducibilidad demostrada.
- Si el tiempo lo permite, conservar una evidencia mínima archivada de corrida productiva real; si no, mantener la formulación actual y no sobreprometer replicabilidad total.

### 3.7 Calidad de escritura y presentación — ✅ Cumple sólido

**Hallazgos:**
- La redacción es sobria, técnicamente precisa y prudente en el uso de afirmaciones.
- La numeración global y el aparato visual ya están consolidados, lo que reduce mucho el riesgo de manuscrito fragmentado.
- La principal mejora pendiente ya no es de escritura, sino de congelamiento editorial final, especialmente en anexos y materiales complementarios.

**Acciones correctivas:**
- Antes de ensamblar la versión final, eliminar cualquier rastro de documento interno de trabajo que no deba ir al manuscrito final.
- Congelar la selección final de anexos para evitar que la tesis parezca todavía en edición.

## 4. Riesgos para defensa

1. ¿Por qué debería considerarse que `LightGBM` mejora a los baselines si la comparación no está cerrada con las mismas métricas ni sobre el mismo universo de series?
   - Debilidad subyacente: evidencia experimental parcial y no homogénea.
2. ¿Cuál es exactamente la contribución académica frente a la literatura previa: un mejor modelo, una mejor arquitectura o una combinación de ambas?
   - Debilidad subyacente: el capítulo experimental es más débil que el capítulo de implementación.
3. ¿Cómo se conecta el sistema con decisiones reales de reposición si la tesis no mide impacto operativo final?
   - Debilidad subyacente: valor de negocio expresado de forma plausible, pero no operacionalizado con indicadores.
4. ¿Qué cubre y qué no cubre el estado del arte si el propio texto reconoce que sigue siendo parcial en inventarios y reposición?
   - Debilidad subyacente: cobertura bibliográfica todavía incompleta en el dominio de negocio.
5. ¿Qué tan reproducible es el sistema completo por un tercero hoy, y qué parte de esa reproducibilidad está realmente demostrada?
   - Debilidad subyacente: brecha entre documentación operativa y reejecución efectiva demostrada.

## 5. Acciones prioritarias antes de entregar

1. **Definir la estrategia de defensa del capítulo experimental**
   - Dónde: [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md) y [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md)
   - Qué hacer: decidir explícitamente si el trabajo se presentará como solución aplicada con evidencia cuantitativa parcial.
   - Por qué: es el punto con mayor capacidad de generar preguntas difíciles.
   - Esfuerzo: Bajo.

2. **Fortalecer o acotar explícitamente el estado del arte**
   - Dónde: [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md)
   - Qué hacer: o bien sumar literatura de inventarios/reposición, o bien declarar con más fuerza que la sección actúa como marco conceptual y no como revisión exhaustiva.
   - Por qué: hoy es el segundo frente académico más débil.
   - Esfuerzo: Medio.

3. **Preparar una defensa oral clara sobre impacto operativo esperado**
   - Dónde: [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md#L11) y [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md#L33)
   - Qué hacer: convertir el valor esperado ya redactado en una respuesta oral breve, concreta y no exagerada.
   - Por qué: el texto ya quedó mejor, pero el tribunal probablemente igual lo pregunte.
   - Esfuerzo: Bajo.

4. **Congelar la selección final de anexos y materiales complementarios**
   - Dónde: [LISTA_DE_ANEXOS.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/LISTA_DE_ANEXOS.md)
   - Qué hacer: dejar solo anexos efectivamente incluidos y suprimir candidatos editoriales.
   - Por qué: evita señales de manuscrito todavía abierto.
   - Esfuerzo: Bajo.

5. **Solo si hay tiempo: cerrar el artefacto faltante de `LightGBM`**
   - Dónde: notebooks y capítulo de experimentos.
   - Qué hacer: exportar CV comparable o asumir definitivamente que no se cerrará.
   - Por qué: es la única acción que puede mejorar de verdad la fuerza cuantitativa del manuscrito.
   - Esfuerzo: Alto.

## 6. Puntaje cualitativo por dimensión

| Dimensión | Evaluación |
|---|---|
| Claridad y relevancia del problema | ⚠️ Cumple con debilidades |
| Rigor metodológico | ⚠️ Cumple con debilidades |
| Calidad de experimentos y resultados | 🔶 Cumple parcialmente |
| Solidez teórica y estado del arte | 🔶 Cumple parcialmente |
| Coherencia interna | ✅ Cumple sólido |
| Reproducibilidad | ⚠️ Cumple con debilidades |
| Escritura y presentación | ✅ Cumple sólido |
| Preparación global para defensa | ⚠️ Cumple con debilidades |

## 7. Veredicto global

La versión actual del manuscrito ya es sustancialmente más defendible que la revisada anteriormente. La formulación académica central quedó cerrada, la conexión con el problema de negocio está mejor explicitada y las conclusiones mantienen un nivel de prudencia adecuado. El manuscrito hoy puede defenderse con seriedad como tesis aplicada centrada en la construcción de una solución de ciencia de datos desplegable para predicción de demanda supermercadista.

Lo que sigue impidiendo un cierre académico más fuerte no es la falta de estructura ni de coherencia, sino el hecho de que los resultados experimentales todavía no constituyen una comparación cuantitativa exhaustiva y de que el estado del arte aún no cubre con igual fuerza el dominio de inventarios y reposición. Por eso, el veredicto final es el siguiente: manuscrito avanzado y defendible, pero todavía no completamente cerrado para una defensa muy exigente sin una estrategia oral clara sobre sus límites.
