import pygame
from typing import List, Tuple
from enum import Enum


class Color(Enum):
    White = 1
    Black = 2


class Piece:
    SPRITESHEET = pygame.image.load("images/pieces.png")

    def __init__(self, color: Color):
        self._color = color
        self._image = pygame.Surface((105, 105), pygame.SRCALPHA)

    @property
    def color(self):
        return self._color

    def set_image(self, x: int, y: int) -> None:
        self._image.blit(Piece.SPRITESHEET, (0, 0), pygame.rect.Rect(x, y, 105, 105))

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        pass

    def copy(self):
        pass


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        x = 0 if color == Color.White else 105
        y = 525
        self.set_image(x, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        moves = []

        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx
            if 0 <= new_y < 8 and 0 <= new_x < 8:
                moves.append((new_y, new_x))

        return moves

    def copy(self):
        return King(self.color)


class Queen(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        x = 210 if color == Color.White else 315
        y = 525
        self.set_image(x, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        moves.extend(self.get_diagonal_moves(y, x))
        moves.extend(self.get_horizontal_moves(y, x))
        moves.extend(self.get_vertical_moves(y, x))

        return moves

    def copy(self):
        return Queen(self.color)

class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        x = 630 if color == Color.White else 735
        y = 525
        self.set_image(x, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        directions = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]
        moves = []


        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx
            if 0 <= new_y < 8 and 0 <= new_x < 8:
                moves.append((new_y, new_x))

        return moves

    def copy(self):
        return King(self.color)


class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        x = 420 if color == Color.White else 525
        y = 525
        self.set_image(x, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        return self.get_diagonal_moves(y, x)

    def copy(self):
        return Bishop(self.color)

class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        x = 840 if color == Color.White else 945
        y = 525
        self.set_image(x, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        moves.extend(self.get_horizontal_moves(y, x))
        moves.extend(self.get_vertical_moves(y, x))

        return moves

    def copy(self):
        return Rook(self.color)


class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        x = 1050 if color == Color.White else 1155
        y = 525
        self.set_image(x, y)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        direction = -1 if self.color == Color.White else 1

        # Move forward one square
        new_y = y + direction
        if 0 <= new_y < 8:
            moves.append((new_y, x))

        # Move forward two squares if on starting rank
        if (self.color == Color.White and y == 6) or (self.color == Color.Black and y == 1):
            new_y = y + (2 * direction)
            if 0 <= new_y < 8:
                moves.append((new_y, x))

        return moves

    def copy(self):
        return Pawn(self.color)


class Game:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self._setup_pieces()

    def _setup_pieces(self):
        for x in range(8):
            # Add Pawns
            self.board[1][x] = Pawn(Color.Black)
            self.board[6][x] = Pawn(Color.White)

        # Add Rooks
        self.board[0][0] = Rook(Color.Black)
        self.board[0][7] = Rook(Color.Black)
        self.board[7][0] = Rook(Color.White)
        self.board[7][7] = Rook(Color.White)

        # Add Knights
        self.board[0][1] = Knight(Color.Black)
        self.board[0][6] = Knight(Color.Black)
        self.board[7][1] = Knight(Color.White)
        self.board[7][6] = Knight(Color.White)
        # add bishops
        self.board[0][2] = Bishop(Color.White)
        self.board[0][5] = Bishop(Color.White)
        self.board[7][2] = Bishop(Color.Black)
        self.board[7][5] = Bishop(Color.Black)

        # add knights
        self.board[0][1] = Knight(Color.White)
        self.board[0][6] = Knight(Color.White)
        self.board[7][1] = Knight(Color.Black)
        self.board[7][6] = Knight(Color.Black)

        # add rooks
        self.board[0][0] = Rook(Color.White)
        self.board[0][7] = Rook(Color.White)
        self.board[7][0] = Rook(Color.Black)
        self.board[7][7] = Rook(Color.Black)

        # add queens
        self.board[0][3] = Queen(Color.White)
        self.board[7][3] = Queen(Color.Black)

        # add kings
        self.board[0][4] = King(Color.White)
        self.board[7][4] = King(Color.Black)

        # add pawns
        for i in range(8):
            self.board[1][i] = Pawn(Color.White)
            self.board[6][i] = Pawn(Color.Black)

        # Set images for all pieces
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    self.board[i][j].set_image(j * 105, i * 105)