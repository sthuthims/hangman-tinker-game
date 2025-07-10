import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman - Tkinter Edition")
        self.master.geometry("450x400")
        self.master.resizable(False, False)

        self.word = self.get_random_word()
        self.display_word = ["_" for _ in self.word]
        self.guessed_letters = set()
        self.max_tries = 4
        self.remaining_tries = self.max_tries

        # GUI Elements
        self.title_label = tk.Label(master, text="🎮 Hangman Game", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)

        self.word_label = tk.Label(master, text=" ".join(self.display_word), font=("Helvetica", 18))
        self.word_label.pack(pady=10)

        self.info_label = tk.Label(master, text=f"Tries left: {self.remaining_tries}", font=("Helvetica", 14))
        self.info_label.pack(pady=5)

        self.guessed_label = tk.Label(master, text="Guessed Letters: ", font=("Helvetica", 12))
        self.guessed_label.pack(pady=5)

        self.entry = tk.Entry(master, font=("Helvetica", 14), justify='center')
        self.entry.pack(pady=10)

        self.guess_button = tk.Button(master, text="Guess", font=("Helvetica", 12), command=self.check_guess)
        self.guess_button.pack(pady=5)

        self.reset_button = tk.Button(master, text="🔄 Restart Game", font=("Helvetica", 12), command=self.reset_game)
        self.reset_button.pack(pady=10)

    def get_random_word(self):
        with open("words.txt") as f:
            words = f.read().splitlines()
        return random.choice(words).lower()

    def check_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showwarning("Invalid Input", "Please enter a single alphabet.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You've already guessed '{guess}'.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.display_word[i] = guess
            self.word_label.config(text=" ".join(self.display_word))
        else:
            self.remaining_tries -= 1
            self.info_label.config(text=f"Tries left: {self.remaining_tries}")

        self.guessed_label.config(text=f"Guessed Letters: {', '.join(sorted(self.guessed_letters))}")

        self.check_game_over()

    def check_game_over(self):
        if "_" not in self.display_word:
            messagebox.showinfo("🎉 Victory", f"You guessed it! The word was '{self.word}'.")
            self.disable_game()
        elif self.remaining_tries == 0:
            messagebox.showerror("💀 Game Over", f"Out of tries! The word was '{self.word}'.")
            self.disable_game()

    def disable_game(self):
        self.guess_button.config(state="disabled")
        self.entry.config(state="disabled")

    def reset_game(self):
        self.word = self.get_random_word()
        self.display_word = ["_" for _ in self.word]
        self.guessed_letters = set()
        self.remaining_tries = self.max_tries

        self.word_label.config(text=" ".join(self.display_word))
        self.info_label.config(text=f"Tries left: {self.remaining_tries}")
        self.guessed_label.config(text="Guessed Letters: ")
        self.entry.config(state="normal")
        self.guess_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

