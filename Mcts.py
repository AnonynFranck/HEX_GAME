import time
import random
from math import sqrt, log
from copy import copy, deepcopy
from sys import stderr
from queue import Queue
inf = float('inf')

class HexNode:
    """
    Node for the MCST. Stores the move applied to reach this node from its parent,
    stats for the associated game position, children, parent and outcome 
    (outcome==none unless the position ends the game).
    """
    def __init__(self, position=None, parent=None):
        """
        Initialize a new node with optional position and parent and initially empty
        children list and rollout statistics and unspecified outcome.
        """
        self.position = position
        self.parent = parent
        self.N = 0  # times this position was visited
        self.Q = 0  # average reward (wins-losses) from this position
        self.children = []
        self.outcome = None  # Will be set to 'red' or 'blue' when the game ends

    def add_children(self, children):
        """
        Add a list of nodes to the children of this node.
        """
        self.children += children

    def set_outcome(self, outcome):
        """
        Set the outcome of this node (i.e. if we decide the node is the end of
        the game)
        """
        self.outcome = outcome

    def value(self, explore):
        """
        Calculate the UCT value of this node relative to its parent, the parameter
        "explore" specifies how much the value should favor nodes that have
        yet to be thoroughly explored versus nodes that seem to have a high win
        rate. 
        Currently explore is set to zero when choosing the best move to play so
        that the move with the highest winrate is always chosen. When searching
        explore is set to EXPLORATION specified above.
        """
        # unless explore is set to zero, maximally favor unexplored nodes
        if self.N == 0:
            if explore == 0:
                return 0
            else:
                return inf
        else:
            return self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)


