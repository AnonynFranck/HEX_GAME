import pygame
from AIeasy import EasyAIPlayer
from AInormal import NormalAIPlayer
from AIhard import HardAIPlayer
import sys
class DisjointSet:
    def __init__(self, map_size):
        self.parent = {}
        self.rank = {}
        self.map_width, self.map_height = map_size

        # Nodos auxiliares para las filas 0 y última
        self.red_top_node = (-1, -1)
        self.red_bottom_node = (-2, -2)

        # Nodos auxiliares para las columnas 0 y última
        self.blue_left_node = (-3, -3)
        self.blue_right_node = (-4, -4)

        # Inicializando todos los nodos con ellos mismos como padres y rango 0
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.parent[(x, y)] = (x, y)
                self.rank[(x, y)] = 0

        # Inicializar los nodos auxiliares
        self.parent[self.red_top_node] = self.red_top_node
        self.rank[self.red_top_node] = 0
        self.parent[self.red_bottom_node] = self.red_bottom_node
        self.rank[self.red_bottom_node] = 0
        self.parent[self.blue_left_node] = self.blue_left_node
        self.rank[self.blue_left_node] = 0
        self.parent[self.blue_right_node] = self.blue_right_node
        self.rank[self.blue_right_node] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)

        if x_root == y_root:
            return

        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1

    def check_win(self):
        # Verificar si los nodos auxiliares rojos están conectados
        if self.find(self.red_top_node) == self.find(self.red_bottom_node):
            return "red"

        # Verificar si los nodos auxiliares azules están conectados
        if self.find(self.blue_left_node) == self.find(self.blue_right_node):
            return "blue"

        return None

