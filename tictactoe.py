import tkinter as tk
from tkinter import messagebox
from tkinter import font

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.current_player = "X"

        self.header_label = tk.Label(self.root, text="Tic-Tac-Toe", font=("Arial", 24, "bold"), fg="blue")
        self.header_label.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Player X's Turn", font=("Arial", 16), fg="green")
        self.status_label.pack(pady=10)

        self.create_buttons()

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(
                    frame, text=" ", font=("Arial", 24), height=2, width=5,
                    command=lambda r=row, c=col: self.on_button_click(r, c)
                )
                self.buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Arial", 14), bg="orange", fg="white", command=self.reset_game)
        self.reset_button.pack(pady=10)

    def on_button_click(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, fg="blue" if self.current_player == "X" else "red")

            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif not any(" " in row for row in self.board):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Player {self.current_player}'s Turn", fg="green")

                if self.current_player == "O":
                    self.root.after(500, self.ai_move)

    def ai_move(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]

        for player in ["O", "X"]:
            for row, col in empty_cells:
                self.board[row][col] = player
                if self.check_winner(player):
                    self.board[row][col] = "O"
                    self.buttons[row][col].config(text="O", fg="red")
                    if player == "O":
                        messagebox.showinfo("Game Over", "Player O wins!")
                        self.reset_game()
                    return
                self.board[row][col] = " "

        row, col = empty_cells[0]
        self.board[row][col] = "O"
        self.buttons[row][col].config(text="O", fg="red")

        if self.check_winner("O"):
            messagebox.showinfo("Game Over", "Player O wins!")
            self.reset_game()
        else:
            self.current_player = "X"
            self.status_label.config(text=f"Player {self.current_player}'s Turn", fg="green")

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ")
        self.current_player = "X"
        self.status_label.config(text="Player X's Turn", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()