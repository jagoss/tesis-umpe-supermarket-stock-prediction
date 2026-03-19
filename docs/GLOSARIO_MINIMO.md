# Glosario mínimo

| Término | Definición operativa en esta tesis |
|---|---|
| `predicción de demanda` | Estimación de ventas futuras a partir de información histórica, usada como apoyo a decisiones de reposición o planificación. |
| `serie temporal multiserie` | Conjunto de múltiples series temporales paralelas, en este caso una por combinación de tienda y familia de producto. |
| `modelo global` | Enfoque en el que un único modelo aprende conjuntamente sobre múltiples series, en lugar de entrenar un modelo separado para cada una. |
| `baseline` | Modelo de referencia utilizado para contextualizar el desempeño del modelo principal. |
| `horizonte de predicción` | Cantidad de períodos futuros que el modelo intenta estimar en cada corrida de pronóstico. |
| `validación temporal` | Estrategia de evaluación que respeta el orden cronológico y evita usar información futura durante el entrenamiento. |
| `rezago (lag)` | Valor histórico de una variable observado en períodos anteriores y usado como predictor. |
| `ingeniería de características` | Proceso de construcción de variables derivadas a partir de datos originales para mejorar la capacidad predictiva del modelo. |
| `escalado local por serie` | Estandarización aplicada individualmente a cada serie para reducir diferencias de escala entre combinaciones de tienda y familia. |
| `serving de modelos` | Conjunto de componentes y procesos que permiten ejecutar un modelo entrenado en un entorno de inferencia operativo. |
| `pre-cómputo de características` | Generación offline de variables de entrada para reutilizarlas en producción sin recalcularlas en cada solicitud. |
| `consistencia entre entrenamiento e inferencia` | Correspondencia entre las transformaciones, el orden y el significado de las variables usadas al entrenar el modelo y al consumirlo en producción. |
| `artefacto ONNX` | Archivo exportado en formato interoperable que contiene el modelo listo para ser ejecutado por un runtime compatible. |
| `pipeline` | Secuencia organizada de pasos de preparación, transformación, modelado y despliegue. |
| `reproducibilidad operativa` | Capacidad de reinstalar el entorno, reejecutar procesos y verificar el funcionamiento técnico del sistema con condiciones documentadas. |

## Criterio de uso

- Este glosario no pretende ser enciclopédico; solo fija el sentido operativo de términos que aparecen repetidamente en el manuscrito.
- Las definiciones están redactadas según el uso efectivo del proyecto y no como definiciones universales del área.
- Si el manuscrito final incorpora nuevos conceptos centrales, conviene ampliar este glosario y mantenerlo alineado con la terminología de [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md), [metodologia.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/metodologia.md), [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md) y [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md).