class Renderer:
    START_HEX_COLOR = pygame.Color(0, 255, 0)
    END_HEX_COLOR = pygame.Color(255, 0, 0)
    BARRIER_COLOR = pygame.Color(0, 0, 255)
    # Changue
    RED_PIECE_COLOR = pygame.Color(255, 0, 0)
    BLUE_PIECE_COLOR = pygame.Color(0, 0, 255)

    def __init__(self, difficulty, default_width, default_height):
        pygame.init()
        self.graphic_size = 70  # Tamaño de cada hexágono
        self.map_type = "HEX"  # Tipo de mapa: HEX
        self.map_size = (11, 11)  # Dimensiones del tablero: 11x11

        create_graphic = self.create_hex_gfx
        self.render = self.render_hex_map

        self.empty_node_gfx = create_graphic(None)
        self.start_node_gfx = create_graphic(self.START_HEX_COLOR)
        self.end_node_gfx = create_graphic(self.END_HEX_COLOR)
        self.barrier_node_gfx = create_graphic(self.BARRIER_COLOR)
        self.red_piece_gfx = create_graphic(self.RED_PIECE_COLOR)
        self.blue_piece_gfx = create_graphic(self.BLUE_PIECE_COLOR)

        self.window_width, self.window_height = self.get_map_size_pixels(self.map_size)
        self.window_width += 700  # Aumentar el ancho de la ventana
        self.window_height += 300  # Aumentar el alto de la ventana
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Tablero Hex 11x11")

        self.red_player_positions = set()
        self.blue_player_positions = set()
        self.current_player = "red"
        self.difficulty = difficulty
        self.font = pygame.font.Font("fonts/mytype.ttf",48)

        if difficulty == "Easy (BFS)":
            self.ai_player = EasyAIPlayer(self)
        elif difficulty == "Normal (Dijkstra)":
            self.ai_player = NormalAIPlayer(self)
        elif difficulty == "Hard (Monte Carlo Tree Search)":
            self.ai_player = HardAIPlayer(self)
    
        #self.window_width = default_width
        #self.window_height = default_height
        self.occupied_positions = set()  # Conjunto para almacenar posiciones ocupadas

        self.disjoint_set = DisjointSet(self.map_size) #Inicializando estructura DisjoinSet


    def get_neighbors(self, x, y):
        # Implementación para obtener los vecinos de un hexágono en las coordenadas (x, y)
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_hex_coords(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
    
    def get_map_size_pixels(self, map_size):
        g = self.graphic_size
        w = map_size[0]
        h = map_size[1]

        w_pix = int(((w + 1) * g) - (0.5 * g)) + 1
        h_pix = int((h * g * 0.75) - (0.25 * g))

        return w_pix, h_pix

    def create_hex_gfx(self, color):
        hex_size = self.graphic_size

        s = pygame.Surface((hex_size, hex_size))
        magenta = pygame.Color(255, 0, 255)
        s.fill(magenta)
        white = pygame.Color(255, 255, 255, 0)

        half = hex_size / 2
        quarter = hex_size / 4

        # Hexagon points
        if color is not None:
            points = []
            points.append((half, 0))
            points.append((hex_size - 1, quarter))
            points.append((hex_size - 1, 3 * quarter))
            points.append((half, hex_size - 1))
            points.append((0, 3 * quarter))
            points.append((0, quarter))

            pygame.draw.polygon(s, color, points)

        # Draw outlines
        pygame.draw.line(s, white, (half, 0), (hex_size - 1, quarter), 1)
        pygame.draw.line(s, white, (hex_size - 1, quarter), (hex_size - 1, 3 * quarter), 1)
        pygame.draw.line(s, white, (hex_size - 1, 3 * quarter), (half, hex_size - 1), 1)
        pygame.draw.line(s, white, (half, hex_size - 1), (0, 3 * quarter), 1)
        pygame.draw.line(s, white, (0, 3 * quarter), (0, quarter), 1)
        pygame.draw.line(s, white, (0, quarter), (half, 0), 1)

        s.set_colorkey(magenta)
        return s
    
    def convert_pixel_to_hex_coords(self, pos):
        g = self.graphic_size
        board_width, board_height = self.get_map_size_pixels(self.map_size)
        board_x = (self.window_width - board_width) // 2
        board_y = (self.window_height - board_height) // 2

        x_pos, y_pos = pos
        x_pos -= board_x
        y_pos -= board_y

        y = y_pos // (g * 0.75)
        x = (x_pos - y * (g // 2)) // g

        return x, y
    def is_valid_hex_coords(self, x, y):
        m_width, m_height = self.map_size
        return 0 <= x < m_width and 0 <= y < m_height
    
    def convert_hex_to_pixel_coords(self, x, y):
        g = self.graphic_size
        board_width, board_height = self.get_map_size_pixels(self.map_size)
        board_x = (self.window_width - board_width) // 2
        board_y = (self.window_height - board_height) // 2

        x_blit = board_x + (x * g) + (g // 2 * (y % 2))
        y_blit = board_y + (y * g * 0.75)

        return x_blit, y_blit
    
    def render_hex_map(self, path):
        g = self.graphic_size
        m_width, m_height = self.map_size

        magenta = pygame.Color(255, 0, 255)

        b = pygame.Surface((self.window_width, self.window_height))
        b.fill(magenta)
        b.set_colorkey(magenta)

        board_width, board_height = self.get_map_size_pixels(self.map_size)
        board_x = (self.window_width - board_width) // 2
        board_y = (self.window_height - board_height) // 2

        for y in range(m_height):
            offset = y // 2
            for x in range(m_width):
                x_blit = board_x + (x * g) + (offset * g)
                y_blit = board_y + (y * g)

                if y % 2 != 0:
                    x_blit += (g / 2)

                if y > 0:
                    y_blit -= ((g / 4) + 1) * y

                if (x, y) in self.red_player_positions:
                    b.blit(self.red_piece_gfx, (x_blit, y_blit))
                elif (x, y) in self.blue_player_positions:
                    b.blit(self.blue_piece_gfx, (x_blit, y_blit))
                elif (x, y) in path:
                    b.blit(self.start_node_gfx, (x_blit, y_blit))
                else:
                    b.blit(self.empty_node_gfx, (x_blit, y_blit))

        difficulty_text = self.font.render(self.difficulty, True, (255, 255, 255))
        self.screen.blit(b, (0, 0))
        self.screen.blit(difficulty_text, (10, 10))
        pygame.display.flip()
    

    def handle_mouse_click(self, pos):
        x, y = self.convert_pixel_to_hex_coords(pos)
        if self.is_valid_hex_coords(x, y) and (x, y) not in self.occupied_positions:
            if self.current_player == "red":
                self.red_player_positions.add((x, y))
                # Unir con los nodos auxiliares si están en el borde
                if y == 0:
                    self.disjoint_set.union((x, y), self.disjoint_set.red_top_node)
                if y == self.map_size[1] - 1:
                    self.disjoint_set.union((x, y), self.disjoint_set.red_bottom_node)
                for neighbor in self.get_neighbors(x, y):
                    if neighbor in self.red_player_positions:
                        self.disjoint_set.union((x, y), neighbor)
            else:
                self.blue_player_positions.add((x, y))
                # Unir con los nodos auxiliares si están en el borde
                if x == 0:
                    self.disjoint_set.union((x, y), self.disjoint_set.blue_left_node)
                if x == self.map_size[0] - 1:
                    self.disjoint_set.union((x, y), self.disjoint_set.blue_right_node)
                for neighbor in self.get_neighbors(x, y):
                    if neighbor in self.blue_player_positions:
                        self.disjoint_set.union((x, y), neighbor)

            self.occupied_positions.add((x, y))
            self.current_player = "blue" if self.current_player == "red" else "red"

            winner = self.disjoint_set.check_win()
            if winner == "red":
                print("El jugador rojo ha ganado!")
                exit()
            elif winner == "blue":
                print("El jugador azul ha ganado!")
                exit()

    def print_player_positions(self):
        print("Posiciones del jugador rojo:")
        for pos in self.red_player_positions:
            print(pos)
        print("\nPosiciones del jugador azul:")
        for pos in self.blue_player_positions:
            print(pos)

    def run(self, show_difficulty_menu):
        path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0)]
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        running = False
                        show_difficulty_menu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            # Realizar movimiento del bot
            self.ai_player.make_move()

            # Show map and print position of the players
            self.render_hex_map(path)
            self.print_player_positions()

        pygame.quit()