import graphviz
import os
class DisjointSetWeighted:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n
        self.n = n

    def find(self, u):
        if u != self.parent[u]:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        print(f"Union nodes {u} (root {root_u}) and {v} (root {root_v})")
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

    def show(self, player):
        dot = graphviz.Digraph(comment=f'Disjoint Set {player}')
        for i in range(self.n):
            dot.node(str(i))
        for i in range(self.n):
            if i != self.parent[i]:
                dot.edge(str(self.parent[i]), str(i))
        dot.view()

    def save(self, output_path):
        dot = graphviz.Digraph(comment='Disjoint Set')
        for i in range(self.n):
            dot.node(str(i))
        for i in range(self.n):
            if i != self.parent[i]:
                dot.edge(str(self.parent[i]), str(i))

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        dot.render(output_path, format='png', cleanup=False)
        print(f"Graphviz output saved to {output_path}.png")