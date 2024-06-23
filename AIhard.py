import random
from collections import deque

class HardAIPlayer:
    def __init__(self, game):
        self.game = game
        self.map_size = game.map_size
        self.adj_map = self._create_adj_map()
        self.painted = {(x, y): False for x in range(self.map_size[0]) for y in range(self.map_size[1])}
        self.starting_vertexes = [(x, 0) for x in range(self.map_size[0])]
        self.ending_vertexes = [(x, self.map_size[1] - 1) for x in range(self.map_size[0])]
        self.last_move = None
        self.nodesR = 0

    def get_NodesR(self):
        return self.nodesR

    def _get_valid_moves(self):
        return [(x, y) for x in range(self.map_size[0]) for y in range(self.map_size[1])
                if (x, y) not in self.game.occupied_positions]

    def print_board(self):
        for y in range(self.map_size[1]):
            for x in range(self.map_size[0]):
                if (x, y) in self.game.blue_player_positions:
                    print('B', end=' ')
                elif (x, y) in self.game.red_player_positions:
                    print('R', end=' ')
                else:
                    print('.', end=' ')
            print()
    
    def _create_adj_map(self):
        adj_map = {}
        for y in range(self.map_size[1]):
            for x in range(self.map_size[0]):
                adj_map[(x, y)] = self.game.get_neighbors(x, y)
        return adj_map

    def make_move(self):
        with open('movimientos.txt', 'a') as f:  # Abre el archivo en modo de escritura
            if self.game.current_player == "red" and not self.game.winner:
                f.write("Turno del bot ROJO\n")
                f.write("Movimientos posibles antes de decidir:\n")
                for move in self._get_valid_moves():
                    f.write(str(move) + "\n")  # Escribe el movimiento en el archivo
                move = self._get_best_move()
                if move:
                    self.game.handle_mouse_click(self.game.convert_hex_to_pixel_coords(*move))
                    self.last_move = move
                    self._update_game_state(move)
                    f.write(f"Posicion del bot ROJO: {move}\n")  # Escribe la posición del bot en el archivo
                    self.nodesR += 1
                    self.print_board()

    def _get_best_move(self):
        if not self.last_move:
            return random.choice(self.starting_vertexes)

        paths = {}
        start = self.last_move
        for end in self.ending_vertexes:
            path = self._get_shortest_path(start, end)
            if path:
                paths[len(path)] = path

        if paths:
            best_path = paths[min(paths.keys())]
            with open('movimientos.txt', 'a') as f:  # Abre el archivo en modo de escritura
                f.write("Mejor camino antes de decidir:\n")
                f.write(str(best_path) + "\n")  # Escribe el mejor camino en el archivo

            for move in best_path[1:]:
                if move not in self.game.occupied_positions:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        adj_x, adj_y = move[0] + dx, move[1] + dy
                        if (adj_x, adj_y) in self.game.red_player_positions:
                            return move

        unoccupied = [(x, y) for x in range(self.map_size[0]) for y in range(self.map_size[1])
                      if (x, y) not in self.game.occupied_positions]
        return random.choice(unoccupied) if unoccupied else None

    def _get_shortest_path(self, start, end):
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            (vertex, path) = queue.popleft()
            if vertex not in visited:
                if vertex == end:
                    return path
                visited.add(vertex)
                for neighbor in self.adj_map[vertex]:
                    if neighbor not in self.game.occupied_positions or neighbor == end:
                        queue.append((neighbor, path + [neighbor]))
        return None

    def _update_game_state(self, move):
        self.painted[move] = True
        for neighbor in self.adj_map[move]:
            if neighbor in self.game.blue_player_positions:
                self.adj_map[move].remove(neighbor)
                self.adj_map[neighbor].remove(move)

        if move in self.starting_vertexes:
            self.starting_vertexes.remove(move)
        if move in self.ending_vertexes:
            self.ending_vertexes.remove(move)

        if move[1] == 0:
            new_starts = [n for n in self.adj_map[move] if n[1] == 0 and n not in self.game.occupied_positions]
            self.starting_vertexes.extend(new_starts)
        if move[1] == self.map_size[1] - 1:
            new_ends = [n for n in self.adj_map[move] if n[1] == self.map_size[1] - 1 and n not in self.game.occupied_positions]
            self.ending_vertexes.extend(new_ends)
