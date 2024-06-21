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
        #if self.is_valid_position(x) and self.is_valid_position(y):
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

    #def is_valid_position(self, pos):
    #    x, y = pos
    #    print(x, " === ", y)
    #    return (x >= 0 and x < self.map_width) and (y >= 0 and y < self.map_height)
        

    def check_win(self):
        # Verificar si los nodos auxiliares rojos están conectados
        if self.find(self.red_top_node) == self.find(self.red_bottom_node):
            return "red"

        # Verificar si los nodos auxiliares azules están conectados
        if self.find(self.blue_left_node) == self.find(self.blue_right_node):
            return "blue"

        return None