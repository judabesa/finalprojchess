import pygame_gui as gui
from pygame.locals import *
from game import Game
import pygame
import pygame as pg
import chessengine

IMAGES = {}
SQUARE_SIZE = 80
SQ_SIZE = 64
WIDTH, HEIGHT = 512, 512

class Color:
    WHITE = Color('white')
    BLACK = Color('black')


def get_clicked_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def __get_coords__(y, x):
    grid_x = x // 105
    grid_y = y // 105
    return grid_y, grid_x


class GUI:
    def __init__(self) -> None:
        self.check_for_events = None
        pg.init()
        self._game = Game()
        self._screen = pg.display.set_mode((1440, 900))
        pg.display.set_caption("Laker Chess")
        self._pieces = pg.image.load("./images/pieces.png")
        self._ui_manager = gui.UIManager((1440, 900))
        self._side_box = gui.elements.UITextBox('<b>Laker Chess</b><br /><br />White moves first.<br />',
                                                relative_rect=pg.Rect((1000, 100), (400, 500)),
                                                manager=self._ui_manager)
        self._undo_button = gui.elements.UIButton(relative_rect=pg.Rect((1000, 50), (100, 50)), text='Undo',
                                                  manager=self._ui_manager)
        self._restart_button = gui.elements.UIButton(relative_rect=pg.Rect((1200, 50), (100, 50)), text='Reset',
                                                     manager=self._ui_manager)
        self._piece_selected = False
        self._first_selected = (0, 0)
        self._second_selected = (0, 0)
        self._valid_moves = []
        self.game = Game()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.surface = pygame.Surface((WIDTH, HEIGHT))

    def run_game(self) -> None:
        global event
        running = True
        time_delta = 0
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    y, x = __get_coords__(y, x)
                    piece = self._game.get_piece(y, x)
                    if not self._piece_selected and piece:
                        if piece.color != self._game.turn:
                            continue
                        self._piece_selected = True
                        self._first_selected = y, x
                        self._valid_moves = piece.valid_moves(y, x)
                        self._piece_selected = piece
                    elif self._piece_selected and (y, x) in self._valid_moves:
                        target = self._game.get_piece(y, x)
                        moved = self._game.move(self._piece_selected, self._first_selected[0])
                        if moved:
                            self._side_box.append_html_text(self._piece_selected.color.name + ' moved '
                                                            + str(type(self._piece_selected).__name__))
                            if target:
                                self._side_box.append_html_text(' and captures ' + str(type(target).__name__))
                            self._side_box.append_html_text('<br />')
                            computer_message = self._game._computer_move()
                            if computer_message:
                                self._side_box.append_html_text(computer_message)
                        else:
                            self._side_box.append_html_text('Invalid move.  Would leave '
                                                            + str(self._piece_selected.color.name) + ' in check.<br />')
                        if self._game.check(Color.WHITE):
                            self._side_box.append_html_text("WHITE is in CHECK!<br />")
                        if self._game.check(Color.BLACK):
                            self._side_box.append_html_text("BLACK is in CHECK!<br />")
                        if self._game.mate(Color.WHITE):
                            self._side_box.append_html_text("WHITE is in CHECKMATE!<br />GAME OVER!")
                        if self._game.mate(Color.BLACK):
                            self._side_box.append_html_text("BLACK is in CHECKMATE!<br />GAME OVER!")

                        self._piece_selected = False
                    else:
                        self._piece_selected = False
                if event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self._restart_button:
                        self._game.reset()
                        self._side_box.set_text("Restarting game...<br />")
                    if event.ui_element == self._undo_button:
                        if self._game.undo():
                            self._side_box.append_html_text('Undoing move.<br />')
                        else:
                            self._side_box.append_html_text('Nothing to undo.<br />')
            self._ui_manager.process_events(event)

            self._screen.fill((255, 255, 255))
            self.__draw_board__()
            self._ui_manager.draw_ui(self._screen)
            self._ui_manager.update(time_delta)

            pg.display.flip()
            time_delta = clock.tick(30) / 1000.0

    def __draw_board__(self, game):
        self.surface.fill(pg.Color("white"))
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == 1:
                    pg.draw.rect(
                        self.surface,
                        pg.Color("gray"),
                        pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                    )

        # Draw the chess pieces
        for r in range(8):
            for c in range(8):
                piece = game.board[r][c]
                if piece != '--':
                    self.surface.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def left_click(self, event):
        row, col = get_clicked_pos(event.pos)
        selected_piece = self.game.get_piece(row, col)
        if selected_piece is not None and selected_piece.color == self.game.turn:
            self.selected_piece = selected_piece
        else:
            if self.selected_piece is not None:
                self.game.move_piece(self.selected_piece.pos, (row, col))
            self.selected_piece = None

    def right_click(self, event):
        row, col = get_clicked_pos(event.pos)
        self.game.place_piece(row, col)

    def update(self):
        self.__draw_board__()
        pg.display.update()

    def load_images(self):
        pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']
        for piece in pieces:
            IMAGES[piece] = pygame.image.load(f"images/{piece}.png")


def main():
    pg.init()
    pg.display.set_caption("Chess")
    g = GUI()
    clock = pg.time.Clock()

    # Create a new game instance
    game = chessengine.GameState()

    # ...

    # Draw the initial board
    g.__draw_board__(game)

    # ...

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # ...

        # Draw the board
        g.__draw_board__(game)

        # ...

    pg.quit()
