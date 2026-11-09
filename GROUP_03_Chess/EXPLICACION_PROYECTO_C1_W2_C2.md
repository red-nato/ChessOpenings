# De C1 a C2: cómo pensar y defender este proyecto, explicado de a poco

*Documento interno del equipo (Javier Alcaíno, Lucas Riquelme, Renato Varela). No es el brief del profesor ni el PDF de 3 páginas que exige el curso — es la explicación que nos preparamos a nosotros mismos, de lo más simple a lo más técnico, para poder defender el proyecto completo (C1 → W2 → C2) sin depender de IA durante la defensa oral.*

> Documento completo. Las secciones 5 a 8 reflejan los números reales obtenidos al ejecutar `notebooks/C2_clustering.ipynb` — si vuelven a correr el notebook y los números cambian (por ejemplo, si cambian la semilla o los datos), hay que actualizar esta sección para que coincida, porque la rúbrica penaliza que los archivos entregados no concuerden entre sí.

---

## 1. La decisión de negocio, en una frase

Un coordinador de entrenamiento de un club de ajedrez (un perfil que nosotros proponemos, no alguien que realmente validó esto) tiene que decidir **qué aperturas revisar primero con cada grupo de jugadores**, según si juegan con blancas o negras, a qué ritmo (blitz o rapid) y en qué nivel de rating están. No tiene tiempo para revisar las 140 familias de apertura que aparecen en los datos; necesita un criterio para priorizar.

Todo el proyecto — C1, W2 y ahora C2 — es, en el fondo, intentar responder esa misma pregunta de formas cada vez más cuidadosas, nunca una pregunta distinta.

## 2. El KPI: qué medimos y, sobre todo, qué NO significa

Medimos **puntos por partida**: una victoria vale 1 punto, un empate vale 0.5 y una derrota vale 0. Promediamos esos puntos dentro de un grupo (por ejemplo, "blancas, blitz, rating 1600-1999, Defensa Siciliana") para obtener una tasa de puntaje entre 0 y 1.

**Analogía simple:** es como el promedio de notas de un curso, pero donde "notas altas" significa "ganó más seguido en ese grupo específico". No es el porcentaje de victorias ignorando los empates, y no es una probabilidad calibrada de ganar la próxima partida.

**Lo más importante — y la fuente de casi todas las advertencias que vamos a repetir en este documento:** este número es puramente **descriptivo**. No prueba que:
- jugar con un color específico "cause" ganar más;
- estudiar una apertura específica mejore el resultado de un jugador;
- un jugador que aparece en un grupo con puntaje bajo "juega mal" esa apertura.

¿Por qué no? Porque **nadie fue asignado al azar** a jugar blancas o negras, a elegir blitz o rapid, o a abrir con la Siciliana en vez de la Francesa. Cada jugador *elige* (o termina jugando, según el emparejamiento) esas condiciones según su nivel, su estilo y su preparación. Si un grupo tiene mejor puntaje, puede ser simplemente porque los jugadores de rating más alto eligen más esa apertura — no porque la apertura "sea mejor". Esto es exactamente lo que en el curso se llama el problema de que **la correlación no es causalidad**: sin un experimento donde alguien fuerza al azar quién juega qué apertura, no podemos separar "el efecto de la apertura" del "efecto de quién elige esa apertura".

## 3. Qué pasó entre C1 y W2 (de describir a poder confiar en lo que describimos)

**C1** fue la primera mirada: tomamos 86.950 partidas de Lichess (julio, agosto y septiembre de 2026), las limpiamos, y calculamos el KPI de puntos por grupo. Mostramos, por ejemplo, que la Defensa Siciliana es la apertura más frecuente, y que la ventaja de blancas es pequeña (~51% de puntaje) y está muy ligada a la diferencia de rating entre los dos jugadores (Spearman = 0.149 entre diferencia de rating y puntaje — una asociación débil-moderada, nunca causal).

**W2** se preguntó algo distinto y más incómodo: *¿podemos confiar en que estos números seguirían siendo parecidos si entrenáramos un modelo con ellos?* Para eso hay que evitar lo que el curso llama **fuga de datos (leakage)** — usar, sin darse cuenta, información que en la vida real no estaría disponible en el momento de la predicción.

