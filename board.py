import tkinter as tk
from PIL import Image, ImageTk


class Board(tk.Frame):

    rows = 8
    columns = 8
    light_color = "#FFDEAD"
    dark_color = "#CD853F"
    icon_path = {
        "k": "img/black_king.png",
        "q": "img/black_queen.png",
        "r": "img/black_rook.png",
        "n": "img/black_knight.png",
        "b": "img/black_bishop.png",
        "p": "img/black_pawn.png",
        "K": "img/white_king.png",
        "Q": "img/white_queen.png",
        "R": "img/white_rook.png",
        "N": "img/white_knight.png",
        "B": "img/white_bishop.png",
        "P": "img/white_pawn.png"
    }


    def __init__(self, master, chess, square_length=64):
        super().__init__(master)
        self.chess = chess
        self.square_length = square_length
        self.selected = None
        self.highlighted = [
            [False for _ in range(self.columns)] for _ in range(self.rows)
        ]

        # create canvas
        canvas_width = self.columns * square_length
        canvas_height = self.rows * square_length
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        # create icons
        light_bg = Image.new("RGBA", (100, 100), self.light_color)
        dark_bg = Image.new("RGBA", (100, 100), self.dark_color)
        highlight_bg = Image.new("RGBA", (100, 100), "yellow")
        self.icons = {}
        for key, path in self.icon_path.items():
            img = Image.open(path)
            light_img = Image.alpha_composite(light_bg, img)
            light_img = light_img.resize((32, 32)).convert("RGB")
            self.icons[self.light_color + key] = ImageTk.PhotoImage(light_img)
            dark_img = Image.alpha_composite(dark_bg, img)
            dark_img = dark_img.resize((32, 32)).convert("RGB")
            self.icons[self.dark_color + key] = ImageTk.PhotoImage(dark_img)
            highlight_img = Image.alpha_composite(highlight_bg, img)
            highlight_img = highlight_img.resize((32, 32)).convert("RGB")
            self.icons["yellow" + key] = ImageTk.PhotoImage(highlight_img)

    def refresh(self, event=None):
        """
        redraw board
        """

        if event:
            xsize = int((event.width - 1) / self.columns)
            ysize = int((event.height - 1) / self.rows)
            self.square_length = min(xsize, ysize)

        # delete the previous images
        self.canvas.delete("square")
        self.canvas.delete("piece")

        # draw board
        # the color of the top left square is light
        color = self.light_color
        for row in range(self.rows):
            # exchange square color
            color = self.light_color if color == self.dark_color else self.dark_color
            for col in range(self.columns):
                # exchange square color
                color = self.light_color if color == self.dark_color else self.dark_color

                # define coordinates of top left and bottom right of a square
                x1 = col * self.square_length
                x2 = x1 + self.square_length
                y1 = row * self.square_length
                y2 = y1 + self.square_length

                # draw a light or dark square
                if self.highlighted[row][col]:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="black", fill="yellow", tags="square"
                    )
                    filled_color = "yellow"
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="black", fill=color, tags="square"
                    )
                    filled_color = color

                # draw a piece
                piece = self.chess._position[row][col]
                if piece is not None:
                    self.canvas.create_image(
                        ((x1 + x2) // 2, (y1 + y2) // 2),
                        image=self.icons[filled_color + piece],
                        tags=(piece, "piece")
                    )

    def click(self, event):
        # selected square
        col = event.x // self.square_length
        row = event.y // self.square_length
        if self.selected is not None:
            self.move(self.selected, (row, col))
        if (row, col) == self.selected:
            self.selected = None
            self.highlighted[row][col] = False
        else:
            self.selected = (row, col)
            self.highlighted = [
                [False for _ in range(self.columns)] for _ in range(self.rows)
            ]
            self.highlighted[row][col] = True

        self.refresh()

    def move(self, origin, destination):
        piece_origin = self.chess._position[origin[0]][origin[1]]
        if piece_origin is not None:
            self.chess._position[destination[0]][destination[1]] = piece_origin
            self.chess._position[origin[0]][origin[1]] = None
