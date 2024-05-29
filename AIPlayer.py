class AIPlayer:
    def __init__(self, renderer):
        self.renderer = renderer

    def make_move(self):
        raise NotImplementedError