**Ejemplo cotidiano de fuga de datos:** imagina que quieres predecir si un estudiante aprobará el curso, y usas como variable de entrada "la nota final del estudiante". Por supuesto que vas a "predecir" perfecto — pero es un engaño, porque esa nota final es justamente lo que querías predecir, no algo que conocías antes. En nuestro caso, cosas como el resultado final de la partida, la etiqueta de apertura calculada *después* de toda la partida, o el cambio de rating posterior, son ese tipo de información "del futuro" que W2 identificó y excluyó explícitamente de los predictores.

W2 también **congeló un contrato de datos**: entrenamos (ajustamos el escalador y el codificador) solo con julio, y usamos agosto para revisar decisiones y septiembre — que ya habíamos mirado parcialmente en C1 — como una prueba final que tratamos con cuidado. Esto es exactamente la misma lógica de "no mirar la prueba antes de rendirla": si ajustas tus herramientas de medición mirando las respuestas del examen, el examen ya no mide nada confiable.

W2 dejó, a propósito, dos preguntas sin responder — simplemente las dejó anotadas como "esto podría ser un problema, pero no lo arreglamos todavía":
1. **3.112 jugadores** aparecen tanto en julio (entrenamiento) como en septiembre (prueba). Si un modelo "aprende" algo sobre esos jugadores específicos en julio, parte de lo que parece "generalizar bien" en septiembre podría ser simplemente que ya conocía a esos jugadores — no que el patrón generalice a gente nueva.
2. Los "meses" de julio/agosto/septiembre en realidad no son meses completos: son ventanas de apenas **35 a 45 minutos** justo a la medianoche UTC del día 1 de cada mes (una limitación técnica de cómo se descargaron los datos). Eso significa que nuestras conclusiones podrían depender de qué momento exacto del día/mes se haya elegido para extraer los datos, no de un patrón mensual real.

C2 retoma exactamente esas dos preguntas abiertas y las convierte en análisis explícitos (ver sección 7).

## 4. Por qué C2 usa clustering y no "predecir quién gana"

El profesor permite elegir entre tres caminos para C2: predecir un número (regresión), predecir una categoría (clasificación), o explorar grupos (clustering). C1 y W2 habían dejado la puerta abierta a clasificación (predecir victoria/empate/derrota de blancas apenas termina la jugada 10 de negras), pero decidimos **no tomar ese camino**, por una razón muy concreta y ya demostrada en nuestros propios datos:

> **Predecir quién gana usando solo color + apertura + rating + ritmo es una señal débil.** El propio C1 ya mostró que la correlación entre la diferencia de rating y el resultado es de solo 0.149 (en una escala de -1 a 1), y que el rating de un jugador solo, sin comparar con el rival, casi no predice nada (correlación ~0.03). Construir un clasificador con esas variables nos daría, probablemente, un modelo que apenas le gana a "siempre predecir empate con blancas ganando un poco más" — poco interesante y poco útil para el coordinador del club.

En cambio, el clustering nos permite hacer una pregunta distinta y más honesta con lo que los datos realmente pueden responder: **¿existen grupos de comportamiento reconocibles combinando color, apertura, rating y ritmo, que le sirvan al coordinador para organizar su trabajo** — aunque esos grupos no "predigan" el resultado de la próxima partida con precisión? Es la diferencia entre decir "no puedo decirte quién va a ganar" (clasificación débil) y decir "sí puedo decirte qué tipos de partidas se parecen entre sí y cómo se comportan en promedio" (clustering descriptivo). Esta decisión en sí es una aplicación directa de algo que el curso insiste mucho: **elegir el modelo según la pregunta que los datos pueden responder de forma defendible, no según cuál modelo es más sofisticado.**

---

## 5. Qué es "Gower / k-prototypes", explicado simple antes de las fórmulas

Imaginemos 4 partidas de juguete, cada una descrita por: color, ritmo (blitz/rapid) y rating propio.

| Partida | Color | Ritmo | Rating |
|---|---|---|---|
| A | Blancas | Blitz | 1900 |
| B | Negras | Blitz | 1880 |
| C | Blancas | Rapid | 1300 |
| D | Negras | Rapid | 1250 |

Si quisiéramos agrupar estas 4 filas "a ojo", diríamos que A y B se parecen (mismo ritmo, rating parecido) y C y D se parecen entre sí — aunque A y B tengan colores distintos, y C y D también. **El color es, en este ejemplo, la variable que MENOS ayuda a decidir el grupo** — el ritmo y el rating "pesan más" para saber a qué grupo pertenece cada fila.

