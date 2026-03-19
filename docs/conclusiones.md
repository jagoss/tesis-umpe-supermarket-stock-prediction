# Conclusiones

## Síntesis de los hallazgos principales

La evidencia consolidada en esta tesis permite sostener que el proyecto logró materializar una solución aplicada de ciencia de datos orientada a la predicción de demanda en supermercados sobre un problema multiserie de ventas diarias por tienda y familia de producto. En términos observables, el trabajo no se limitó al entrenamiento de un modelo experimental, sino que integró un pipeline completo de preparación de datos, ingeniería de características, validación temporal, exportación del modelo a `ONNX` y exposición del servicio de inferencia mediante API REST y `MCP`, con integración prevista hacia un entorno conversacional basado en Onyx.

Desde el punto de vista metodológico, el repositorio demuestra la construcción de un enfoque global basado en `LightGBM` y `MLForecast`, sustentado en rezagos temporales, variables de calendario, promociones, feriados y escalado local por serie. Esta formulación es coherente con la estructura del problema y con el análisis exploratorio realizado, que mostró heterogeneidad entre series, presencia de ceros estructurales, relevancia descriptiva de promociones y efectos de calendario que justifican la incorporación de variables temporales y festivas en el modelo.

Desde el punto de vista de ingeniería, el proyecto también deja una contribución concreta. La solución implementada desacopla dominio, aplicación, infraestructura e interfaz, utiliza artefactos `Parquet` para preprocesamiento productivo, despliega el modelo en formato `ONNX` y lo integra en un servicio validado por pruebas, smoke tests y documentación operativa. Esta evidencia permite afirmar que el trabajo aborda el problema no solo como ejercicio de forecasting, sino como construcción de un sistema técnicamente desplegable para apoyar un caso de negocio realista. En ese sentido, la tesis aporta tanto un pipeline analítico como una arquitectura operativa, una combinación consistente con enfoques de sistemas ML productivos donde la utilidad práctica depende de la integración entre modelo, datos e infraestructura (Sculley et al., 2015; Breck et al., 2017).

## Respuesta prudente al problema planteado

Sobre la base de la evidencia preservada en el repositorio, puede sostenerse que el trabajo construyó una solución técnicamente consistente para apoyar tareas de predicción de demanda o reposición en un contexto supermercadista. También puede sostenerse que el modelo principal `LightGBM` fue efectivamente entrenado y evaluado bajo validación temporal, y que el repositorio conserva un `RMSLE = 0.5380629595521763` visible en el output embebido del notebook académico. Este valor es inferior a los `RMSLE` observados en los dos baselines tabulados disponibles (`SeasonalNaive` y `AutoETS`), lo que constituye una señal favorable para el modelo principal.

Sin embargo, esa señal no debe confundirse con una demostración concluyente de superioridad global del enfoque. La conclusión defendible no es que el modelo final haya quedado cuantitativamente probado de manera exhaustiva frente a todas las alternativas, sino que el repositorio conserva evidencia suficiente para afirmar una mejora parcial en `RMSLE` y una implementación más madura desde el punto de vista operativo que la de un experimento aislado de notebook. En consecuencia, la hipótesis de trabajo puede considerarse respaldada de forma parcial: el proyecto demuestra viabilidad técnica y una señal empírica favorable, pero no un cierre experimental completamente homogéneo y reproducible en todas las métricas relevantes.

## Limitaciones que condicionan la interpretación

La primera limitación crítica es la ausencia de un artefacto tabular exportado de validación cruzada para `LightGBM`, equivalente a [cv_results_baseline_retrained.csv](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.notebooks/cv_results_baseline_retrained.csv). Esto impide recomputar o auditar con la misma facilidad los resultados del modelo principal fuera del output embebido del notebook.

La segunda limitación es que, en ausencia de ese artefacto, no quedan trazables con el mismo nivel de detalle métricas adicionales como `MAE`, `RMSE` ni el comportamiento por `cutoff` o ventana temporal del modelo `LightGBM`. Por lo tanto, la comparación experimental solo puede sostenerse hoy en `RMSLE`, no en un conjunto métrico completo.

