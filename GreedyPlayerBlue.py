class GreedyBlueAIPlayer:
    def __init__(self, game):
        self.game = game
        self.last_move = None
        self.blocking_column = None

    def make_move(self):
        print(f"Turno actual: {self.game.current_player}")
        if self.game.current_player == "blue" and not self.game.winner:
            move = self._get_best_move()
            
            if move and move not in self.game.occupied_positions:
                self.game.handle_mouse_click(self.game.convert_hex_to_pixel_coords(*move))
                self.last_move = move
                print(f"Movimiento del azul: {move}")
            else:
                random_move = self._find_random_move()
                self.game.handle_mouse_click(self.game.convert_hex_to_pixel_coords(*random_move))
                print("No se encontró un movimiento válido para el azul")
    def _get_best_move(self):
        red_path = self._find_red_path()
        if red_path:
            print(f"Camino rojo encontrado: {red_path}")
            blocking_move = self._find_blocking_move(red_path)
            if blocking_move:
                return blocking_move

        return self._find_advancing_move()
    def _find_red_path(self):
        red_positions = sorted(list(self.game.red_player_positions), key=lambda pos: pos[1])
        if not red_positions:
            return []
        
        path = [red_positions[0]]
        for pos in red_positions[1:]:
            if self._is_adjacent(path[-1], pos):
                path.append(pos)
            else:
                if len(path) > len(red_positions) // 2:
                    return path
                path = [pos]
        return path if len(path) > len(red_positions) // 2 else []
    def _is_adjacent(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1
    def _find_blocking_move(self, red_path):
        if not red_path:
            return None

        # Intentar bloquear arriba o abajo del camino
        top = red_path[0]
        bottom = red_path[-1]
        block_top = (top[0], top[1] - 1)
        block_bottom = (bottom[0], bottom[1] + 1)

        if self._is_valid_move(block_top):
            return block_top
        if self._is_valid_move(block_bottom):
            return block_bottom

        # Intentar bloquear a los lados del camino
        for x, y in red_path:
            left = (x - 1, y)
            right = (x + 1, y)
            if self._is_valid_move(left):
                return left
            if self._is_valid_move(right):
                return right

        # Si no se puede bloquear directamente, intentar acercarse
        target = red_path[-1]
        best_move = None
        best_distance = float('inf')
        for x in range(self.game.map_size[0]):
            for y in range(self.game.map_size[1]):
                if self._is_valid_move((x, y)):
                    distance = abs(x - target[0]) + abs(y - target[1])
                    if distance < best_distance:
                        best_distance = distance
                        best_move = (x, y)
        return best_move
##################################
    def _find_advancing_move(self):
        for x in range(self.game.map_size[0]):
            for y in range(self.game.map_size[1]):
                if self._is_valid_move((x, y)):
                    return (x, y)
        return None
##################################
    def _find_random_move(self):
        import random
        empty_positions = [(x, y) for x in range(self.game.map_size[0]) for y in range(self.game.map_size[1])
                        if (x, y) not in self.game.occupied_positions]
        print(f"Casillas vacías: {len(empty_positions)}")
        return random.choice(empty_positions) if empty_positions else None
 ############################   
    def _is_valid_move(self, pos):
        x, y = pos
        return (0 <= x < self.game.map_size[0] and 
                0 <= y < self.game.map_size[1] and 
                (x, y) not in self.game.occupied_positions)