Eso es exactamente lo que el algoritmo **k-prototypes** hace de forma automática y a mayor escala: mide qué tan "lejos" está cada fila de un grupo usando dos reglas a la vez — para los números (rating, segundos de reloj) usa la distancia normal tipo regla ("¿cuánto más alto es un rating que otro?"), y para las categorías (color, ritmo, apertura) usa una regla más simple: "¿es la misma categoría o no?" (0 si es igual, 1 si es distinta). Esta combinación numérico + categórico se llama una **distancia de Gower**, y un peso llamado **gamma (γ)** decide cuánto importa cada tipo de diferencia. Elegimos usar la fórmula estándar que recomienda el propio algoritmo (no inventamos un peso "a mano"), tal como permite el profesor ("un modelo simple es suficiente").

**¿Por qué no usamos K-means normal, el más conocido?** Porque K-means solo entiende números. Si le diéramos las 140 familias de apertura como si fueran números (una técnica común llamada "one-hot encoding"), terminaríamos con 140 columnas casi todas en cero, y K-means mediría mal las distancias — como comparar dos ciudades por código postal numérico en vez de por su ubicación real. K-prototypes evita ese problema tratando las categorías como categorías, no como números disfrazados.

**¿Cuántos grupos (K) elegimos?** Probamos de 3 a 8 grupos y nos quedamos con el que mejor separaba los datos según una medida llamada *silhouette* (qué tan "cómoda" está cada fila en su grupo comparado con el grupo más cercano). El resultado fue **K = 4**.

## 6. Qué mostraron los resultados

Con K=4, los grupos que aparecieron fueron:

| Grupo | Tamaño (test, sept.) | Ritmo dominante | Rating promedio | Apertura más común |
|---|---|---|---|---|
| 0 | 25.929 (42%) | Blitz (98%) | ~1.883 | Defensa Siciliana |
| 1 | 12.002 (20%) | Rapid (0%) | ~1.439 | Apertura de Peón de Dama |
| 2 | 20.224 (33%) | Blitz (99%) | ~1.287 | Apertura de Peón de Dama |
| 3 | 2.951 (5%) | Rapid (1%) | ~1.432 | Apertura de Peón de Dama |

**Primera sorpresa (importante):** si miramos el puntaje promedio de cada grupo mezclando blancas y negras, da casi exactamente 50% en los cuatro grupos — parecería que "no hay ningún patrón". **Pero esto es un espejismo matemático, no un resultado real.** Descubrimos que en el 95,3% de las partidas de prueba, la perspectiva de blancas y la de negras de la MISMA partida terminan en el MISMO grupo. Y como el puntaje de blancas más el de negras siempre suma exactamente 1 (si uno gana 1, el otro saca 0; si empatan, 0,5 y 0,5), cualquier grupo que junte casi siempre a ambos lados de la misma partida va a promediar 50% sí o sí — sin importar si el color realmente influye o no. Es como preguntarle a una pareja de baile, por separado, "¿quién bailó mejor?", promediar sus respuestas, y sorprenderse de que da "empate": por supuesto que da empate, porque es la misma pareja respondiendo sobre el mismo baile.

**Por eso separamos el puntaje por color dentro de cada grupo**, y ahí sí aparece un patrón real y consistente: en los tres grupos grandes (más del 95% de los datos), blancas obtiene entre **2,0 y 2,9 puntos porcentuales más** que negras. En el grupo más chico (5% de los datos), esa diferencia prácticamente desaparece (-0,17 puntos). Esto es coherente con lo que ya sabíamos desde C1: hay una pequeña ventaja de jugar con blancas, del orden de un par de puntos porcentuales.

**Comparación con la regla simple del club** (agrupar solo por color × ritmo × tramo de rating, sin apertura): esa regla, al mantener separados los 4 tramos de rating, detecta una diferencia máxima de **4,62 puntos porcentuales** — más grande que cualquiera de nuestros 4 grupos — concentrada específicamente en jugadores de blitz con rating 2000+. Dicho de forma simple: **la regla manual, al no "mezclar" tanto los tramos de rating, ve con más detalle dónde es más grande la ventaja de blancas; el clustering, al agrupar de forma más compacta, entrega un resumen más simple pero pierde algo de esa resolución.** Esto no significa que el clustering "no sirva" — significa que agrupar siempre implica un costo: se gana simplicidad, se pierde detalle, y hay que decirlo con todas sus letras en la defensa.

