import pygame
from gamefinal import Game, Color

pygame.init()

WIDTH = 840
HEIGHT = 840
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

game = Game()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    WINDOW.fill(WHITE)

    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x * 105, y * 105, 105, 105)
            if (x + y) % 2 == 0:
                pygame.draw.rect(WINDOW, WHITE, rect)
            else:
                pygame.draw.rect(WINDOW, BLACK, rect)

            piece = game.board[y][x]
            if piece:
                WINDOW.blit(piece._image, rect)

    pygame.display.flip()
    clock.tick(FPS)
