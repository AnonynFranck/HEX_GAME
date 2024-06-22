class GreedyBlueAIPlayer:
    def __init__(self, game):
        self.game = game
        self.last_move = None

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
        # Primero, buscar un movimiento que bloquee un camino casi completo del rojo
        blocking_move = self._find_blocking_move()
        if blocking_move:
            print(f"Movimiento de bloqueo: {blocking_move}")
            return blocking_move

        advancing_move = self._find_advancing_move()
        if advancing_move:
            print(f"Movimiento de avance: {advancing_move}")
            return advancing_move

        # Si no hay un movimiento de bloqueo urgente, buscar un movimiento que avance hacia el objetivo
        random_move = self._find_random_move()
        if random_move:
            print(f"Movimiento aleatorio: {random_move}")
            return random_move
        # Si no se encuentra ningún movimiento específico, elegir una casilla vacía aleatoria
        #print("No se encontró ningún movimiento válido")
        #return None

    def _find_blocking_move(self):
        # Buscar un camino vertical del rojo para bloquear
        for x in range(self.game.map_size[0]):
            red_path = self._find_vertical_red_path(x)
            if red_path:
                # Intentar bloquear el camino en la parte superior o inferior
                block_top = (x, red_path[0][1] - 1)
                block_bottom = (x, red_path[-1][1] + 1)
                if self._is_valid_move(block_top):
                    return block_top
                if self._is_valid_move(block_bottom):
                    return block_bottom
                
                # Si no se puede bloquear arriba o abajo, intentar bloquear en el medio
                for rx, ry in red_path:
                    block_left = (rx - 1, ry)
                    block_right = (rx + 1, ry)
                    if self._is_valid_move(block_left):
                        return block_left
                    if self._is_valid_move(block_right):
                        return block_right
        
        return None
    def _find_vertical_red_path(self, x):
        path = []
        for y in range(self.game.map_size[1]):
            if (x, y) in self.game.red_player_positions:
                path.append((x, y))
            else:
                if len(path) >= 2:  # Considerar un camino si hay al menos 2 piezas rojas consecutivas
                    return path
                path = []
        return path if len(path) >= 2 else None

    def _find_advancing_move(self):
        for x in range(self.game.map_size[0]):
            for y in range(self.game.map_size[1]):
                if self._is_valid_move((x, y)):
                    return (x, y)
        return None

    def _find_random_move(self):
        import random
        empty_positions = [(x, y) for x in range(self.game.map_size[0]) for y in range(self.game.map_size[1])
                        if (x, y) not in self.game.occupied_positions]
        print(f"Casillas vacías: {len(empty_positions)}")
        return random.choice(empty_positions) if empty_positions else None
    
    def _is_valid_move(self, pos):
        x, y = pos
        return (0 <= x < self.game.map_size[0] and 
                0 <= y < self.game.map_size[1] and 
                (x, y) not in self.game.occupied_positions)