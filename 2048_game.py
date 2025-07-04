import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.master.geometry("420x500")
        self.master.bind("<Key>", self.handle_key)

        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0

        self.tiles = []
        self.create_ui()
        self.add_tile()
        self.add_tile()
        self.update_ui()

    def create_ui(self):
        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Helvetica", 20))
        self.score_label.pack(pady=10)

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                tile = tk.Label(self.frame, text="", font=("Helvetica", 32), width=4, height=2, relief="ridge", bg="lightgray")
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def add_tile(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                text = str(value) if value != 0 else ""
                color = "lightblue" if value != 0 else "lightgray"
                self.tiles[i][j].config(text=text, bg=color)

        self.score_label.config(text=f"Score: {self.score}")
        self.master.update_idletasks()

    def handle_key(self, event):
        key = event.keysym
        moved = False

        if key == 'Up':
            self.grid, moved, score = self.move_up()
        elif key == 'Down':
            self.grid, moved, score = self.move_down()
        elif key == 'Left':
            self.grid, moved, score = self.move_left()
        elif key == 'Right':
            self.grid, moved, score = self.move_right()

        self.score += score
        if moved:
            self.add_tile()
            self.update_ui()
            if self.check_game_over():
                self.game_over()

    def compress(self, row):
        """ Shift non-zero values to the left """
        new_row = [num for num in row if num != 0]
        new_row += [0] * (self.grid_size - len(new_row))
        return new_row

    def merge(self, row):
        score = 0
        for i in range(self.grid_size - 1):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                row[i+1] = 0
                score += row[i]
        return row, score

    def move_left(self):
        moved = False
        score = 0
        new_grid = []
        for row in self.grid:
            compressed = self.compress(row)
            merged, row_score = self.merge(compressed)
            compressed = self.compress(merged)
            new_grid.append(compressed)
            if compressed != row:
                moved = True
            score += row_score
        return new_grid, moved, score

    def move_right(self):
        reversed_grid = [row[::-1] for row in self.grid]
        moved_grid, moved, score = self.move_left_base(reversed_grid)
        return [row[::-1] for row in moved_grid], moved, score

    def move_up(self):
        transposed = [list(row) for row in zip(*self.grid)]
        moved_grid, moved, score = self.move_left_base(transposed)
        return [list(row) for row in zip(*moved_grid)], moved, score

    def move_down(self):
        transposed = [list(row) for row in zip(*self.grid)]
        reversed_transposed = [row[::-1] for row in transposed]
        moved_grid, moved, score = self.move_left_base(reversed_transposed)
        final = [row[::-1] for row in moved_grid]
        return [list(row) for row in zip(*final)], moved, score

    def move_left_base(self, grid):
        moved = False
        score = 0
        new_grid = []
        for row in grid:
            compressed = self.compress(row)
            merged, row_score = self.merge(compressed)
            compressed = self.compress(merged)
            new_grid.append(compressed)
            if compressed != row:
                moved = True
            score += row_score
        return new_grid, moved, score

    def check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
        return True

    def game_over(self):
        for row in self.tiles:
            for tile in row:
                tile.config(bg="red")
        self.score_label.config(text=f"Game Over! Final Score: {self.score}")

def main():
    root = tk.Tk()
    Game2048(root)
    root.mainloop()

if __name__ == "__main__":
    main()
