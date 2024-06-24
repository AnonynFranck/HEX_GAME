import pygame
from AIhard import HardAIPlayer
from DisjointSet import DisjointSet
from GreedyPlayerBlue import GreedyBlueAIPlayer
from PlayerH import PlayerH
import sys
import time

class Renderer:
    START_HEX_COLOR_BLUE = pygame.Color(0, 0, 100)
    START_HEX_COLOR_RED = pygame.Color(100, 0, 0)
    START_HEX_COLOR = pygame.Color(0, 255, 0)
    END_HEX_COLOR = pygame.Color(255, 0, 0)
    BARRIER_COLOR = pygame.Color(0, 0, 255)
    # Changue
    RED_PIECE_COLOR = pygame.Color(255, 0, 0)
    BLUE_PIECE_COLOR = pygame.Color(0, 0, 255)
    BORDER_COLOR = pygame.Color(128, 0, 128)  # Color morado

    def __init__(self, difficulty):
        pygame.init()
        self.graphic_size = 70  # Tamaño de cada hexágono
        self.map_type = "HEX"  # Tipo de mapa: HEX
        self.map_size = (11, 11)  # Dimensiones del tablero: 11x11

        create_graphic = self.create_hex_gfx
        self.render = self.render_hex_map
        self.winner_written = False

        self.execution_times_red = []
        self.execution_times_blue = []
        self.written_to_file = False

        self.empty_node_gfx = create_graphic(None)
        self.start_node_gfx = create_graphic(self.START_HEX_COLOR)
        self.node_gfx_blue = create_graphic(self.START_HEX_COLOR_BLUE)
        self.node_gfx_red = create_graphic(self.START_HEX_COLOR_RED)
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
        self.current_player = "red" # current player
        self.difficulty = difficulty
        self.font = pygame.font.Font("fonts/mytype.ttf",48)
        self.font_Cracked = pygame.font.Font("fonts/MH.ttf",85)

        if difficulty == "Player(Blue) vs Player(Red)":
            self.ai_player = PlayerH(self)
        elif difficulty == "Bot(Blue) vs Bot(Red)":
            self.ai_playerRed = HardAIPlayer(self)
            self.ai_playerBlue = GreedyBlueAIPlayer(self)

        self.occupied_positions = set()  # Conjunto para almacenar posiciones ocupadas

        self.disjoint_set = DisjointSet(self) #Inicializando estructura DisjoinSet
        self.winner = None  # Para almacenar al WINNER

    def draw_current_player(self):
        if not self.winner:
            text = self.font.render(f"Turno: {self.current_player}", True, (255, 255, 255))
            rect = text.get_rect(topright=(self.screen.get_width() - 10, 10))
            self.screen.blit(text, rect)

    def draw_winner(self, width, height):
        with open('ganadores.txt', 'a') as f:
            if self.winner:
                text = self.font_Cracked.render(f"THE PLAYER {self.winner.upper()} IT'S WINNER!", True, (255, 255, 255))
                rect = text.get_rect(center=(width, height))
                if not self.winner_written:
                    f.write(f"THE PLAYER {self.winner.upper()} WINS\n")
                    f.write(f"NODES EXPANDED BY BLUE: {self.ai_playerBlue.get_NodesB()}\n")
                    f.write(f"NODES EXPANDED BY RED: {self.ai_playerRed.get_NodesR()}\n")
                self.screen.blit(text, rect)
                legendText = self.font.render("press 'r' to return menu or 'q' to exit", True, (255, 255, 255))
                rectL = legendText.get_rect(midbottom=(width, height * 2))
                self.screen.blit(legendText, rectL)
                self.winner_written = True


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

        if self.difficulty == "Player(Blue) vs Player(Red)":
            y = y_pos // (g * 0.75)
            x = (x_pos - y * (g // 2)) // g
        else:
            # Ajustar el cálculo de las coordenadas
            y = int((y_pos / (g * 0.75)))
            x = int((x_pos - (y % 2) * g / 2) / g)

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

    def render_hex_map(self, path_blue, path_red):
        g = self.graphic_size
        m_width, m_height = self.map_size

        hex_size = self.graphic_size
        half = hex_size / 2
        quarter = hex_size / 4

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

                points = []
                points.append((x_blit + half, y_blit))
                points.append((x_blit + hex_size - 1, y_blit + quarter))
                points.append((x_blit + hex_size - 1, y_blit + 3 * quarter))
                points.append((x_blit + half, y_blit + hex_size - 1))
                points.append((x_blit, y_blit + 3 * quarter))
                points.append((x_blit, y_blit + quarter))

                if (x == 0 and y != 0 and y != m_height - 1) or (
                        x == m_width - 1 and y != 0 and y != m_height - 1):  # Extremos verticales sin esquinas
                    pygame.draw.polygon(b, self.START_HEX_COLOR_BLUE, points)
                if (y == 0 and x != 0 and x != m_width - 1) or (
                        y == m_height - 1 and x != 0 and x != m_width - 1):  # Extremos horizontales sin esquinas
                    pygame.draw.polygon(b, self.START_HEX_COLOR_RED, points)

                if (x == 0 and y == 0) or (x == 0 and y == m_height - 1) or (x == m_width - 1 and y == 0) or (
                        x == m_width - 1 and y == m_height - 1):  # Esquinas
                    pygame.draw.polygon(b, self.BORDER_COLOR, points)

                if (x, y) in self.red_player_positions:
                    b.blit(self.red_piece_gfx, (x_blit, y_blit))
                elif (x, y) in self.blue_player_positions:
                    b.blit(self.blue_piece_gfx, (x_blit, y_blit))
                else:
                    b.blit(self.empty_node_gfx, (x_blit, y_blit))

        difficulty_text = self.font.render(self.difficulty, True, (255, 255, 255))
        self.screen.blit(b, (0, 0))
        self.screen.blit(difficulty_text, (10, 10))

        # Show winner
        self.draw_winner(780, 400)

        pygame.display.flip()


    def handle_mouse_click(self, pos):
        if self.winner is not None:
            return

        x, y = self.convert_pixel_to_hex_coords(pos)
        if self.is_valid_hex_coords(x, y) and (x, y) not in self.occupied_positions:
            if self.current_player == "red":
                print(f"Posicion del jugador rojo: {x}, {y}")
                self.red_player_positions.add((x, y))
                if y == 0:
                    self.disjoint_set.union((x, y), self.disjoint_set.red_top_node)
                if y == self.map_size[1] - 1:
                    self.disjoint_set.union((x, y), self.disjoint_set.red_bottom_node)
                for neighbor in self.get_neighbors(x, y):
                    if neighbor in self.red_player_positions:
                        self.disjoint_set.union((x, y), neighbor)
            else:
                self.blue_player_positions.add((x, y))
                if x == 0:
                    self.disjoint_set.union((x, y), self.disjoint_set.blue_left_node)
                if x == self.map_size[0] - 1:
                    self.disjoint_set.union((x, y), self.disjoint_set.blue_right_node)
                for neighbor in self.get_neighbors(x, y):
                    if neighbor in self.blue_player_positions:
                        self.disjoint_set.union((x, y), neighbor)

            self.occupied_positions.add((x, y))
            self.current_player = "blue" if self.current_player == "red" else "red"

            self.winner = self.disjoint_set.check_win()
            if self.winner:
                if not self.written_to_file:
                    avg_time_red = sum(self.execution_times_red) / len(self.execution_times_red)
                    avg_time_blue = sum(self.execution_times_blue) / len(self.execution_times_blue)
                    with open('average_times.txt', 'a') as f:
                        f.write(
                            f"Promedio de tiempo de ejecucion de ai_playerRed.make_move(): {avg_time_red} nano segundos\n")
                        f.write(
                            f"Promedio de tiempo de ejecucion de ai_playerBlue.make_move(): {avg_time_blue} nano segundos\n")
                    self.written_to_file = True

    def print_player_positions(self):
        print("Posiciones del jugador rojo:")
        for pos in self.red_player_positions:
            print(pos)
        print("\nPosiciones del jugador azul:")
        for pos in self.blue_player_positions:
            print(pos)

    def run(self, show_difficulty_menu):
        path_blue = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5)]
        path_red = [(5, y) for y in range(11)]
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
            if self.difficulty == "Player(Blue) vs Player(Red)":
                self.ai_player.make_move()
            elif self.difficulty == "Bot(Blue) vs Bot(Red)":
                if self.current_player == "red":
                    time.sleep(0.3)
                    start_time_red = time.time_ns()
                    self.ai_playerRed.make_move()
                    end_time_red = time.time_ns()
                    execution_time_red = end_time_red - start_time_red
                    self.execution_times_red.append(execution_time_red)
                    print(f"Tiempo de ejecución de ai_playerRed.make_move(): {execution_time_red} nano segundos")
                elif self.current_player == "blue":
                    time.sleep(0.3)
                    start_time_blue = time.time_ns()
                    self.ai_playerBlue.make_move()
                    end_time_blue = time.time_ns()
                    execution_time_blue = end_time_blue - start_time_blue
                    self.execution_times_blue.append(execution_time_blue)
                    print(f"Tiempo de ejecución de ai_playerBlue.make_move(): {execution_time_blue} nano segundos")
            # Show map and print position of the players
            self.render_hex_map(path_blue, path_red)
            # self.print_player_positions()
            # Show current player
            self.screen.fill((0, 0, 0))  # Clean screen
            self.draw_current_player()
        pygame.quit()
