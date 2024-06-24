class GreedyBlueAIPlayer:
    def __init__(self, game):
        self.game = game
        self.last_move = None
        self.nodesB = 0 # B Nodes

    def get_NodesB(self):
        return self.nodesB

    def make_move(self):
        if self.game.current_player == "blue" and not self.game.winner:
            move = self._get_best_move() # Best Move
            print("MOVE: ", move)
            if move and move not in self.game.occupied_positions:
                self.game.handle_mouse_click(self.game.convert_hex_to_pixel_coords(*move))
                self.last_move = move
                self.nodesB += 1

    def _get_best_move(self):
        red_component = self.game.disjoint_set.get_largest_component("red")
        #print("RED_COMPONENT: ", red_component)
        if red_component:
            blocking_move = self._find_blocking_move(red_component)
            #print("FIND_ADVANCING_MOVE: ", blocking_move)
            if blocking_move:
                return blocking_move
        return self._find_advancing_move()

    def _find_blocking_move(self, red_component):
        bottom_positions = sorted(red_component, key=lambda pos: (-pos[1], pos[0]))
        for x, y in bottom_positions:
            below = (x, y + 1)
            if self._is_valid_move(below):
                return below
            
            below_left = (x - 1, y + 1)
            if self._is_valid_move(below_left):
                return below_left
            
            below_right = (x + 1, y)
            if self._is_valid_move(below_right):
                return below_right

        # Si no se puede bloquear directamente debajo, intentar bloquear a los lados
        for x, y in red_component:
            left = (x - 1, y)
            right = (x + 1, y)
            if self._is_valid_move(left):
                return left
            if self._is_valid_move(right):
                return right

        return None

    def _find_advancing_move(self):
        blue_component = self.game.disjoint_set.get_largest_component("blue")
        #print("BLUE_COMPONENT: ", blue_component)
        if not blue_component:
            return (self.game.map_size[0] // 2, self.game.map_size[1] // 2)
        
        potential_moves = set()
        for x, y in blue_component:
            neighbors = self.game.get_neighbors(x, y)
            potential_moves.update(neighbors)
        
        valid_moves = [move for move in potential_moves if self._is_valid_move(move)]
        
        if valid_moves:
            return max(valid_moves, key=lambda move: move[0])
        return None

    def _is_valid_move(self, pos):
        x, y = pos
        return (0 <= x < self.game.map_size[0] and 
                0 <= y < self.game.map_size[1] and 
                (x, y) not in self.game.occupied_positions)