## 7. Las dos sensibilidades: ¿qué tan frágil es esta conclusión?

**Sensibilidad a la ventana/mes:** revisamos si el tamaño y la composición de cada grupo cambiaban mucho entre julio, agosto y septiembre. El resultado fue tranquilizador: cada grupo mantuvo prácticamente el mismo tamaño relativo (variación máxima de 1,2 puntos porcentuales) y el mismo perfil de rating/ritmo en los tres meses. Esto es evidencia a favor de que los grupos encontrados no son un accidente de cuál ventana de 40 minutos se usó — aunque, ojo, esto no dice nada sobre si julio/agosto/septiembre representan bien otros horarios o días (esa limitación, heredada de W2, sigue intacta).

**Sensibilidad a jugadores repetidos:** acá encontramos algo más dramático. Construimos un "mapa de conexiones" entre jugadores: cada jugador es un punto, y cada partida dibuja una línea entre los dos jugadores que la jugaron. Si seguimos esas líneas de jugador en jugador, el **74,5% de todos los jugadores (y el 84,5% de todas las partidas) terminan conectados en un solo gran grupo conectado** — como si casi todo el mundo del blitz/rapid de esos momentos fuera, en el fondo, "una sola red" de rivales que se cruzan una y otra vez. Esto significa que **no es posible dividir los datos en un entrenamiento y una prueba que no compartan absolutamente ningún jugador**, sin tirar a la basura la enorme mayoría de los datos. Ese resultado — "no se puede separar limpiamente" — es en sí mismo un hallazgo honesto, no un fracaso del análisis.

Como alternativa más realista, miramos específicamente las partidas de septiembre donde **ninguno de los dos jugadores** había aparecido en julio (77,8% de las partidas de septiembre cumplen esto). Ahí, el patrón de "blancas ganan un par de puntos porcentuales más" se mantuvo prácticamente igual (por ejemplo, el grupo 0 pasó de +2,87 a +2,13 puntos porcentuales). Es decir: la conclusión principal no depende de que haya jugadores repetidos entre julio y septiembre.

## 8. Límites finales y la advertencia causal, conectados con la teoría del curso

- **Límite metodológico propio del diseño:** el mismo diseño de clustering (una fila por jugador-partida, con rating propio/rival) hace que las dos perspectivas de una misma partida sean casi "gemelas" en el espacio de variables, por lo que el algoritmo casi siempre las junta en el mismo grupo. Esto es justamente el concepto de **fuga de información estructural**: no es que alguien haya cometido un error de código, es que la forma en que se construyeron las variables empuja el resultado agregado hacia 50%, y hay que revisar el "por qué" antes de confiar en un número que se ve demasiado limpio — la misma lección que W2 ya enseñaba sobre fuga de datos, aplicada ahora a un problema distinto (clustering en vez de clasificación).
- **Posible mejora:** dar al color un peso propio y distinto al de ritmo/apertura en la distancia (en vez de compartir un solo gamma), o agrupar por separado las filas de blancas y las de negras, para que el color sí pueda influir en a qué grupo pertenece una fila, no solo aparecer después como una división manual.
- **Sin causalidad, otra vez:** ni la ventaja de blancas, ni las diferencias entre grupos, prueban que jugar con un color "cause" ganar más, ni que estudiar una apertura específica mejore el resultado de nadie. Nadie fue asignado al azar a un color ni a una apertura — cada jugador llega a esa combinación por su propio nivel, preparación y estilo. Esta es la misma idea del "problema fundamental de la inferencia causal" que vimos en la clase de A/B testing: sin un experimento con asignación aleatoria, una asociación observada —por más consistente que se vea— no es evidencia de causalidad. Esto conecta directamente con la frase que pide el propio profesor en el brief: *"una predicción útil no prueba que una acción vaya a mejorar un resultado."*

---

*Preparado con apoyo de Claude Code para el desarrollo del pipeline y la redacción; todos los números citados provienen de la ejecución real de `notebooks/C2_clustering.ipynb` (ver `outputs/tables/C2_*.csv` y `outputs/figures/C2_*.png`), revisada por el equipo antes de la entrega.*
