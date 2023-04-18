import pygame as pg
from typing import Optional

class Piece:
    SPRITESHEET = pg.image.load('./images/pieces.png')
    SPRITE_SIZE = 64

    def __init__(self, color, game):
        self.game = game
        self.color = color

    def is_valid_move(self, start, end):
        raise NotImplementedError("This method should be implemented in the subclass")

    def get_sprite(self):
        raise NotImplementedError("This method should be implemented in the subclass")

    def get_piece_sprite(self, x, y):
        rect = (self.SPRITE_SIZE * x, self.SPRITE_SIZE * y, self.SPRITE_SIZE, self.SPRITE_SIZE)
        return self.SPRITESHEET.subsurface(rect)


class King(Piece):
    def is_valid_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        self.pos = None

        if row_diff <= 1 and col_diff <= 1:
            target_piece = self.game.get_piece(*end)
            if target_piece is None or target_piece.color != self.color:
                return True

        return False

    def get_sprite(self):
        x, y = (0, 0) if self.color == 'white' else (0, 1)
        return self.get_piece_sprite(x, y)


class Queen(Piece):
    def is_valid_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])

        # Check if the move is diagonal, horizontal, or vertical
        if row_diff == col_diff or start[0] == end[0] or start[1] == end[1]:
            # Check if there are no pieces blocking the path
            direction = (int((end[0] - start[0]) / max(row_diff, 1)), int((end[1] - start[1]) / max(col_diff, 1)))
            current_row, current_col = start[0] + direction[0], start[1] + direction[1]

            while (current_row, current_col) != end:
                if self.game.get_piece(current_row, current_col) is not None:
                    return False
                current_row += direction[0]
                current_col += direction[1]

            # If the target square is empty or contains an opponent's piece, the move is valid
            target_piece = self.game.get_piece(*end)
            if target_piece is None or target_piece.color != self.color:
                return True

        return False

    def get_sprite(self):
        x, y = (1, 0) if self.color == 'white' else (1, 1)
        return self.get_piece_sprite(x, y)


class Rook(Piece):
    def is_valid_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])

        # Check if the move is horizontal or vertical
        if start[0] == end[0] or start[1] == end[1]:
            # Check if there are no pieces blocking the path
            direction = (int((end[0] - start[0]) / max(row_diff, 1)), int((end[1] - start[1]) / max(col_diff, 1)))
            current_row, current_col = start[0] + direction[0], start[1] + direction[1]

            while (current_row, current_col) != end:
                if self.game.get_piece(current_row, current_col) is not None:
                    return False
                current_row += direction[0]
                current_col += direction[1]

            # If the target square is empty or contains an opponent's piece, the move is valid
            target_piece = self.game.get_piece(*end)
            if target_piece is None or target_piece.color != self.color:
                return True

        return False

    def get_sprite(self):
        x, y = (4, 0) if self.color == 'white' else (4, 1)
        return self.get_piece_sprite(x, y)


class Bishop(Piece):
    def is_valid_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])

        # Check if the move is diagonal
        if row_diff == col_diff:
            # Check if there are no pieces blocking the path
            direction = (int((end[0] - start[0]) / row_diff), int((end[1] - start[1]) / col_diff))
            current_row, current_col = start[0] + direction[0], start[1] + direction[1]

            while (current_row, current_col) != end:
                if self.game.get_piece(current_row, current_col) is not None:
                    return False
                current_row += direction[0]
                current_col += direction[1]

            # If the target square is empty or contains an opponent's piece, the move is valid
            target_piece = self.game.get_piece(*end)
            if target_piece is None or target_piece.color != self.color:
                return True

        return False

    def get_sprite(self):
        x, y = (2, 0) if self.color == 'white' else (2, 1)
        return self.get_piece_sprite(x, y)


class Knight(Piece):
    def is_valid_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])

        # Check if the move is an L-shape (two squares in one direction and one square in the other)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            # If the target square is empty or contains an opponent's piece, the move is valid
            target_piece = self.game.get_piece(*end)
            if target_piece is None or target_piece.color != self.color:
                return True

        return False

    def get_sprite(self):
        x, y = (3, 0) if self.color == 'white' else (3, 1)
        return self.get_piece_sprite(x, y)


class Pawn(Piece):
    def is_valid_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])

        forward = 1 if self.color == "white" else -1

        # Check if the move is a single step forward
        if start[0] + forward == end[0] and start[1] == end[1]:
            # If the target square is empty, the move is valid
            if self.game.get_piece(*end) is None:
                return True

        # Check if the move is a diagonal capture
        if start[0] + forward == end[0] and col_diff == 1:
            # If the target square contains an opponent's piece, the move is valid
            target_piece = self.game.get_piece(*end)
            if target_piece is not None and target_piece.color != self.color:
                return True

        # Implement rules for en passant and pawn promotion as needed

        return False

    def get_sprite(self):
        x, y = (5, 0) if self.color == 'white' else (5, 1)
        return self.get_piece_sprite(x, y)


class Game:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.turn = "white"
        self.pieces = []

    def setup_board(self):
        # Place the white pieces
        self.board[0] = [Rook("white", self), Knight("white", self), Bishop("white", self), Queen("white", self),
                             King("white", self), Bishop("white", self), Knight("white", self), Rook("white", self)]
        self.board[1] = [Pawn("white", self) for _ in range(8)]

# Place the black pieces
        self.board[7] = [Rook("black", self), Knight("black", self), Bishop("black", self), Queen("black", self),
                             King("black", self), Bishop("black", self), Knight("black", self), Rook("black", self)]
        self.board[6] = [Pawn("black", self) for _ in range(8)]
        # Set up the initial board with pieces
        # Replace this code with the actual initial chess setup
        self.board[0][0] = King("white", self)

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def place_piece(self, row, col):
        if not self.board[row][col]:
            self.board[row][col] = King("white", self)
        else:
            self.board[row][col] = None

    def move(self, start, end):
        piece: Optional[Piece] = self.board[start[0]][start[1]]
        if piece is not None and piece.color == self.turn:
            if piece.is_valid_move(start, end,):
                self.board[end[0]][end[1]] = piece
                self.board[start[0]][start[1]] = None
                self.turn = not self.turn
                return True
        return False

    def move_piece(self, start, end):
        row1, col1 = start
        row2, col2 = end
        self.board[row2][col2] = self.board[row1][col1]
        self.board[row1][col1] = None

    def check(self, color):
        # Check if the king of the given color is in check.
        king_pos = self.find_king(color)
        for piece in self.pieces:
            if piece.color != color:
                if king_pos in piece.get_moves(self.board):
                    return True
        return False

    def mate(self, color):
        # Check if the king of the given color is in checkmate.
        if not self.check(color):
            return False
        for piece in self.pieces:
            if piece.color == color:
                for move in piece.get_moves(self.board):
                    # Make the move temporarily to see if the king is still in check
                    temp_board = self.board.copy()
                    temp_board[piece.pos] = None
                    temp_board[move] = piece
                    if not self.check(color):
                        return False
        return True

    def find_king(self, color):
        # Find the position of the king of the given color.
        for piece in self.pieces:
            if isinstance(piece, King) and piece.color == color:
                return piece.pos
        raise ValueError("No king of color {} found in game.".format(color))

if __name__ == "__main__":
    game = Game()
    game.place_piece(0, 0)
