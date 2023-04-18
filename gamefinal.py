import pygame
import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from enum import Enum


class Color(Enum):
    White = 1
    Black = 2


class Piece(ABC):
    SPRITESHEET = "images/pieces.png"
    _game = None

    @staticmethod
    def set_game(game):
        if not isinstance(game, Game):
            raise ValueError("You must provide a valid Game instance.")
        Piece._game = game

    def __init__(self, color: Color):
        self._color = color
        self._image = pygame.Surface((105, 105), pygame.SRCALPHA)
        self.board = board

    @property
    def color(self):
        return self._color

    def set_image(self, x: int, y: int) -> None:
        self._image.blit(Piece.SPRITESHEET, (0, 0), pygame.rect.Rect(x, y, 105, 105))

    def _diagonal_moves(self, y: int, x: int, distance: int):
        moves = []
        for i in range(1, distance + 1):
            moves += [(y + i, x + i), (y - i, x + i), (y + i, x - i), (y - i, x - i)]
        return moves

    def _horizontal_moves(self, y: int, x: int, distance: int):
        moves = []
        for i in range(1, distance + 1):
            moves += [(y, x + i), (y, x - i)]
        return moves

    def _vertical_moves(self, y: int, x: int, distance: int):
        moves = []
        for i in range(1, distance + 1):
            moves += [(y + i, x), (y - i, x)]
        return moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        moves = self._diagonal_moves(y, x, distance)
        valid_moves = []
        for move in moves:
            y2, x2 = move
            if 0 <= y2 < 8 and 0 <= x2 < 8:
                piece = self.board.get(y2, x2)
                if not piece or piece.color != self.color:
                    valid_moves.append(move)
        return valid_moves

    def get_horizontal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        moves = self._horizontal_moves(y, x, distance)
        valid_moves = []
        for move in moves:
            y2, x2 = move
            if 0 <= y2 < 8 and 0 <= x2 < 8:
                piece = self.board.get(y2, x2)
                if not piece or piece.color != self.color:
                    valid_moves.append(move)
        return valid_moves

    def get_vertical_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        moves = self._vertical_moves(y, x, distance)
        valid_moves = []
        for move in moves:
            y2, x2 = move
            if 0 <= y2 < 8 and 0 <= x2 < 8:
                piece = self.board.get(y2, x2)
                if not piece or piece.color != self.color:
                    valid_moves.append(move)
        return valid_moves
    @abstractmethod
    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def copy(self):
        pass
class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        if color == Color.White:
            self.set_image(0, 0)
        else:
            self.set_image(105, 0)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        moves += self.get_diagonal_moves(y, x, 1)
        moves += self.get_horizontal_moves(y, x, 1)
        moves += self.get_vertical_moves(y, x, 1)
        return moves

    def copy(self):
        return King(self._color)


