# Guía para entender el proyecto

El proyecto propone ayudar a un encargado de entrenamiento de un club a elegir qué familias de aperturas revisar con cada grupo. No presupone que un club real haya validado esa necesidad ni que podamos demostrar mejoras de aprendizaje con estas bases.

## Qué leer primero

El informe PDF de C1 explica el caso completo sin necesitar código. Su notebook muestra cómo se obtienen las cifras. W2 continúa exactamente esa base y agrega muestreo, controles de calidad, auditoría de fugas y separación de datos. Los dos notebooks están en inglés para alinearse con el curso.

## Qué significa una fila

La base principal tiene una fila por partida única. Para mirar la experiencia de blancas y negras creamos dos perspectivas de esa misma partida. No se convierten en dos partidas independientes. Por ejemplo, una victoria blanca vale 1 para blancas y 0 para negras; unas tablas valen 0,5 para cada lado. Por eso juntar todos los colores siempre produce un promedio de 50% y no sirve para decir qué apertura es mejor.

## Qué medimos

El KPI es el promedio de puntos: victorias más media unidad por cada empate, dividido por el total de partidas elegibles del segmento. Cada comparación conserva color, ritmo, tramo de rating y familia de apertura. No es lo mismo que porcentaje de victorias: las tablas aportan medio punto y permanecen en el denominador.

La frecuencia muestra qué aperturas aparecen más en el caso. Los puntos describen qué ocurrió. Ninguna de esas medidas prueba que elegir o estudiar esa apertura cause una mejora. El rival, las preferencias del jugador y muchas decisiones posteriores también intervienen.

## Por qué observamos diez jugadas de cada lado

No se conoce una apertura antes de empezar. Para que el futuro ML tenga sentido fijamos el instante inmediatamente después de la décima jugada de negras. Reproducimos únicamente los primeros 20 movimientos individuales o plies y buscamos posiciones conocidas en un catálogo externo de Lichess. Las transposiciones pueden coincidir aunque se llegue por otro orden.

No usamos la etiqueta de apertura final como predictor: puede describir algo que ocurrió después. Tampoco usamos ganador, cambio final de rating, total de jugadas ni forma de término. Las partidas que no llegan a ese punto o ya tienen un tablero terminal quedan fuera del caso. Eso limita las conclusiones a las partidas que alcanzan el punto de observación.

## Qué tan recientes y representativos son los datos

Los registros son oficiales y corresponden a 2026. Para mantener una descarga reducida y reconstruible se usan ventanas al inicio de julio, agosto y septiembre. No son los meses completos ni una muestra aleatoria de toda la plataforma. Coinciden con horas específicas en UTC y pueden incluir usuarios que juegan repetidamente.

La muestra del 25% de W2 es una segunda selección dentro de ese conjunto disponible. Si reproduce bien el KPI y las proporciones del conjunto, solo demuestra similitud dentro de ese marco. No elimina la falta de otras fechas, horarios, plataformas o jugadores.

## Qué cambia entre C1 y W2

C1 establece la descripción y presenta los resultados sin atribuir causalidad. W2 muestra cómo cambian algunas comparaciones al restringir rivales a diferencias de rating de hasta 100 puntos, además de implementar validación y datos de entrenamiento/prueba. Esa restricción no es un ajuste causal: cambia la población comparada y reduce los casos disponibles.

Entrenamiento corresponde a julio, validación interna a agosto y prueba a septiembre. Las dos perspectivas de una partida siempre conservan el mismo conjunto. El escalador y el codificador de categorías aprenden sus parámetros solo con julio. No se entrenó un modelo predictivo: W2 pide demostrar una estrategia válida, no prometer exactitud.

Septiembre ya aparece en la exploración de C1. Por eso no se presenta como una prueba completamente intacta. Si después entrenan y comparan modelos, habrá que ampliar la cobertura y reservar datos realmente nuevos para una evaluación confirmatoria.

## Límites que debemos poder defender

Los tramos de rating son convenciones del análisis; el rating de Lichess no debe confundirse con una escala idéntica de otra plataforma. Blitz y rapid se mantienen separados. El umbral de 50 partidas evita destacar celdas extremadamente pequeñas, pero no garantiza precisión estadística. Las celdas pequeñas siguen guardadas en las tablas.

Una apertura común puede merecer tiempo de revisión por su frecuencia, aunque no tenga la peor puntuación. Una puntuación baja indica material para investigar, no una apertura intrínsecamente mala. El paso siguiente sería revisar partidas concretas y ampliar la muestra; para demostrar que una sesión funciona se necesitan datos de entrenamiento y seguimiento que aquí no existen.

El paquete conserva C1 como reconstrucción para seguimiento. No dice que el C1 original trataba de ajedrez ni inventa comentarios del profesor o aportes individuales. Cada integrante debe completar su propia revisión en `TEAM_REVIEW.md`.
