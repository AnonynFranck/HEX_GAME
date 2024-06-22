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
        print("No se encontró ningún movimiento válido")
        return None

    def _find_blocking_move(self):
        for y in range(self.game.map_size[1]):
            for x in range(self.game.map_size[0]):
                if (x, y) not in self.game.occupied_positions:
                    # Verificar si este movimiento bloquea un camino casi completo del rojo
                    red_neighbors = sum(1 for nx, ny in self.game.get_neighbors(x, y) if (nx, ny) in self.game.red_player_positions)
                    if red_neighbors >= 2:
                        return (x, y)
        return None

    def _find_advancing_move(self):
        # Intentar avanzar hacia la derecha
        for x in range(self.game.map_size[0]):
            for y in range(self.game.map_size[1]):
                if (x, y) not in self.game.occupied_positions:
                    return (x, y)
        return None

    def _find_random_move(self):
        import random
        empty_positions = [(x, y) for x in range(self.game.map_size[0]) for y in range(self.game.map_size[1])
                        if (x, y) not in self.game.occupied_positions]
        print(f"Casillas vacías: {len(empty_positions)}")
        return random.choice(empty_positions) if empty_positions else None