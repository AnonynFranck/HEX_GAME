---
title: "HEX GAME"
author: 
  - Francko Therey Ccama Guerra
  - Luis Enrique Aquije Quiroga
date: "16/06/2024"
---

# HEX GAME

<div align="center">
  <img src="images/hex.png" alt="HEX GAME" width="200">
</div>

## UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS
<div align="center">
  <img src="images/upc-logo.png" alt="UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS">
</div>

## TRABAJO FINAL

### Curso: 
Complejidad Algorítmica

### Sección:
CC43  

### Profesor:
Carnaval Sánchez, Luis Martin

### Integrantes:
- Aquije Quiroga, Luis Enrique - U202114936
- Ccama Guerra, Rogger Francko Therey - U202416650  
---

## Tabla de Contenido:
1. [Descripción del Problema](#descripción-del-problema)
    - [Descripción](#descripción)
    - [Fundamentación del Problema](#fundamentación-del-problema)
2. [Descripción del Conjunto de Datos](#descripción-del-conjunto-de-datos)
    - [Análisis Teórico del Espacio de Decisiones](#análisis-teórico-del-espaci-de-decisiones)
    - [Metodología Estadística y Proceso de Muestreo](#metodología-estadística-y-proceso-de-muestreo)
    - [Relacion con grafos](#relacion-con-grafos)
    - [Motivo del Análisis](#motivo-del-motivo-del-análisis)
3. [Propuesta](#propuesta)
    - [Técnicas y Metodologías Utilizadas]()
      - [Estructura de Datos Disjoint Set](#estructura-de-datos-disjoint-set)
      - [Bot Rojo (HardAIPlayer)]()
      - [Bot Azul (GreedyBlueAIPlayer)]()
      - [Detección de Victoria]()
      - [Análisis de Componentes Conectados]()
      - [Metodología de Evaluación]()
      - [Resultados Esperados]()
4. [Diseño del aplicativo](#diseño-del-aplicativo)
    - [Análisis de complejidad](#análisis-de-complejidad)
5. [Validación de datos y pruebas](#validación-de-datos-y-pruebas)
    - [Tasa de victorias por partida](#tasa-de-victorias-por-partida)
    - [Tiempo de ejecucion de ambos Algoritmos](#tiempo-de-ejecucion-de-ambos-algoritmos)
6. [Conclusiones](#conclusiones)
7. [Bibliografía](#bibliografía)

## Descripción del Problema
### Descripción
En el mundo de los juegos de estrategia, como el HEX, la teoría de grafos desempeña un papel crucial, brindando herramientas y técnicas para abordar problemas específicos. Uno de estos desafíos se define como la búsqueda de estrategias óptimas basadas en los resultados del ganador del juego, lo cual está estrechamente relacionado con la búsqueda de caminos o conexiones eficientes en el tablero.

En el juego HEX, los jugadores compiten por conectar los lados opuestos del tablero con sus fichas de color. Este objetivo se puede equiparar al concepto de encontrar el camino más corto entre dos puntos en un grafo, donde cada celda del tablero representa un nodo, y las conexiones entre las celdas adyacentes representan las aristas.

En este proyecto, nos enfocaremos en el desarrollo de un bot (jugador rojo) que combine el algoritmo de Dijkstra con un árbol de decisiones. Dijkstra se utilizará para encontrar la ruta más corta entre las fichas del jugador, mientras que el árbol de decisiones permitirá al bot evaluar los diferentes escenarios y tomar decisiones estratégicas en cada turno, basándose en las posibles jugadas y sus consecuencias.

Aunque nuestro enfoque principal no será la implementación completa del algoritmo de Monte Carlo Tree Search (MCTS), tomaremos algunas ideas y conceptos clave de este enfoque. Por ejemplo, utilizaremos simulaciones y rollouts para explorar las posibles jugadas y evaluar su efectividad, lo que contribuirá a mejorar la calidad y efectividad del bot en el juego. Por esa razon esta combinación de técnicas proporcionará al bot la capacidad de analizar el tablero de manera eficiente, simular movimientos potenciales y tomar decisiones estratégicas en cada turno, adaptándose a las jugadas del oponente y buscando la conexión ganadora óptima.

<div align="center">
  <img src="images/GR7qf.png" alt="MONTE CARLO TREE SEARCH">>
</div>


## Descripción del Conjunto de Datos

### Análisis Teórico del Espacio de Decisiones
En este proyecto, al utilizar el algoritmo de Dijkstra en conjunto con un árbol de decisiones, podemos estimar el número de posibles resultados o nodos en el árbol de decisiones de la siguiente manera:

* Primero, debemos considerar que el tablero de Hex tiene un tamaño de 11x11, lo que significa que hay un total de $121$ celdas o nodos en el grafo.
* Para calcular el número máximo de nodos en el árbol de decisiones, podemos suponer que en cada turno, el bot (jugador rojo) tiene la opción de colocar su ficha en cualquiera de las celdas vacías restantes. Esto significa que en el primer turno, el bot tiene $121$ opciones diferentes.
* En el segundo turno, suponiendo que el oponente (jugador azul) también ha colocado una ficha, el bot tendría $119$ opciones ($121 - 2$ fichas colocadas).
Siguiendo esta lógica, en el turno $t$, el número de opciones disponibles para el bot sería $121 - (2t - 1)$, ya que habrá $(2t - 1)$ fichas colocadas en el tablero ($t$ del bot y $t - 1$ del oponente).

Entonces, el número máximo de nodos en el árbol de decisiones sería la suma de las opciones disponibles en cada turno, desde el turno $1$ hasta el turno $61$ (asumiendo que el juego termina cuando todas las $121$ celdas están ocupadas):

$$Número Máximo Nodos = 121 + 119 + 117 + ... + 3 + 1 = \sum_{t=1}^{61} (121 - 2(t - 1)) = 3721$$ 

Por lo tanto, en el peor de los casos, el árbol de decisiones podría tener un máximo de 3721 nodos.

Sin embargo, es importante tener en cuenta que este cálculo asume que todas las jugadas son posibles y que no se consideran las reglas del juego Hex, que implican la formación de cadenas ininterrumpidas para conectar los lados opuestos.

En la práctica, el número real de nodos en el árbol de decisiones será menor, ya que algunas jugadas serán descartadas por ser inválidas o poco prometedoras. Además, el uso del algoritmo de Dijkstra para encontrar la ruta más corta entre las fichas del bot, junto con la poda del árbol de decisiones basada en heurísticas y evaluaciones, reducirá aún más el tamaño efectivo del árbol de decisiones.
### Metodología Estadística y Proceso de Muestreo

Para evaluar el rendimiento de los bots en el juego Hex, se implementó un riguroso proceso de muestreo y análisis estadístico. El objetivo fue obtener una estimación confiable de la tasa de victoria de cada bot bajo diferentes condiciones de juego.

#### Diseño del Muestreo

Se realizaron tres conjuntos de simulaciones, cada uno con un número diferente de partidas:

* 100 partidas

* 500 partidas

* 1000 partidas

Cada partida se jugó hasta su conclusión, determinando un ganador claro (bot rojo o bot azul).

#### Cálculo de la Tasa de Victoria

Para cada conjunto de simulaciones, se calculó la tasa de victoria para cada bot utilizando la siguiente fórmula:

$$\text{Tasa de Victoria} = \frac{\text{Número de Victorias}}{\text{Número Total de Partidas}} \times 100\%$$

#### Análisis de la Media

Para obtener una estimación más robusta del rendimiento general, se calculó la media de las tasas de victoria a través de los tres conjuntos de simulaciones:

$$\text{Media de Tasa de Victoria} = \frac{\sum_{i=1}^{3} \text{Tasa de Victoria}_i}{3}$$

donde $i$ representa cada conjunto de simulaciones (100, 500, y 1000 partidas).

#### Justificación del Tamaño de Muestra

La elección de realizar hasta 1000 partidas se basó en la necesidad de:
> Reducir el margen de error en nuestras estimaciones.

> Capturar una amplia variedad de escenarios de juego posibles.

> Proporcionar suficientes datos para identificar patrones consistentes en el rendimiento de los bots.

El incremento progresivo en el número de partidas (100, 500, 1000) nos permite también observar cómo la estabilidad de los resultados mejora con tamaños de muestra más grandes.

#### Limitaciones

Es importante notar que, aunque 1000 partidas proporcionan una muestra sustancial, este número sigue siendo pequeño en comparación con el número total de posibles configuraciones de juego en Hex. Por lo tanto, nuestros resultados deben interpretarse como una aproximación del rendimiento real de los bots, sujeta a cierto margen de error.

### Origen de los Datos

Los datos se generan durante el transcurso de las partidas de Hex en un tablero de $11$ X $11$, donde se enfrentan dos bots con estrategias distintas:

### `Bot Rojo (HardAIPlayer)`
### `Bot Azul (GreedyBlueAIPlayer)`

Los datos se generan y registran de la siguiente manera:

* Movimientos considerados:

  Antes de cada movimiento del Bot Rojo, se guarda en un archivo de texto (movimientos.txt) una lista de todas las posiciones válidas que el algoritmo está considerando.


* Movimiento seleccionado:

  Después de que cada bot realiza su movimiento, se registra la posición exacta donde se colocó la ficha.


* Camino óptimo:

  Para el Bot Rojo, después de cada movimiento, se guarda el camino que el algoritmo considera como el mejor en ese momento, mostrando la secuencia de casillas desde su posición actual hasta el borde objetivo.


* Estado del tablero:

  Después de cada movimiento, se guarda una representación del estado actual del tablero, mostrando las posiciones de todas las fichas rojas y azules.


* Resultado de la partida:

  Al finalizar cada juego, se registra el ganador (Rojo o Azul) y el número total de movimientos realizados durante la partida.


* Estadísticas de nodos explorados:

  Se lleva un conteo de cuántos nodos (posiciones) explora cada bot durante la partida, lo que puede dar una idea de la eficiencia de cada estrategia.

### Motivo del Análisis

El presente estudio se centra en un análisis exhaustivo del rendimiento y las estrategias empleadas por los bots rojo y azul en el juego Hex, con el objetivo de obtener una comprensión profunda de las dinámicas del juego y la efectividad de los algoritmos implementados. En primer lugar, se busca determinar la tasa de victoria (win rate) para ambos bots a lo largo de múltiples partidas. Este análisis no solo proporcionará un porcentaje claro de victorias para cada bot, sino que también permitirá establecer la efectividad general de cada estrategia empleada, ofreciendo insights valiosos sobre qué enfoque resulta más exitoso en el contexto del juego Hex.
Este enfoque se dara con las siguientes areas:

* Tasa de Victoria (Win Rate):

  Determinar el rango de victorias para el bot rojo y el bot azul a lo largo de múltiples partidas para calcular el porcentaje de victorias de cada bot para establecer cuál estrategia es más efectiva en general.

* Exploración de Nodos:

  Cuantificar el número de nodos (posiciones) explorados por cada bot durante las partidas, para comparar la eficiencia de exploración entre el bot rojo (que utiliza algoritmos de búsqueda de caminos) y el bot azul (que emplea una estrategia codiciosa). Además, mapear patrones de movimientos que tienen mayor probabilidad de llevar a la victoria.

* Análisis Probabilístico:

  Desarrollar un modelo probabilístico para predecir las chances de victoria basado en la configuración del tablero en diferentes etapas del juego, que conllevará a calcular la probabilidad de victoria asociada a ciertas posiciones o patrones de fichas en el tablero.


* Evaluación de Estrategias:

  Analizar la efectividad de la estrategia de búsqueda de caminos del bot rojo frente a la estrategia de bloqueo del bot azul, para identificar situaciones donde una estrategia supera consistentemente a la otra. Por ello, se examinará en detalle las partidas donde la victoria se decide por un margen estrecho de tal forma q se dentificará movimientos críticos que pueden cambiar el curso del juego.

<div align="center">
  <img src="images/bluered.png" alt="Estadistic & Prob" width="700">
</div>

Este análisis exhaustivo proporcionará insights valiosos sobre las dinámicas del juego Hex y las estrategias empleadas por los bots. Los resultados pueden utilizarse para refinar los algoritmos, mejorar las estrategias de juego, y potencialmente desarrollar nuevos enfoques que combinen las fortalezas de ambas estrategias. Además, este estudio podría ofrecer perspectivas interesantes sobre la teoría de juegos y la inteligencia artificial aplicada a juegos de estrategia.
### Relacion con grafos

El juego Hex se presta naturalmente a una representación mediante grafos, lo cual es fundamental para entender y analizar las estrategias de los bots. La relación se puede describir de la siguiente manera:

* Estructura del Grafo:
  
  El tablero de Hex se traduce naturalmente a un grafo donde cada una de las 121 casillas del tablero 11x11 se convierte en un nodo. Las conexiones entre casillas adyacentes se representan como aristas, formando una red compleja. Las casillas internas tienen 6 vecinos, mientras que las de los bordes y esquinas tienen menos, creando una topología única que refleja fielmente la estructura del juego Hex.

* Grafo No Dirigido:
  
  En esta representación, las  conexiones entre casillas son bidireccionales, lo que da lugar a un grafo no dirigido. Esta característica es fundamental para entender cómo los jugadores pueden moverse y conectar sus fichas en cualquier dirección, capturando la esencia de la libertad de movimiento en Hex.

* Grafo Ponderado vs No Ponderado:
  
  En su forma más básica, el grafo del Hex es no ponderado, asignando igual importancia a todas las conexiones. Sin embargo, estrategias más sofisticadas podrían incorporar pesos en las aristas, reflejando la importancia estratégica variable de diferentes conexiones en el tablero, lo que añadiría una capa adicional de complejidad al análisis.

* Subgrafos Dinámicos:
  
  A medida que avanza el juego, se forman subgrafos dinámicos para cada jugador. El subgrafo del jugador rojo busca conectar el borde superior con el inferior, mientras que el del azul intenta unir el izquierdo con el derecho. Estos subgrafos evolucionan con cada movimiento, representando el estado actual del juego y las posibilidades de victoria para cada jugador.

* Componentes Conectados:
  
  El bot azul utiliza el análisis de componentes conectados para identificar y bloquear las estructuras de conexión del oponente. Este enfoque se relaciona con el concepto de componentes fuertemente conectadas en teoría de grafos, permitiendo al bot identificar áreas críticas del tablero donde puede interrumpir las estrategias del oponente. Es por ello que se implemento la estructura DisjointSet, no solo para determinar quien ganó el juego, sino determinar los caminos potenciales que empiezán a crear.

* Optimización de Rutas:
  
  Los algoritmos empleados por los bots pueden interpretarse como problemas de optimización de rutas en grafos. Buscan el camino más eficiente para conectar sus bordes objetivo, considerando no solo la longitud del camino sino también su resistencia a los bloqueos del oponente, lo que añade una dimensión estratégica adicional al análisis del juego. Es por ello que se hizo la implemantacion de recorrido BFS con apertura de fuerza bruta para la evaluacion de los posibles caminos.

<div align="center">
  <img src="images/hex_graph.png" alt="HEX GRAPH">
</div>


## Propuesta

El objetivo principal de esta propuesta es desarrollar, implementar y analizar estrategias eficientes para bots que jueguen al Hex, un juego de estrategia de conexión. Se busca crear bots que puedan tomar decisiones inteligentes, anticipar movimientos del oponente y establecer conexiones efectivas en el tablero donde se detallara cual sera la intension de cada uno de las fichas.

### Técnicas y Metodologías Utilizadas:

#### Estructura de Datos Disjoint Set:

Se implementa una estructura de conjuntos disjuntos (DisjointSet) para manejar eficientemente las conexiones en el tablero.
Esta estructura permite:
* Detectar rápidamente componentes conectados para el jugador rojo, identificando posibles caminos.
* Determinar el ganador utilizando nodos auxiliares para los bordes del tablero.


#### Bot Rojo (HardAIPlayer):

Utiliza una estrategia de fuerza bruta basada en DFS (Depth-First Search) evaluando el conjunto de estados finales si es que llegue a una de ellas, de esa forma probando las demas posiblidades.
* Explora sistemáticamente todos los caminos posibles desde su posición actual hasta el borde opuesto con la finalidad de intenta crear y extender caminos para completar una conexión entre los bordes superior e inferior utiliza la estructura DisjointSet para usar la conectividad y detectar caminos potenciales. Además, al usar un recorrido por profundidad nos permite prevenir obstaculos que se presenten usando backtracking.

<p align="center">
  <img src="images/DFS2.gif" width="400">
</p>

#### Bot Azul (GreedyBlueAIPlayer):

Emplea una estrategia codiciosa (greedy) con ayuda de análisis de componentes.
* Utiliza la `función get_largest_component` de DisjointSet para identificar el componente conectado más grande del jugador rojo, lo cual  prioriza bloquear el avance del componente más grande del oponente.
* Si no puede bloquear directamente, busca avanzar hacia su propio objetivo de conectar los bordes izquierdo y derecho. Aprovechando esta estrategia, su proposito principalmente es bloquear al jugador rojo. Para ello se implemento un sistema de componentes conectados para identificar y obstruir los caminos potenciales del oponente, teniendo en cuenta que mientras bloquea buscará avanzar hacia su propio objetivo de conectar los bordes izquierdo y derecho del tablero.
<p align="center">
  <img src="images/OhhWl.gif" width="400">
</p>

#### Detección de Victoria:

Se utiliza la función check_win de DisjointSet para determinar si algún jugador ha ganado.
Los nodos auxiliares (`red_top_node`, `red_bottom_node`, `blue_left_node`, `blue_right_node`) permiten una verificación eficiente de la victoria al comprobar si los bordes opuestos están conectados.


#### Análisis de Componentes Conectados:

La función `get_connected_components` de DisjointSet se utiliza para analizar la estructura del tablero y las posiciones de las fichas.
Esto permite a los bots evaluar la fortaleza de sus posiciones y las del oponente.



#### Metodología de Evaluación:

Se realizarán múltiples partidas entre los bots para recopilar datos sobre sus tasas de victoria, eficiencia en la toma de decisiones y patrones de juego. También, se analizará la efectividad de las estrategias de cada bot en diferentes etapas del juego, de esta forma, recopilando y estudiando la capacidad de los bots para adaptarse a las estrategias del oponente. Además, medirá el rendimiento computacional de los algoritmos utilizados, considerando el tiempo de respuesta y la cantidad de nodos explorados en cada turno.

#### Resultados Esperados:

* Determinar la eficacia relativa de las estrategias de fuerza bruta (Bot Rojo) versus la estrategia codiciosa (Bot Azul) en el contexto del juego Hex . Con ello se esperara que la tasa de victorias la tenga el bot azul, por una simple razón de tener una estrategia defensiva y ofensiva a la vez, por lo mensionado anteriormente.
* Identificar patrones de juego exitosos y situaciones críticas que influyen significativamente en el resultado de las partidas.
* Proporcionar insights sobre posibles mejoras y refinamientos en las estrategias de los bots.
* Evaluar la escalabilidad de los algoritmos utilizados para tableros de diferentes tamaños.


## Diseño del aplicativo

* Hemos utilizado la estructura Disjoints o conjuntos disjuntos para realizar y a su vez detectar las uniones de extremo a extremo con las fichas del jugador correspondiente implementando la finalidad del juego, esto mediante nodos auxiliares, dos para el rojo y otros dos para azul. Estos nodos son inicializados en el main. Los extremos están conectados a los nodos auxiliares correspondientes teniendo como complejidad O(1).

* También se han empleado funciones de pygame para el dibujo de polígonos y sus contornos como ```pygame.draw.polygon()```, tomando como referencia las coordenadas y el tamaño que tendrá cada hexágono. ```pygame.draw.line()``` para la creación de las líneas que unen los hexágonos. ```pygame.display.flip()``` para mostrar los cambios en la pantalla.

* Se diseña el tablero unitariamente cada hexagono con sus respectivas coordenadas como si de un plano cartesiano invertido se tratase tratandolos de manera lógica como si fueran nodos pero representandolos como un tablero de hexágonos.

* El uso de una función ```convert_pixel_to_hex_coords()``` es necesaria para poder aplicar DisjointSet ya que este trabaja con coordenadas. Las coordenadas de cada hexágono se emplean para identificar y manipular los nodos en la estructura de datos del Disjoint Set. Esto en el juego Hex es aplicado en forma de hexágonos que vendrían a ser los nodos.

* Se agregó también nuevas funciones como ```def get_connected_components(self, color)``` que obtiene los caminos del bot rojo y ```def get_largest_component(self, color)``` obtiene el mas reciente componente que ha creado el algoritmo y determinar el componente más grande. Empleando el algoritmo de Kusaragi analizando los componentes de rojo facilitamos la busqueda de los caminos más cortos.


* También se ha utilizado un algoritmo DFS para detectar el camino más corto que se pueda crear y que conecte a los extremos de cada lado del tablero.

* La funcion que utiliza este algoritmo es ```_get_shortest_path(self, start, end)``` que recibe como parametros el nodo de inicio y fin el cual luego es almacenado en una cola ```queue``` que sirve para almacenar vértices a visitar y visited que es un conjunto que se utiliza para almacenar los vértices que ya han sido visitados. 

* Mediante un bucle ```while``` que ocurre hasta que la cola esté vacía, en cada iteración del bucle se toma un vértice de la cola y se explora. Si el vértice es el vértice final se vuelve el camino hasta dicho vertice, caso contrario se agregan los vertices no visitados de la cola para explorarlos en las iteraciones posteriores

### Análisis de complejidad

```render_hex_map()``` posee una complejidad de tiempo $O(n^2)$ porque tiene dos bucles anidados que recorren ancho y alto del tablero.

```handle_mouse_click()``` posee una complejidad de tiempo $O(n)$ porque llama a una función que tiene un ciclo for que recorre el tablero.

```print_player_positions()``` posee una complejidad de tiempo $O(n)$ porque recorre las posiciones en el tablero.

```run()``` posee una complejidad de tiempo $O (n^2)$ debido a que llama a una funcion ```render_hex_map()``` con una complejidad de tiempo $O(n^2)$

### DisjointSet.py

```find()``` posee una complejidad $O(k) $

Toma un nodo como entrada y devuelve el representante de su conjunto. Utiliza la técnica de compresión de caminos para optimizar futuras búsquedas.

```union()``` posee una complejidad $O(1)$

Toma dos nodos como entrada y une sus conjuntos. Utiliza la técnica de unión por rango para mantener el árbol de conjuntos disjuntos equilibrado.

```check_win()``` posee una complejidad $O(1+k) $

```def get_connected_components(self, color)``` posee una complejidad de tiempo $O(n^2)$

```def get_largest_component(self, color)``` posee una complejidad de tiempo $O(n^2)$

### AIhard.py

```_get_valid_moves(self)``` posee una complejidad de tiempo de $O(n^2) $

```make_move(self)``` tiene una complejidad de tiempo $O(n^2) $

```_get_best_move(self)``` posee una complejidad de tiempo $O(m*n^2+n^2) $

```_get_shortest_path(self, start, end``` posee una complejidad de tiempo $O(n*m)$

### Renderer.py

```def get_neighbors()``` posee una complejidad de tiempo $O(n)$

```def render_hex_map()``` posee una complejidad de tiempo $O(n^2)$

```def run()``` es la funcion que llama a las demás funciones para ejecutar el juego.

### GreedyPlayerBlue.py
```_get_best_move```:
* Obtener el componente rojo más grande: $O(m)$, donde n es el número de celdas en el tablero (121 para un tablero 11x11).
Buscar un movimiento de bloqueo:

* Iterar sobre las posiciones del componente rojo: $O(m)$, donde m es el tamaño del componente más grande _(en el peor caso, m = n)_.
Para cada posición, comprobar hasta 3 posiciones adyacentes:$ O(1)$ por posición.

* Si no se encuentra un movimiento de bloqueo, llamar a (`_find_advancing_move`): $O(n) en el peor caso.

```make_move```:
* Llamada a (`_get_best_move`) Esta es la operación principal que 
determina la complejidad.

```_find_advancing_move```
* Obtener el componente azul más grande: $O(n)$
* Generar movimientos potenciales: $O(m)$, donde m es el tamaño del componente azul más grande.
* Validar movimientos: $O(m)$
Seleccionar el movimiento más avanzado: $O(m)$

```_is_valid_move```
* Comprovabaciones simples $O(1)$
## Validación de datos y pruebas
> ### Tasa de victorias por partida
<p align="center">
  <img src="images/dataset_graph.png" width="400"><br>
    <a href="https://docs.google.com/spreadsheets/d/1aukxchH79EYdNzJKLk0XQ3KdyHOFFYE3O7KxIXU3Rj8/edit?gid=0#gid=0">Dataset1</a>
</p>

**Tabla 1: Resultados de victorias por número de partidas y media**

| Jugador | Caso 100 | Caso 500 | Caso 1000 | Media |
|---------|----------|----------|-----------|-------|
| Rojo    | 21       | 87       | 172       | 93.3  |
| Azul    | 79       | 413      | 828       | 440.0 |

*Nota: La media se calculó sobre los tres casos presentados.*

> ### Tiempo de ejecucion de ambos Algoritmos

<p align="center">
    <img src="./images/ComparationBlueRed.png" width="400"></br>
    <a href="python3">Dataset2</a>
</p>

**Tabla 2: Resultados del tiempo de ejecución**
|   Rojo (ms) |   Azul (ms) |
|------------:|------------:|
|       1.511 |       0.048 |
|       1.271 |       0.153 |
|       1.88  |       0.15  |
|       3.55  |       0.078 |
|       1.548 |       0.046 |

*Nota: Solo se considero los tiempo que eran mayor a cero para el azul, ya que mayormente daba cero.*

**[Demostraciones](https://github.com/AnonynFranck/HEX_GAME/tree/main/source)**
## Conclusiones
El experimento reveló que el algoritmo greedy implementado para el jugador azul en el juego Hex demostró ser superior tanto en eficacia como en eficiencia computacional. Con una mayor tasa de victoria y tiempos de ejecución significativamente menores _(frecuentemente cercanos a cero)_ en comparación con el algoritmo del jugador rojo, el enfoque greedy se posiciona como una estrategia altamente efectiva para este juego. Esta combinación de alto rendimiento y baja complejidad computacional sugiere que estrategias aparentemente simples, cuando están bien diseñadas y adaptadas al contexto específico del juego, pueden superar a enfoques más complejos. La eficacia del algoritmo greedy en bloquear al oponente mientras avanza hacia su objetivo demuestra la importancia de balancear tácticas defensivas y ofensivas en juegos de conexión como Hex. Para futuras investigaciones, sería valioso explorar la escalabilidad de este enfoque en tableros de mayor tamaño, investigar la integración de técnicas de aprendizaje por refuerzo para mejorar la toma de decisiones, y examinar cómo el algoritmo se comportaría contra jugadores humanos expertos o contra otros algoritmos de IA más avanzados, como los basados en redes neuronales o búsqueda de Monte Carlo.
## Bibliografía

Altamirano, C. (2018). MONTE CARLO TREE SEARCH PARA EL
PROBLEMA DE CARGA DE CONTENEDORES [Informe de proyecto de
título, Pontificia Universidad Católica de Valparaíso]. OPAC. http://opac.pucv.cl/pucv_txt/txt-7500/UCC7969_01.pdf

Algoritmo de Monte Carlo aplicado a Búsquedas en Espacios de Estados. Universidad de Sevilla. https://www.cs.us.es/~fsancho/Blog/posts/MCTS.md

The rules of Hex. Krammer. https://www.krammer.nl/hex/

El algoritmo de Dijkstra. Runestone. https://runestone.academy/ns/books/published/pythoned/Graphs/ElAlgoritmoDeDijkstra.html

"Monte Carlo Tree Search: A New Framework for Game AI" por Michael Buro, de la Universidad de Alberta. https://webdocs.cs.ualberta.ca/~mburo/eps/othereps.php

Amalia Duch. (2006). Esquema de Dividir y Vencer .UPC Universitat Politècnica de Catalunya. https://www.cs.upc.edu/~duch/home/duch/dyd.pdf

Backtracking. Universidad de Illinois en Urbana-Champaign https://jeffe.cs.illinois.edu/teaching/algorithms/book/02-backtracking.pdf

Shirley, A. (s.f.). A* Pathfinding Algorithm Comparison. Recuperado de https://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html

Rosell, E., & Keila, R. Título del documento (Trabajo de fin de grado). Recuperado de https://diposit.ub.edu/dspace/bitstream/2445/186821/2/tfg_rosell_esau_keila_ruth.pdf

De Waard, H. (2011). Greedy and $K$-Greedy Algorithms for Multidimensional Data Association. IEEE Transactions on Aerospace and Electronic Systems. https://www.academia.edu/101541946/Greedy_and_K_Greedy_Algorithms_for_Multidimensional_Data_Association?sm=b