class MCTSAgentHex:
    """
    Basic no frills implementation of an agent that performs MCTS for Hex.
    """
    EXPLORATION = 1

    def __init__(self, renderer):
        self.renderer = renderer
        self.root = HexNode()
        self.reset_root()

    def reset_root(self):
        """
        Reset the root node based on the current game state.
        """
        self.root = HexNode(position=tuple(self.renderer.occupied_positions))
    def best_move(self):
        """
        Return the best move according to the current tree.
        """
        if self.renderer.winner is not None:
            return None  # El juego ha terminado, no hay movimientos que hacer

        # Elige el movimiento del nodo más simulado, rompiendo empates al azar
        max_value = max(self.root.children, key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children if n.N == max_value]
        best_child = random.choice(max_nodes)
        return best_child.position

    def make_move(self):
        """
        Make the passed move and update the tree appropriately.
        """
        self.search()  # Realizar una simulación MCTS
        best_move = self.best_move()
        print("BM: ", best_move)
        if best_move is not None:
                
            best_move = best_move[1]  # Obtener solo la segunda tupla (la mejor jugada)
            print( "BEST_MOVE[1] : " , best_move )
            self.renderer.red_player_positions.add(best_move)
            self.renderer.occupied_positions.add(best_move)
            print("Rende PLAYER RED: ",self.renderer.red_player_positions )
            print("Rende OCCUPOED: ", self.renderer.occupied_positions)
            # Actualizar el estado de juego después del movim   iento
            # print(best_move, " ====> ", self.renderer.disjoint_set.red_bottom_node)
            self.renderer.disjoint_set.union(best_move, self.renderer.disjoint_set.red_bottom_node)
            for neighbor in self.renderer.get_neighbors(*best_move):
                if neighbor in self.renderer.red_player_positions:
                    self.renderer.disjoint_set.union(best_move, neighbor)

            self.renderer.current_player = "blue"
            self.renderer.winner = self.renderer.disjoint_set.check_win()

            self.move(best_move)
    def move(self, move):
        for child in self.root.children:
            if move == child.position:
                child.parent = None
                self.root = child
                self.reset_root()
                return

        self.reset_root()

    def search(self):
        """
        Search and update the search tree for a specified amount of time in seconds.
        """
        node, state = self.select_node()
        print("NODO: ", node, "STATE: ", state)
        turn = self.renderer.current_player
        outcome = self.roll_out(state)
        self.backup(node, turn, outcome)

    def select_node(self):
        """
        Select a node in the tree to perform a single simulation from.
        """
        node = self.root
        state = tuple(self.renderer.occupied_positions)

        # stop if we reach a leaf node
        while len(node.children) != 0:
            # descend to the maximum value node, break ties at random
            max_value = max(node.children, key=lambda n: n.value(self.EXPLORATION)).value(self.EXPLORATION)
            max_nodes = [n for n in node.children if n.value(self.EXPLORATION) == max_value]
            node = random.choice(max_nodes)
            state = node.position

            # if some child node has not been explored, select it before expanding
            # other children
            if node.N == 0:
                return node, state

        # if we reach a leaf node, generate its children and return one of them
        # if the node is terminal, just return the terminal node
        if self.expand(node, state):
            if node.children:  # Check if the node has children
                node = random.choice(node.children)
                state = node.position
        return node, state

    def roll_out(self, state):
        """
        Simulate an entirely random game from the passed state and return the winning
        player.
        """
        # Crear una copia del estado actual del juego
        game_state = self.renderer.copy_state()
        print("STATE_ROLL: ", state)
        # Actualizar el estado de juego temporal con el estado pasado
        game_state['occupied_positions'].update(state)
        if self.renderer.current_player == "red":
            game_state['red_player_positions'].update(state)
        #else:
            # game_state['blue_player_positions'].update(state)

        moves = self.get_available_moves(state)
        print("get_available_moves: ", moves)
        while self.renderer.winner is None:
            if not moves:
                break
            move = random.choice(moves)
            print("MOVES_DE_ROLLOUT: ", move)
            game_state['occupied_positions'].add(move)
            if self.renderer.current_player == "red" and move not in self.renderer.occupied_positions:
                #pass 
                game_state['red_player_positions'].add(move)
                self.renderer.red_player_positions.add(move)
            #else:
                #self.renderer.red_player_positions.add(move)
                #game_state['red_player_positions'].add(move)
            #    game_state['blue_player_positions'].add(move)
            moves.remove(move)
            self.renderer.current_player = "blue" if self.renderer.current_player == "red" else "red"

        # Restaurar el estado del juego original
        # self.renderer.occupied_positions = game_state['occupied_positions']
        # self.renderer.red_player_positions = game_state['red_player_positions']
        # self.renderer.blue_player_positions = game_state['blue_player_positions']
        # self.renderer.current_player = game_state['current_player']
        # self.renderer.winner = game_state['winner']

        return self.renderer.winner

    def backup(self, node, turn, outcome):
        """
        Update the node statistics on the path from the passed node to root to reflect
        the outcome of a randomly simulated playout.
        """
        # note that reward is calculated for the player who just played
        # at the node and not the next player to play
        reward = 1 if outcome == turn else -1

        while node is not None:
            node.N += 1
            node.Q += reward
            reward = -reward
            node = node.parent

    def expand(self, parent, state):
        """
        Generate the children of the passed "parent" node based on the available
        moves in the passed game state and add them to the tree.
        """
        children = []
        if self.renderer.winner is not None:
            # game is over at this node, so nothing to expand
            return False

        for move in self.get_available_moves(state):
            new_state = list(state)
            new_state.append(move)
            children.append(HexNode(tuple(new_state), parent))

        parent.add_children(children)
        return True

    def get_available_moves(self, state):
        """
        Get a list of available moves based on the current game state and game rules.
        """
        available_moves = []
        current_player = self.renderer.current_player

        for x in range(self.renderer.map_size[0]):
            for y in range(self.renderer.map_size[1]):
                if (x, y) not in state and (x, y) not in self.renderer.occupied_positions:
                    if current_player == "red":
                        if y == 0 or (x, y - 1) in state:
                            available_moves.append((x, y))
                    elif current_player == "blue":
                        if x == 0 or (x - 1, y) in state:
                            available_moves.append((x, y))

        return available_moves

    def tree_size(self):
        """
        Count nodes in the tree by Breadth-First Search (BFS).
        """
        queue = Queue()
        count = 0
        queue.put(self.root)
        while not queue.empty():
            node = queue.get()
            count += 1
            for child in node.children:
                queue.put(child)
        return count
