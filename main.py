import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        self.player_names = ['', '']
        self.current_player_idx = 0
        self.scores = {'X': 0, 'O': 0}
        self.create_widgets()
        self.initialize_game()

    def create_widgets(self):
        self.buttons = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('Arial', 60), width=4, height=2,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=3, column=0, pady=10, padx=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_game)
        self.quit_button.grid(row=3, column=2, pady=10, padx=10)

    def initialize_game(self):
        self.current_player_idx = 0
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.get_player_names()
        self.update_status_bar()

    def get_player_names(self):
        for i in range(2):
            self.player_names[i] = simpledialog.askstring("Player Names", f"Enter name for Player {i + 1} ({'X' if i == 0 else 'O'}):")
            if not self.player_names[i]:
                self.player_names[i] = f"Player {i + 1}"

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.players[self.current_player_idx % 2]
            self.update_buttons_state()

            if self.check_winner(self.players[self.current_player_idx % 2]):
                winner = self.player_names[self.current_player_idx % 2]
                self.scores[self.players[self.current_player_idx % 2]] += 1
                messagebox.showinfo("Game Over", f"Player {winner} ({self.players[self.current_player_idx % 2]}) wins!")
                self.update_status_bar()
                self.restart_game()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.update_status_bar()
                self.restart_game()
            else:
                self.current_player_idx += 1

    def update_buttons_state(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.board[i][j]
                self.buttons[i][j].config(state=tk.DISABLED if self.board[i][j] != ' ' else tk.NORMAL)

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True

        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True

        if all(self.board[i][i] == player for i in range(3)):
            return True

        if all(self.board[i][2 - i] == player for i in range(3)):
            return True

        return False

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    def restart_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.update_buttons_state()
        self.update_status_bar()

    def quit_game(self):
        self.root.destroy()

    def update_status_bar(self):
        self.root.title(f"Tic-Tac-Toe - {self.player_names[0]} (X) vs {self.player_names[1]} (O)")
        self.restart_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)

    def show_final_score(self):
        messagebox.showinfo("Final Score", f"{self.player_names[0]} (X): {self.scores['X']}, {self.player_names[1]} (O): {self.scores['O']}")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

    # After mainloop exits (when user closes the window), show final score
    game.show_final_score()
