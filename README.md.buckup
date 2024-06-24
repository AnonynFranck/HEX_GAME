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

## TRABAJO PARCIAL

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
3. [Propuesta](#propuesta)
4. [Diseño del aplicativo](#diseño-del-aplicativo)
4. [Bibliografía](#bibliografía)

## Descripción del Problema
### Descripción
En el mundo de los juegos de estrategia, como el HEX, la teoría de grafos desempeña un papel crucial, brindando herramientas y técnicas para abordar problemas específicos. Uno de estos desafíos se define como la búsqueda de estrategias óptimas basadas en los resultados del ganador del juego, lo cual está estrechamente relacionado con la búsqueda de caminos o conexiones eficientes en el tablero.

En el juego HEX, los jugadores compiten por conectar los lados opuestos del tablero con sus fichas de color. Este objetivo se puede equiparar al concepto de encontrar el camino más corto entre dos puntos en un grafo, donde cada celda del tablero representa un nodo, y las conexiones entre las celdas adyacentes representan las aristas.

En este proyecto, nos enfocaremos en el desarrollo de un bot (jugador rojo) que combine el algoritmo de Dijkstra con un árbol de decisiones. Dijkstra se utilizará para encontrar la ruta más corta entre las fichas del jugador, mientras que el árbol de decisiones permitirá al bot evaluar los diferentes escenarios y tomar decisiones estratégicas en cada turno, basándose en las posibles jugadas y sus consecuencias.

Aunque nuestro enfoque principal no será la implementación completa del algoritmo de Monte Carlo Tree Search (MCTS), tomaremos algunas ideas y conceptos clave de este enfoque. Por ejemplo, utilizaremos simulaciones y rollouts para explorar las posibles jugadas y evaluar su efectividad, lo que contribuirá a mejorar la calidad y efectividad del bot en el juego. Por esa razon esta combinación de técnicas proporcionará al bot la capacidad de analizar el tablero de manera eficiente, simular movimientos potenciales y tomar decisiones estratégicas en cada turno, adaptándose a las jugadas del oponente y buscando la conexión ganadora óptima.

## Descripción del Conjunto de Datos
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

## Propuesta

Se usará DFS en lugar de BFS, ya que, BFS usa una búsqueda por anchura con una cierta eficacia en buscar el camino más corto, algo que a comparación de DFS es mucho más ineficiente, ya que para este caso lo que se busca es evaluar las posibles rutas y escenarios. En hex todos tienen el mismo peso pero mientras se van eliminando los nodos el peso de estos va cambiando.

Con respecto a los dataset el algoritmo que nos proporcionará muchos más datos será el DFS porque mediante fuerza bruta evaluará los 121 posibles caminos del tablero y 3721 posibles nodos.

También se contempla implementar el algoritmo de Dijkstra para encontrar el camino más corto mediante un árbol de decisiones enfocado en Monte Carlo Tree Search el cual hará uso del Backtracking como estrategia de recorrido en profundidad. Este algoritmo reduce su cantidad de posibles nodos que con DFS serían 3721 haciéndolo mucho más eficiente.

A comparación de BFS, Dijkstra es mucho más eficiente, ya que, a pesar de que BFS se enfoca en encontrar el camino más corto, Dijkstra se enfoca en encontrar el camino más corto y además el más eficiente para conectar los lados opuestos del tablero. Por lo que Dijkstra generara menos contenido en el dataset.

Además mediante programación dinámica y algoritmos greedy se realizará la poda de los arboles de decisión para reducir la cantidad de nodos y así hacer más eficiente el algoritmo.

## Diseño del aplicativo

Hemos utilizado la estructura Disjoints o conjuntos disjuntos para realizar y a su vez detectar las uniones de extremo a extremo con las fichas del jugador correspondiente implementando la finalidad del juego, esto mediante nodos auxiliares, dos para el rojo y otros dos para azul. Estos nodos son inicializados en el main. Los extremos están conectados a los nodos auxiliares correspondientes teniendo como complejidad O(1).

También se han empleado funciones de pygame para el dibujo de polígonos y sus contornos como ```pygame.draw.polygon()```, tomando como referencia las coordenadas y el tamaño que tendrá cada hexágono. ```pygame.draw.line()``` para la creación de las líneas que unen los hexágonos. ```pygame.display.flip()``` para mostrar los cambios en la pantalla.

Se diseña el tablero unitariamente cada hexagono con sus respectivas coordenadas como si de un plano cartesiano invertido se tratase tratandolos de manera lógica como si fueran nodos pero representandolos como un tablero de hexágonos.

El uso de una función ```convert_pixel_to_hex_coords()``` es necesaria para poder aplicar DisjointSet ya que este trabaja con coordenadas. Las coordenadas de cada hexágono se emplean para identificar y manipular los nodos en la estructura de datos del Disjoint Set. Esto en el juego Hex es aplicado en forma de hexágonos que vendrían a ser los nodos.

Además el sistema de turnos está basado en clicks.

### Analisis de complejidad

```render_hex_map()``` posee una complejidad de tiempo O(n^2) porque tiene dos bucles anidados que recorren ancho y alto del tablero.

```handle_mouse_click()``` posee una complejidad de tiempo O(n) porque llama a una función que tiene un ciclo for que recorre el tablero.

```print_player_positions()``` posee una complejidad de tiempo O(n) porque recorre las posiciones en el tablero.

```run()``` posee una complejidad de tiempo O(n^2) debido a que llama a una funcion ```render_hex_map()``` con una complejidad de tiempo O(n^2)

### DisjointSet.py

```__init__()``` posee una complejidad de tiempo O(n) porque inicializa con el tamaño del tablero los diccionarios rank y parent. En este n vendría a ser el número de hexágonos que componen el tablero.

Inicializa la estructura de datos del conjunto disjunto. Crea dos diccionarios, parent y rank, para cada nodo en el tablero. También crea nodos auxiliares para representar los bordes del tablero. 

```find()``` posee una complejidad O(a(n)) porque es constante en todos los valores practicos de n.

Toma un nodo como entrada y devuelve el representante de su conjunto. Utiliza la técnica de compresión de caminos para optimizar futuras búsquedas.

```union()``` posee una complejidad O(a(n)) porque llama a la funcion ```find()``` dos veces

Toma dos nodos como entrada y une sus conjuntos. Utiliza la técnica de unión por rango para mantener el árbol de conjuntos disjuntos equilibrado.

```check_win()``` posee una complejidad O(1) porque solo realiza operaciones constantes

Verifica si los nodos auxiliares rojos o azules están conectados, lo que indicaría que un jugador ha ganado el juego. Devuelve el color del jugador ganador o None si aún no hay ganador.

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