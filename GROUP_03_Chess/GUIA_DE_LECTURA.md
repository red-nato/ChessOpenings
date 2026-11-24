# Guía de lectura · C3

La pregunta es qué partidas debería revisar primero un club con tiempo limitado. El [README final](../README.md) enlaza la presentación, identifica la versión evaluada y ordena los notebooks. Sus tablas y figuras se pueden leer directamente en GitHub.

1. [C1 · Exploración](notebooks/C1_openings.ipynb). De 153.817 registros de origen quedan 86.950 partidas únicas y 140 familias de aperturas. La apertura se reconoce con una secuencia por partida, que incluye las jugadas de ambos colores hasta el ply 20.
2. [W2 · Preparación](notebooks/W2_project.ipynb). Julio, agosto y septiembre se separan por ID de partida y fecha UTC. Las dos perspectivas de una misma partida heredan esa separación. Los parámetros de preparación se aprenden con julio.
3. [C2 · Modelo y referencia](notebooks/C2_clustering.ipynb). K-prototypes agrupa perspectivas jugador-partida. El resultado de la partida se utiliza después del ajuste para describir los grupos. La referencia manual usa ritmo y tramo de rating focal. Ambas lecturas comparan puntuación por color sobre las mismas perspectivas de septiembre. El [anexo de aperturas](notebooks/C2_clustering_anexo_aperturas.ipynb) utiliza familias como unidad.
4. [W3/C3 · Figuras y decisión](notebooks/C3_final_visualizations.ipynb). El máximo de la regla manual es +4,62 pp en Blitz 2000+. La familia Siciliana ofrece 255 derrotas blancas en 556 partidas, material para una primera sesión. El cierre incluye los denominadores, el agregado `Other` y las sensibilidades.

La puntuación es (victorias + 0,5 × tablas) / observaciones de la celda. En las comparaciones por rating focal, ambos colores pueden contener distintas partidas. La recomendación es exploratoria porque se seleccionó a partir de septiembre, un tramo ya observado en C1. El estudio describe ventanas breves y no mide el efecto de entrenar una apertura.

El [registro de decisiones](DECISION_LOG.md) vincula las cifras con su preparación y los cambios a partir de la retroalimentación. La [revisión de equipo](TEAM_REVIEW.md) recoge los aportes registrados y el uso de IA.
