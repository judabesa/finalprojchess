import pygame as pg
import pygame_gui as gui
from game import *
import tkinter as tk
from gamefinal import Game, Color, Piece

class ChessGUI:
    def __init__(self):
        pygame.init()
        Piece.SPRITESHEET = pygame.image.load(Piece.SPRITESHEET)
        self.game = Game()
        Piece.set_game(self.game)
        self.root = tk.Tk()
        self.root.title("Chess")
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.create_buttons()

    def create_buttons(self):
        for row in range(8):
            for col in range(8):
                button = tk.Button(self.board_frame, text="", command=lambda r=row, c=col: self.on_button_click(r, c),
                                   width=10, height=5)
                button.grid(row=row, column=col)
                self.buttons[row][col] = button
        self.update_buttons()

    def update_buttons(self):
        for row in range(8):
            for col in range(8):
                piece = self.game.get(row, col)
                if piece:
                    image = pygame_to_tkinter_image(piece._image)
                    photo = tk.PhotoImage(image)
                    self.buttons[row][col].config(image=photo, text="", compound='c')
                    self.buttons[row][col].image = photo
                else:
                    self.buttons[row][col].config(text="", image=None)

    def on_button_click(self, row, col):
        print(f"Clicked on row {row}, column {col}")
        # Add your game logic here
        self.update_buttons()

    def run(self):
        self.root.mainloop()


def pygame_to_tkinter_image(pygame_image):
    data = pygame.image.tostring(pygame_image, 'RGBA')
    width, height = pygame_image.get_size()
    tkinter_image = tk.PhotoImage(data=data, width=width, height=height, format='RGBA')
    return tkinter_image


if __name__ == "__main__":
    chess_gui = ChessGUI()
    chess_gui.run()