class Queen(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        if color == Color.White:
            self.set_image(0, 105)
        else:
            self.set_image(105, 105)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        moves += self.get_diagonal_moves(y, x, 8)
        moves += self.get_horizontal_moves(y, x, 8)
        moves += self.get_vertical_moves(y, x, 8)
        return moves

    def copy(self):
        return Queen(self._color)


class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        if color == Color.White:
            self.set_image(0, 210)
        else:
            self.set_image(105, 210)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        return self.get_diagonal_moves(y, x, 8)

    def copy(self):
        return Bishop(self._color)


class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        if color == Color.White:
            self.set_image(0, 315)
        else:
            self.set_image(105, 315)

    def valid_moves(self) -> List[Tuple[int, int]]:
        y, x = self.position
        possible_moves = [
            (y + 2, x + 1),
            (y + 2, x - 1),
            (y - 2, x + 1),
            (y - 2, x - 1),
            (y + 1, x + 2),
            (y + 1, x - 2),
            (y - 1, x + 2),
            (y - 1, x - 2),
        ]

        valid_moves = []
        for move in possible_moves:
            y2, x2 = move
            if 0 <= y2 < 8 and 0 <= x2 < 8:
                piece = self.board.get(y2, x2)
                if not piece or piece.color != self.color:
                    valid_moves.append(move)

        return valid_moves

    def copy(self):
        return Knight(self._color)


class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        if color == Color.White:
            self.set_image(0, 420)
        else:
            self.set_image(105, 420)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        moves += self.get_horizontal_moves(y, x, 8)
        moves += self.get_vertical_moves(y, x, 8)
        return moves

    def copy(self):
        return Rook(self._color)


class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self._has_moved = False
        if color == Color.White:
            self.set_image(0, 525)
        else:
            self.set_image(105, 525)

    def valid_moves(self) -> List[Tuple[int, int]]:
        y, x = self.position
        valid_moves = []

        # Determine the direction of movement based on the Pawn's color
        direction = 1 if self.color == Color.WHITE else -1

        # Check if the Pawn can move forward one space
        if 0 <= y + direction < 8:
            piece = self.board.get(y + direction, x)
            if not piece:
                valid_moves.append((y + direction, x))

                # Check if the Pawn can move forward two spaces (first move only)
                if not self.moved and 0 <= y + 2 * direction < 8:
                    piece = self.board.get(y + 2 * direction, x)
                    if not piece:
                        valid_moves.append((y + 2 * direction, x))

        # Check if the Pawn can capture an opponent's piece diagonally
        for dx in [-1, 1]:
            if 0 <= x + dx < 8 and 0 <= y + direction < 8:
                piece = self.board.get(y + direction, x + dx)
                if piece and piece.color != self.color:
                    valid_moves.append((y + direction, x + dx))

        return valid_moves

    def copy(self):
        new_pawn = Pawn(self._color)
        new_pawn._has_moved = self._has_moved
        return new_pawn


class Game:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = random.choice([Color.White, Color.Black])
        self.prior_states = []
        self._setup_pieces()

    def reset(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = random.choice([Color.White, Color.Black])
        self.prior_states = []
        self._setup_pieces()

    def _setup_pieces(self):
        for i in range(8):
            self.board[1][i] = Pawn(self, Color.BLACK, (1, i))
            self.board[6][i] = Pawn(self, Color.WHITE, (6, i))

        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece in enumerate(pieces):
            self.board[0][i] = piece(self, Color.BLACK, 0, i)
            self.board[7][i] = piece(self, Color.WHITE, 7, i)

    def get(self, y: int, x: int) -> Optional[Piece]:
        if 0 <= y < 8 and 0 <= x < 8:
            return self.board[y][x]
        return None

    def switch_player(self):
        self.current_player = Color.White if self.current_player == Color.Black else Color.Black

    def undo(self) -> bool:
        if self.prior_states:
            self.board = self.prior_states.pop()
            self.switch_player()
            return True
        return False

    def copy_board(self):
        new_board = [[piece.copy() if piece else None for piece in row] for row in self.board]
        return new_board

    def move(self, y1: int, x1: int, y2: int, x2: int) -> bool:
        piece = self.get(y1, x1)
        if not piece or (y2, x2) not in piece.valid_moves():
            return False

        self.prior_states.append(self.copy_board())
        captured_piece = self.get(y2, x2)
        piece.move(y2, x2)

        if self.check(piece.color):
            self.undo()
            return False

        if isinstance(piece, Pawn) and (y2 == 0 or y2 == 7):
            self.board[y2][x2] = Queen(self, piece.color, (y2, x2))

        self.switch_player()
        return True

    def get_piece_locations(self, color: Color) -> List[Tuple[int, int]]:
        locations = []
        for y in range(8):
            for x in range(8):
                piece = self.get(y, x)
                if piece and piece.color == color:
                    locations.append((y, x))
        return locations

    def find_king(self, color: Color) -> Tuple[int, int]:
        for y in range(8):
            for x in range(8):
                piece = self.get(y, x)
                if piece and piece.color == color and isinstance(piece, King):
                    return y, x
        return -1, -1  # should not happen

    def check(self, color: Color) -> bool:
        opponent_color = Color.White if color == Color.Black else Color.Black
        opponent_locations = self.get_piece_locations(opponent_color)
        possible_moves = []
        for loc in opponent_locations:
            y, x = loc
            piece = self.get(y, x)
            possible_moves += piece.valid_moves(y, x)

        king_y, king_x = self.find_king(color)
        return (king_y, king_x) in possible_moves

    def mate(self, color: Color) -> bool:
        if not self.check(color):
            return False

        all_valid_moves = []
        for y in range(8):
            for x in range(8):
                piece = self.get(y, x)
                if piece and piece.color == color:
                    all_valid_moves.extend([(y, x, y2, x2) for y2, x2 in piece.valid_moves()])

        for y1, x1, y2, x2 in all_valid_moves:
            self.move(y1, x1, y2, x2)
            if not self.check(color):
                self.undo()
                return False
            self.undo()

        return True

    def _computer_move(self):
        valid_moves = []
        for y in range(8):
            for x in range(8):
                piece = self.get(y, x)
                if piece and piece.color == self.current_player:
                    valid_moves.extend([(y, x, y2, x2) for y2, x2 in piece.valid_moves()])

        if valid_moves:
            move = random.choice(valid_moves)
            self.move(*move)