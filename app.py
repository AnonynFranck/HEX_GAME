import pygame
from HexDeform import Renderer

class StartScreen:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("HEX GAME")
        self.font_title = pygame.font.Font("fonts/Blox2.ttf", 150)
        self.font = pygame.font.Font("fonts/mytype.ttf", 48)
        self.title = self.font_title.render("HEX GAME", True, (255, 255, 255))
        self.title_rect = self.title.get_rect()
        self.title_rect.midtop = (width // 2, 50)

        self.start_easy_button = self.font.render("Easy", True, (255, 255, 255))# (BFS)
        self.start_easy_rect = self.start_easy_button.get_rect()
        self.start_easy_rect.center = (width // 2, height // 2 - 50)

        self.start_normal_button = self.font.render("Normal", True, (255, 255, 255))# (Dijkstra)
        self.start_normal_rect = self.start_normal_button.get_rect()
        self.start_normal_rect.center = (width // 2, height // 2)

        self.start_hard_button = self.font.render("Hard", True, (255, 255, 255))#  (Monte Carlo Tree Search)
        self.start_hard_rect = self.start_hard_button.get_rect()
        self.start_hard_rect.center = (width // 2, height // 2 + 50)
        self.default_width = width
        self.default_height = height

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_easy_rect.collidepoint(event.pos):
                        difficulty = "Easy (BFS)"
                        renderer = Renderer(difficulty)
                        renderer.run(self.show_difficulty_menu)
                    elif self.start_normal_rect.collidepoint(event.pos):
                        difficulty = "Normal (Dijkstra)"
                        renderer = Renderer(difficulty)
                        renderer.run(self.show_difficulty_menu)
                    elif self.start_hard_rect.collidepoint(event.pos):
                        difficulty = "Hard (Monte Carlo Tree Search)"
                        renderer = Renderer(difficulty)
                        renderer.run(self.show_difficulty_menu)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.title, self.title_rect)
            self.screen.blit(self.start_easy_button, self.start_easy_rect)
            self.screen.blit(self.start_normal_button, self.start_normal_rect)
            self.screen.blit(self.start_hard_button, self.start_hard_rect)
            pygame.display.flip()

        pygame.quit()

    def show_difficulty_menu(self):
        pygame.display.set_mode((self.default_width, self.default_height))
        self.run()

if __name__ == "__main__":
    start_screen = StartScreen(800, 600)
    start_screen.run()


""" Detect invert (winner red horizontal) <-
    def handle_mouse_click(self, pos):
        if self.winner is not None:
            return

        x, y = self.convert_pixel_to_hex_coords(pos)
        if self.is_valid_hex_coords(x, y) and (x, y) not in self.occupied_positions:
            if self.current_player == "red":
                self.red_player_positions.add((x, y))
                if x == 0:
                    self.disjoint_set.union((x, y), self.disjoint_set.red_left_node)
                if x == self.map_size[0] - 1:
                    self.disjoint_set.union((x, y), self.disjoint_set.red_right_node)
                for neighbor in self.get_neighbors(x, y):
                    if neighbor in self.red_player_positions:
                        self.disjoint_set.union((x, y), neighbor)
            else:
                self.blue_player_positions.add((x, y))
                if y == 0:
                    self.disjoint_set.union((x, y), self.disjoint_set.blue_top_node)
                if y == self.map_size[1] - 1:
                    self.disjoint_set.union((x, y), self.disjoint_set.blue_bottom_node)
                for neighbor in self.get_neighbors(x, y):
                    if neighbor in self.blue_player_positions:
                        self.disjoint_set.union((x, y), neighbor)

            self.occupied_positions.add((x, y))
            self.current_player = "blue" if self.current_player == "red" else "red"

            self.winner = self.disjoint_set.check_win()
            if self.winner:
                print(f"El jugador {self.winner} ha ganado!")
"""

"""
Con este enfoque creaste mi programa AIHard para mi tablero hex, donde rojo es el bot, y para que este sea winner tiene que ir de una de las filas de 0 a una de las filas de 10.Los cambios principales son: 1. El primer movimiento es ahora aleatorio entre los puntos de inicio. 2. Se mantiene un registro del último movimiento (`self.last_move`) para basar las decisiones futuras en él. 3. En lugar de buscar siempre desde el inicio hasta el final, ahora busca el camino más corto desde el último movimiento hasta cualquier punto final. 4. Si no puede encontrar un camino directo, intenta moverse a una posición adyacente a su última pieza. 5. El método `_update_game_state` actualiza el mapa de adyacencia después de cada movimiento, eliminando las conexiones con las piezas del oponente. 6. Se actualizan dinámicamente los puntos de inicio y fin basándose en las nuevas piezas colocadas. Esta implementación debería proporcionar un comportamiento más variado y adaptativo. El bot ahora: * Comienza en una posición aleatoria. * Intenta construir un camino continuo, adaptándose a los obstáculos. * Puede cambiar de estrategia si se bloquea, buscando nuevas rutas o expandiéndose en nuevas direcciones. * Actualiza constantemente su comprensión del tablero basándose en los movimientos de ambos jugadores. va perfecto, pero parece q inclumple estas: * adaptándose a los obstáculos. * Puede cambiar de estrategia si se bloquea, buscando nuevas rutas o expandiéndose en nuevas direcciones. * Actualiza constantemente su comprensión del tablero basándose en los movimientos de ambos jugadores. ya que primero inicia en una posicion aleatorea, cuando se establece en la posicion (0,3) va bajando casi recto como se ve en la ficura , por lo que choca con una posicion de la columna cero que hace que empiece en la posicion (0,9)y no crea otro camino correspondiente, deberia crear en una de las posiciones que inicio aleatoreamente iniciando su camino. PERO ESO DEBE PASAR CUANDO NO HAY UN CAMINO EN SI, sino, como es un caso sencillo, rodear ese obstaculo, de tal forma que sigue llendo en direccion al destino, rodeandolo que es uno de sus vecinos tipo enfocandose en ir hacia abajo, y si no encuentra, rodear pero con la intension de llegar a su destino. (con la finalidad de tener best_move)"""