# Numeración global del manuscrito

Este documento fija la numeración de referencia para la versión simplificada y pre-entregable del manuscrito en Markdown.

## 1. Estructura general

### 1.1 Elementos preliminares sin numeración visible

- Portada
- Página de aprobación
- Fe de erratas
- Descargo de responsabilidad
- Dedicatoria y agradecimientos
- Cláusula de confidencialidad
- Tabla de contenido o índice
- Lista de tablas
- Lista de figuras
- Lista de abreviaturas y siglas
- Lista de símbolos
- Glosario
- Resumen
- Palabras clave

### 1.2 Capítulos principales numerados

1. `1. Introducción`
2. `2. Estado del arte`
3. `3. Metodología`
4. `4. Análisis exploratorio de datos (EDA)`
5. `5. Arquitectura e implementación del sistema`
6. `6. Experimentos`
7. `7. Validación técnica y reproducibilidad`
8. `8. Conclusiones`
9. `9. Referencias bibliográficas`
10. `10. Anexos y material complementario`

## 2. Correspondencia entre capítulos y archivos

| Numeración final | Sección | Archivo base |
|---|---|---|
| `Resumen` | Resumen | [resumen.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/resumen.md) |
| `1` | Introducción | [introduccion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/introduccion.md) |
| `2` | Estado del arte | [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md) |
| `3` | Metodología | [metodologia.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/metodologia.md) |
| `4` | EDA | [eda.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/eda.md) |
| `5` | Arquitectura e implementación del sistema | [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md) |
| `6` | Experimentos | [experimentos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/experimentos.md) |
| `7` | Validación técnica y reproducibilidad | [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md) |
| `8` | Conclusiones | [conclusiones.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/conclusiones.md) |
| `10 / Anexo A` | Reejecución y validación operativa del entorno | [anexo_reproducibilidad_operativa.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/anexo_reproducibilidad_operativa.md) |

## 3. Numeración global de tablas

1. `Tabla 1. Métricas recuperables para los modelos comparados.`
   Ubicación: `6. Experimentos`

## 4. Numeración global de figuras

1. `Figura 1. Ventas promedio, promociones, transacciones y petróleo.`
   Ubicación: `4. Análisis exploratorio de datos (EDA)`
2. `Figura 2. Distribución de ventas en festividades nacionales.`
   Ubicación: `4. Análisis exploratorio de datos (EDA)`
3. `Figura 3. Distribución de ventas en festividades regionales.`
   Ubicación: `4. Análisis exploratorio de datos (EDA)`
4. `Figura 4. Distribución de ventas en festividades locales.`
   Ubicación: `4. Análisis exploratorio de datos (EDA)`
5. `Figura 5. Patrones de ventas por variables de calendario.`
   Ubicación: `4. Análisis exploratorio de datos (EDA)`
6. `Figura 6. Arquitectura vigente del sistema de predicción e integración con Onyx.`
   Ubicación: `5. Arquitectura e implementación del sistema`

## 5. Numeración global de anexos

- `Anexo A. Reejecución y validación operativa del entorno.`

## 6. Regla editorial de mantenimiento

- Los preliminares quedan fuera de la numeración capitular visible.
- La numeración del cuerpo principal queda fijada de `1` a `10`.
- La numeración de figuras queda congelada en `Figura 1` a `Figura 6` mientras no se incorporen nuevas figuras al cuerpo principal.
- La numeración de tablas queda congelada en `Tabla 1` mientras no se integren nuevas tablas al manuscrito.
- Si se agrega una nueva figura, tabla o anexo al cuerpo principal, este documento debe actualizarse antes de tocar referencias cruzadas.
