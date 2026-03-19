# Bibliografía semilla

Objetivo: reunir una base mínima de referencias externas confiables para sostener el capítulo [estado_arte_conceptos.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/estado_arte_conceptos.md) y futuras citas del manuscrito.

Criterio:
- solo fuentes primarias o documentación oficial;
- sin inventar DOI, venue o paginación;
- formato provisional en Markdown mientras se define el estilo final de citas.

Artefacto complementario ya disponible:
- [references_seed.bib](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/references_seed.bib): subconjunto en BibTeX de las obras efectivamente citadas en el manuscrito actual, pensado para posterior depuración según el estilo institucional.

## 1. Literatura académica núcleo

1. Breck, E., Cai, S., Nielsen, E., Salib, M., & Sculley, D. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction*. Proceedings of IEEE Big Data (2017).  
   URL: [https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

2. Fildes, R., Ma, S., & Kolassa, S. (2022). *Retail forecasting: Research and practice*. International Journal of Forecasting, 38(4), 1283-1318. DOI: `10.1016/j.ijforecast.2019.06.004`.  
   URL: [https://ideas.repec.org/a/eee/intfor/v38y2022i4p1283-1318.html](https://ideas.repec.org/a/eee/intfor/v38y2022i4p1283-1318.html)

3. Fildes, R., Kolassa, S., & Ma, S. (2022). *Post-script—Retail forecasting: Research and practice*. International Journal of Forecasting, 38(4), 1319-1324. DOI: `10.1016/j.ijforecast.2021.09.012`.  
   URL: [https://pmc.ncbi.nlm.nih.gov/articles/PMC9534457/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9534457/)

4. Hewamalage, H., Bergmeir, C., & Bandara, K. (2020). *Global Models for Time Series Forecasting: A Simulation Study*. arXiv:2012.12485.  
   URL: [https://arxiv.org/abs/2012.12485](https://arxiv.org/abs/2012.12485)

5. Huber, J., & Stuckenschmidt, H. (2020). *Daily retail demand forecasting using machine learning with emphasis on calendric special days*. International Journal of Forecasting, 36(4), 1420-1438. DOI: `10.1016/j.ijforecast.2020.02.005`.  
   URL: [https://www.sciencedirect.com/science/article/pii/S0169207020300224](https://www.sciencedirect.com/science/article/pii/S0169207020300224)

6. Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). *LightGBM: A Highly Efficient Gradient Boosting Decision Tree*. Advances in Neural Information Processing Systems 30 (NeurIPS 2017).  
   URL: [https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html](https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html)

7. Montero-Manso, P., & Hyndman, R. J. (2021). *Principles and algorithms for forecasting groups of time series: locality and globality*. International Journal of Forecasting, 37(4), 1632-1653. DOI: `10.1016/j.ijforecast.2021.03.004`.  
   URL: [https://research.monash.edu/en/publications/principles-and-algorithms-for-forecasting-groups-of-time-series-l/](https://research.monash.edu/en/publications/principles-and-algorithms-for-forecasting-groups-of-time-series-l/)

8. Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F., & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems*. NeurIPS 2015.  
   URL: [https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf](https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)

## 2. Documentación oficial técnica

9. Nixtla. *MLForecast Documentation*. Documentación oficial.  
   URL: [https://nixtlaverse.nixtla.io/mlforecast/core.html](https://nixtlaverse.nixtla.io/mlforecast/core.html)

10. Nixtla. *Statistical, Machine Learning and Neural Forecasting methods*. Documentación oficial / tutorial.  
    URL: [https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/statisticalneuralmethods.html](https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/statisticalneuralmethods.html)

11. ONNX. *Overview*. Documentación oficial de ONNX 1.22.0.  
    URL: [https://onnx.ai/onnx/repo-docs/Overview.html](https://onnx.ai/onnx/repo-docs/Overview.html)

## 3. Uso sugerido por tema

- demanda y forecasting minorista:
  `Fildes et al. (2022)`, `Fildes et al. (2022, post-script)`, `Huber & Stuckenschmidt (2020)`
- modelos globales para múltiples series:
  `Hewamalage et al. (2020)`, `Montero-Manso & Hyndman (2021)`, documentación `MLForecast`
- algoritmo base del modelo implementado:
  `Ke et al. (2017)`
- consistencia entre entrenamiento e inferencia y robustez de sistemas ML:
  `Sculley et al. (2015)`, `Breck et al. (2017)`
- interoperabilidad y serving:
  documentación oficial `ONNX`

## 4. Vacíos que siguen abiertos

- ya existe un archivo BibTeX semilla, pero todavía no está depurado como bibliografía final citada;
- aún falta decidir el estilo bibliográfico final de la tesis;
- no se incorporó literatura específica sobre inventarios, seguridad de stock o métricas de forecast aplicadas al negocio;
- la página oficial del desafío de Kaggle no resultó utilizable desde el navegador de esta auditoría por errores de anti-forgery token, por lo que no se incluyó como referencia primaria externa en esta semilla.