La tercera limitación es que la comparación actualmente visible no es perfectamente homogénea en alcance. El artefacto baseline auditado cubre 97 series, mientras que la validación documentada de `LightGBM` se describe sobre un subconjunto de 100 series. Esto obliga a interpretar la mejora observada en `RMSLE` como una evidencia parcial y no como una comparación cerrada sobre exactamente el mismo universo experimental.

Estas tres limitaciones no invalidan el valor del trabajo, pero sí condicionan el nivel de fuerza con el que pueden formularse las conclusiones cuantitativas. La tesis, por tanto, debe distinguir con claridad entre hecho observado, interpretación razonable y afirmación que todavía requeriría evidencia adicional.

## Implicancias para el problema de negocio

Pese a esas restricciones, el trabajo deja una base sólida para un caso de uso de negocio centrado en apoyo a decisiones de reposición. El repositorio muestra que es posible combinar datos históricos públicos, ingeniería de características temporalmente consistente, un modelo global de boosting y una arquitectura de serving preparada para integrarse con interfaces conversacionales. En términos aplicados, esto significa que la solución ya no depende exclusivamente de una etapa exploratoria o experimental, sino que puede ser pensada como un componente reutilizable dentro de un flujo operativo más amplio.

La implicancia principal es que el valor del proyecto no reside únicamente en la reducción observada de una métrica respecto de los baselines, sino en haber llevado ese enfoque hasta una implementación técnicamente integrable. Para un escenario de negocio, esta combinación es relevante porque una mejora predictiva solo resulta útil si puede transformarse en un servicio accesible, trazable y razonablemente reproducible.

En términos operativos, la utilidad esperada de una solución de este tipo radica en ofrecer mejores insumos para decidir cuánto reponer, dónde priorizar revisión de demanda y cómo anticipar con mayor consistencia variaciones entre tiendas y familias de producto. Dicho de otro modo, el aporte esperado no debe interpretarse como una promesa ya verificada de reducción de quiebres o sobrestock, sino como la disponibilidad de una capacidad analítica y técnica que puede servir de apoyo a esas decisiones. Esta distinción es importante porque el repositorio demuestra la viabilidad del sistema y una señal cuantitativa favorable del modelo principal, pero no una medición directa del impacto operativo final sobre el negocio.

## Líneas de mejora y trabajo futuro

La mejora más importante y directa consiste en exportar un artefacto de validación cruzada completo para `LightGBM`, de modo que la comparación frente a los baselines pueda realizarse con `RMSLE`, `MAE`, `RMSE` y detalle por ventana sobre un mismo conjunto de series. Este paso permitiría convertir la señal favorable actual en una evaluación cuantitativa mucho más robusta.

Una segunda línea de mejora consiste en homogeneizar por completo el alcance experimental, asegurando que baselines y modelo principal sean evaluados exactamente sobre el mismo subconjunto de series, horizonte y cortes temporales. Esto cerraría una fuente de ambigüedad importante en la interpretación de resultados.

Una tercera línea de trabajo es reforzar la reproducibilidad del proyecto mediante corrección del notebook académico, congelamiento más estricto de dependencias y archivado de corridas productivas completas del stack con Onyx. Esto no solo fortalecería la tesis como documento académico, sino también la mantenibilidad futura del sistema.

Finalmente, desde una perspectiva aplicada, sería valioso extender la evaluación hacia métricas o criterios más próximos al negocio, por ejemplo asociados a error operativo de reposición, sensibilidad a quiebre de stock o robustez por familia y tienda. Esa ampliación permitiría conectar de manera más directa el desempeño predictivo con decisiones concretas de inventario.

## Cierre

En síntesis, la tesis permite concluir que el proyecto alcanzó una base metodológica y de ingeniería suficientemente sólida para demostrar viabilidad técnica en la predicción de demanda supermercadista y su integración en un sistema desplegable. La evidencia preservada en el repositorio respalda una mejora parcial del modelo `LightGBM` en `RMSLE` respecto de los baselines disponibles y documenta una arquitectura operativa consistente con el objetivo aplicado del trabajo. Al mismo tiempo, las limitaciones identificadas impiden presentar esa mejora como una validación cuantitativa exhaustiva y completamente homogénea. La conclusión más rigurosa, por tanto, es que el trabajo cumple de manera convincente como prueba de concepto aplicada y como base documental robusta para una solución productiva, pero todavía requiere un cierre experimental más completo para sostener afirmaciones cuantitativas finales con menor ambigüedad.
