class DisjointSet:
    def __init__(self, game):
        self.parent = {}
        self.rank = {}
        self.map_width, self.map_height = game.map_size
        self.game = game

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

    def get_connected_components(self, color):
        components = {}
        for y in range(self.map_height):
            for x in range(self.map_width):
                if (x, y) in self.game.red_player_positions and color == "red":
                    root = self.find((x, y))
                    if root not in components:
                        components[root] = []
                    components[root].append((x, y))
                elif (x, y) in self.game.blue_player_positions and color == "blue":
                    root = self.find((x, y))
                    if root not in components:
                        components[root] = []
                    components[root].append((x, y))
        return components

    def get_largest_component(self, color):
        components = self.get_connected_components(color)
        return max(components.values(), key=len) if components else []
