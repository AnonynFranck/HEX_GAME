import pygame
from AIeasy import EasyAIPlayer
from AInormal import NormalAIPlayer
from AIhard import HardAIPlayer

from DisjointSet import DisjointSetWeighted


class Renderer:
    START_HEX_COLOR = pygame.Color(0, 255, 0)
    END_HEX_COLOR = pygame.Color(255, 0, 0)
    BARRIER_COLOR = pygame.Color(0, 0, 255)
    # Cambiado
    RED_PIECE_COLOR = pygame.Color(255, 0, 0)
    BLUE_PIECE_COLOR = pygame.Color(0, 0, 255)

    def __init__(self, difficulty, default_width, default_height):
        pygame.init()
        self.graphic_size = 70
        self.map_type = "HEX"
        self.map_size = (11, 11)

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
        self.font = pygame.font.Font("fonts/mytype.ttf", 48)

        # Disjoint set
        self.red_player_disjoint_set = DisjointSetWeighted(self.map_size[0] * self.map_size[1])
        self.blue_player_disjoint_set = DisjointSetWeighted(self.map_size[0] * self.map_size[1])

        if difficulty == "Easy (BFS)":
            self.ai_player = EasyAIPlayer(self)
        elif difficulty == "Normal (Dijkstra)":
            self.ai_player = NormalAIPlayer(self)
        elif difficulty == "Hard (Monte Carlo Tree Search)":
            self.ai_player = HardAIPlayer(self)

        # self.window_width = default_width
        # self.window_height = default_height
        self.occupied_positions = set()  # Conjunto para almacenar posiciones ocupadas

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

        y = int(y_pos // (g * 0.75))
        x = int((x_pos - (0.5 * g * (y % 2))) // g)
        if x < 0 or y < 0 or x >= self.map_size[0] or y >= self.map_size[1]:
            return None
        return x, y

    def convert_hex_to_pixel_coords(self, pos):
        g = self.graphic_size
        x, y = pos

        x_off = (y % 2) * (g / 2)
        x_pix = (x * g) + x_off
        y_pix = y * (g * 0.75)

        return x_pix, y_pix

    def render_hex_map(self, map_data):
        g = self.graphic_size
        board_width, board_height = self.get_map_size_pixels(self.map_size)
        board_x = (self.window_width - board_width) // 2
        board_y = (self.window_height - board_height) // 2

        self.screen.fill((0, 0, 0))

        for y in range(self.map_size[1]):
            for x in range(self.map_size[0]):
                p_x, p_y = self.convert_hex_to_pixel_coords((x, y))

                p_x += board_x
                p_y += board_y

                gfx = self.empty_node_gfx

                if map_data[y][x] == "S":
                    gfx = self.start_node_gfx
                elif map_data[y][x] == "E":
                    gfx = self.end_node_gfx
                elif map_data[y][x] == "B":
                    gfx = self.barrier_node_gfx
                elif map_data[y][x] == "R":
                    gfx = self.red_piece_gfx
                elif map_data[y][x] == "BL":
                    gfx = self.blue_piece_gfx

                self.screen.blit(gfx, (p_x, p_y))

    def update_disjoint_set(self, disjoint_set, x, y, player):
        def hex_to_index(x, y):
            return y * self.map_size[0] + x

        index = hex_to_index(x, y)
        disjoint_set.union(index, index)  # Union with itself to add the node

        print(f"Updating disjoint set for {player} at ({x}, {y})")

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.map_size[0] and 0 <= ny < self.map_size[1]:
                neighbor_index = hex_to_index(nx, ny)
                if player == "red" and (nx, ny) in self.red_player_positions:
                    print(f"Union red ({x}, {y}) with ({nx, ny})")
                    disjoint_set.union(index, neighbor_index)
                elif player == "blue" and (nx, ny) in self.blue_player_positions:
                    print(f"Union blue ({x}, {y}) with ({nx, ny})")
                    disjoint_set.union(index, neighbor_index)

    def check_win(self, disjoint_set, player):
        if player == "red":
            for y1 in range(self.map_size[1]):
                for y2 in range(self.map_size[1]):
                    if disjoint_set.find(y1 * self.map_size[0]) == disjoint_set.find(
                            y2 * self.map_size[0] + (self.map_size[0] - 1)):
                        print(f"Red wins with connection from (0, {y1}) to ({self.map_size[0] - 1}, {y2})")
                        return True
        elif player == "blue":
            for x1 in range(self.map_size[1]):
                for x2 in range(self.map_size[1]):
                    if disjoint_set.find(x1 * self.map_size[0]) == disjoint_set.find(
                            x2 * self.map_size[0] + (self.map_size[0] - 1)):
                        print(f"Blue wins with connection from ({x1}, 0) to ({x2}, {self.map_size[0] - 1})")
                        return True
        return False

    def show_disjoint_set(self, player):
        output_path = f'/HEX_GAME/{player}_player_tree'
        if player == "red":
            self.red_player_disjoint_set.save(output_path)
        elif player == "blue":
            self.blue_player_disjoint_set.save(output_path)

    def display_turn_info(self):
        turn_info = f"Turn: {'Red' if self.current_player == 'red' else 'Blue'}"
        turn_info_text = self.font.render(turn_info, True, (255, 255, 255))
        turn_info_rect = turn_info_text.get_rect()
        turn_info_rect.topleft = (10, 10)
        self.screen.blit(turn_info_text, turn_info_rect)

    def run(self, callback):
        map_data = [["" for _ in range(self.map_size[0])] for _ in range(self.map_size[1])]
        clock = pygame.time.Clock()
        running = True
        winner = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    hex_coords = self.convert_pixel_to_hex_coords(event.pos)
                    if hex_coords and hex_coords not in self.occupied_positions:
                        self.occupied_positions.add(hex_coords)
                        x, y = hex_coords
                        if self.current_player == "red":
                            map_data[y][x] = "R"
                            self.red_player_positions.add((x, y))
                            print(f"Red player places at ({x}, {y})")
                            self.update_disjoint_set(self.red_player_disjoint_set, x, y, "red")
                            if self.check_win(self.red_player_disjoint_set, "red"):
                                winner = "Red"
                                running = False
                            self.current_player = "blue"
                        elif self.current_player == "blue":
                            map_data[y][x] = "BL"
                            self.blue_player_positions.add((x, y))
                            print(f"Blue player places at ({x}, {y})")
                            self.update_disjoint_set(self.blue_player_disjoint_set, x, y, "blue")
                            if self.check_win(self.blue_player_disjoint_set, "blue"):
                                winner = "Blue"
                                running = False
                            self.current_player = "red"

            self.render(map_data)
            self.display_turn_info()
            pygame.display.flip()
            clock.tick(30)

        if winner:
            self.show_disjoint_set(winner)

        callback()