import pygame
from gamefinal import Game, Color

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ChessGUI:
    def __init__(self):
        self._game = Game()
        self._screen = pygame.display.set_mode((840, 840))
        pygame.display.set_caption("Chess")

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self._draw_board()
            self._draw_pieces()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def _draw_board(self):
        for y in range(8):
            for x in range(8):
                color = WHITE if (x + y) % 2 == 0 else BLACK
                pygame.draw.rect(self._screen, color, pygame.Rect(x * 105, y * 105, 105, 105))

    def _draw_pieces(self):
        for y in range(8):
            for x in range(8):
                piece = self._game.board[y][x]
                if piece is not None:
                    self._screen.blit(piece._image, (x * 105, y * 105))


if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()
