import pygame
import sys
from gamefinal import Game, Color

# ...

class ChessGUI:
    def __init__(self, game):
        self._game = game
        self._screen = pygame.display.set_mode((840, 840))
        pygame.display.set_caption("Chess")

        self._board = pygame.image.load("images/board.png")
        self._selected_square = None

        self._clock = pygame.time.Clock()

    def _draw_pieces(self):
        # Your implementation here

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type ==                 pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Left mouse button
                        x, y = pygame.mouse.get_pos()
                        self._selected_square = self._get_square_from_pixel(x, y)
                        # Add your move handling logic here

            self._screen.blit(self._board, (0, 0))
            self._draw_pieces()

            pygame.display.flip()
            self._clock.tick(60)

    def _get_square_from_pixel(self, x: int, y: int) -> Tuple[int, int]:
        return y // 105, x // 105

if __name__ == "__main__":
    pygame.init()

    game = Game()
    gui = ChessGUI(game)
    gui.run()

