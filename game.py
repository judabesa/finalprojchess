import pygame as pg


class Piece:
    SPRITESHEET = pg.image.load('./images/pieces.png')

    def __init__(self, color):
        self.color = color

    def is_valid_move(self, start, end):
        raise NotImplementedError("This method should be implemented in the subclass")


class King(Piece):
    def is_valid_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])

        if row_diff <= 1 and col_diff <= 1:
            target_piece = self.game.get_piece(*end)
            if target_piece is None or target_piece.color != self.color:
                return True

        return False


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

class Game:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.turn = "white"

        # Set up the initial board with pieces
        # Replace this code with the actual initial chess setup
        self.board[0][0] = King("white")

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def place_piece(self, row, col):
        if not self.board[row][col]:
            self.board[row][col] = King("white")
        else:
            self.board[row][col] = None

    def move(self, start, end):
        if not (0 <= start[0] < 8 and 0 <= start[1] < 8 and 0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        piece = self.get_piece(*start)
        target = self.get_piece(*end)

        if piece and piece.color == self.turn and piece.is_valid_move(start, end):
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            self.turn = "black" if self.turn == "white" else "white"
            return True

        return False


if __name__ == "__main__":
    game = Game()
    game.place_piece(0, 0)
