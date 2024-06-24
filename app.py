import pygame
from HexDeform import Renderer

class StartScreen:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("HEX GAME")
        self.font_title = pygame.font.Font("fonts/Blox2.ttf", 150)
        self.font = pygame.font.Font("fonts/mytype.ttf", 48)
        self.title = self.font_title.render("HEX GAME", True, (255, 255, 255))
        self.title_rect = self.title.get_rect()
        self.title_rect.midtop = (width // 2, 50)

        self.start_normal_button = self.font.render("P(Blue) vs P(Red)", True, (255, 255, 255))# (Dijkstra)
        self.start_normal_rect = self.start_normal_button.get_rect()
        self.start_normal_rect.center = (width // 2, height // 2)

        self.start_hard_button = self.font.render("Bot(Blue) vs Bot(Red)", True, (255, 255, 255))#  (Monte Carlo Tree Search)
        self.start_hard_rect = self.start_hard_button.get_rect()
        self.start_hard_rect.center = (width // 2, height // 2 + 50)
        self.default_width = width
        self.default_height = height

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_normal_rect.collidepoint(event.pos):
                        difficulty = "Player(Blue) vs Player(Red)"
                        renderer = Renderer(difficulty)
                        renderer.run(self.show_difficulty_menu)
                    elif self.start_hard_rect.collidepoint(event.pos):
                        difficulty = "Bot(Blue) vs Bot(Red)"
                        renderer = Renderer(difficulty)
                        renderer.run(self.show_difficulty_menu)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.title, self.title_rect)
            self.screen.blit(self.start_normal_button, self.start_normal_rect)
            self.screen.blit(self.start_hard_button, self.start_hard_rect)
            pygame.display.flip()

        pygame.quit()

    def show_difficulty_menu(self):
        pygame.display.set_mode((self.default_width, self.default_height))
        self.run()

if __name__ == "__main__":
    start_screen = StartScreen(800, 600)
    start_screen.run()