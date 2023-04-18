import pygame
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from enum import Enum

pygame.init()

class Color(Enum):
    White = 1
    Black = 2


class Piece(ABC):
    SPRITESHEET = pygame.image.load("venv/Scripts/images/pieces.png")
    _game = None

    @staticmethod
    def set_game(game):
        if not isinstance(game, Game):
            raise ValueError("You must provide a valid Game instance.")
        Piece._game = game

    def __init__(self, color: Color):
        self._color = color
        self._image = pygame.Surface((105, 105), pygame.SRCALPHA)

    @property
    def color(self):
        return self._color

    def set_image(self, x: int, y: int) -> None:
        self._image.blit(Piece.SPRITESHEET, (0, 0), pygame.rect.Rect(x, y, 105, 105))

    def _diagonal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        moves = []
        for y_d in (-1, 1):
            for x_d in (-1, 1):
                moves.extend(self._game.get_moves_in_line(y, x, y_d, x_d, distance))
        return moves

    def _horizontal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        moves = []
        for x_d in (-1, 1):
            moves.extend(self._game.get_moves_in_line(y, x, 0, x_d, distance))
        return moves

    def _vertical_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        moves = []
        for y_d in (-1, 1):
            moves.extend(self._game.get_moves_in_line(y, x, y_d, 0, distance))
        return moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        return self._diagonal_moves(y, x, distance)

    def get_horizontal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        return self._horizontal_moves(y, x, distance)

    def get_vertical_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        return self._vertical_moves(y, x, distance)

    @abstractmethod
    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def copy(self):
        pass


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        y = 0 if color == Color.WHITE else 105
        self.set_image(0, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        horizontal = self.get_horizontal_moves(y, x, 1)
        vertical = self.get_vertical_moves(y, x, 1)
        diagonal = self.get_diagonal_moves(y, x, 1)
        return horizontal + vertical + diagonal

    def copy(self):
        return King(self._color)

class Queen(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        y = 0 if color == Color.WHITE else 105
        self.set_image(525, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        horizontal = self.get_horizontal_moves(y, x, 8)
        vertical = self.get_vertical_moves(y, x, 8)
        diagonal = self.get_diagonal_moves(y, x, 8)
        return horizontal + vertical + diagonal

    def copy(self):
        return Queen(self._color)


class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        y = 0 if color == Color.WHITE else 105
        self.set_image(315, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        return self.get_diagonal_moves(y, x, 8)

    def copy(self):
        return Bishop(self._color)


class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        y = 0 if color == Color.WHITE else 105
        self.set_image(210, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        for y_d in (-2, -1, 1, 2):
            for x_d in (-2, -1, 1, 2):
                if abs(y_d) != abs(x_d):
                    moves.append((y + y_d, x + x_d))
        return [move for move in moves if self._game.is_valid_move(y, x, *move)]

    def copy(self):
        return Knight(self._color)


class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        y = 0 if color == Color.WHITE else 105
        self.set_image(105, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        horizontal = self.get_horizontal_moves(y, x, 8)
        vertical = self.get_vertical_moves(y, x, 8)
        return horizontal + vertical

    def copy(self):
        return Rook(self._color)


class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        y = 0 if color == Color.WHITE else 105
        self.set_image(420, y)
        self._first_move = True

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        y_d = -1 if self._color == Color.WHITE else 1
        forward = (y + y_d, x)
        if self._game.is_valid_move(y, x, *forward, same_color=False):
            moves.append(forward)

        if self._first_move:
            double_forward = (y + 2 * y_d, x)
            if self._game.is_valid_move(y, x, *double_forward, same_color=False):
                moves.append(double_forward)

        for x_d in (-1, 1):
            capture = (y + y_d, x + x_d)
            if self._game.is_valid_move(y, x, *capture, same_color=True):
                moves.append(capture)

        return moves

        def copy(self):
            new_pawn = Pawn(self._color)
            new_pawn._first_move = self._first_move
            return new_pawn

    class Game:
        def __init__(self):
            self.board = [[None for _ in range(8)] for _ in range(8)]
            self._setup_pieces()

        def _setup_pieces(self):
            for i in range(8):
                self.board[1][i] = Pawn(Color.BLACK)
                self.board[6][i] = Pawn(Color.WHITE)

            for i, cls in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                self.board[0][i] = cls(Color.BLACK)
                self.board[7][i] = cls(Color.WHITE)

        def is_valid_move(self, y: int, x: int, y_to: int, x_to: int, same_color: bool = False) -> bool:
            if not (0 <= y_to < 8 and 0 <= x_to < 8):
                return False
            if not same_color and self.board[y_to][x_to] is not None and self.board[y_to][x_to].color == self.board[y][
                x].color:
                return False
            return True

        def get_moves_in_line(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> List[Tuple[int, int]]:
            moves = []
            for i in range(1, distance + 1):
                y_to, x_to = y + y_d * i, x + x_d * i
                if not self.is_valid_move(y, x, y_to, x_to):
                    break
                moves.append((y_to, x_to))
                if self.board[y_to][x_to] is not None:
                    break
            return moves

        def move(self, y_from: int, x_from: int, y_to: int, x_to: int) -> None:
            if not self.is_valid_move(y_from, x_from, y_to, x_to):
                raise ValueError("Invalid move")

            piece = self.board[y_from][x_from]
            if piece is None:
                raise ValueError("No piece at the given position")

            if (y_to, x_to) not in piece.valid_moves(y_from, x_from):
                raise ValueError("The piece cannot move to the given position")

            self.board[y_to][x_to] = piece
            self.board[y_from][x_from] = None
            if isinstance(piece, Pawn):
                piece._first_move = False
