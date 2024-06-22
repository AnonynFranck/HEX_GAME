temp = 0
aux = 0
for i in range(121, 0, -2):
    temp += 1
    aux += i

print("Nodos: " + str(aux))
print(temp)

t = 0
for i in range(1,temp+1):
    t += (121 - 2*(i-1))
print(t)

"""

#############################
    def _find_longest_vertical_red_path(self):
        longest_path = []
        for x in range(self.game.map_size[0]):
            path = self._find_vertical_red_path(x)
            if path and len(path) > len(longest_path):
                longest_path = path
        return longest_path

    def _find_vertical_red_path(self, x):
        path = []
        for y in range(self.game.map_size[1]):
            if (x, y) in self.game.red_player_positions:
                path.append((x, y))
            else:
                if len(path) >= 2:
                    return path
                path = []
        return path if len(path) >= 2 else None
    def _block_path(self, path):
        x, y_top = path[0]
        print("PATH_TOP: ", path[0])
        x, y_bottom = path[-1]
        print("PATH_BOTTOM: ", path[-1])
        # Intentar bloquear arriba y abajo
        if self._is_valid_move((x, y_top - 1)):
            return (x, y_top - 1)
        if self._is_valid_move((x, y_bottom + 1)):
            return (x, y_bottom + 1)
        
        # Intentar bloquear a los lados
        for _, y in path:
            if self._is_valid_move((x - 1, y)):
                return (x - 1, y)
            if self._is_valid_move((x + 1, y)):
                return (x + 1, y)
        
        return None

    def _continue_blocking(self, column):
        # Buscar el espacio vacío más cercano al centro en la columna de bloqueo
        center = self.game.map_size[1] // 2
        for offset in range(self.game.map_size[1]):
            for sign in [-1, 1]:
                y = center + sign * offset
                if 0 <= y < self.game.map_size[1] and self._is_valid_move((column, y)):
                    return (column, y)
        
        # Si no se puede continuar en la misma columna, buscar en columnas adyacentes
        for dx in [-1, 1]:
            new_column = column + dx
            if 0 <= new_column < self.game.map_size[0]:
                for y in range(self.game.map_size[1]):
                    if self._is_valid_move((new_column, y)):
                        self.blocking_column = new_column
                        return (new_column, y)
        
        self.blocking_column = None
        return None
"""