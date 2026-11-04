
import tkinter as tk
from tkinter import messagebox
import random
import json
from pathlib import Path

# ---------- Settings ----------
LEVELS = {
    "Easy (1-50)": {"maximum": 50, "attempts": 10},
    "Medium (1-100)": {"maximum": 100, "attempts": 7},
    "Hard (1-500)": {"maximum": 500, "attempts": 10}
}

BEST_SCORE_FILE = Path(__file__).with_name(
    "number_guessing_best_score.json"
)

BG = "#101827"
PANEL = "#1b2738"
TEXT = "#f4f7fb"
MUTED = "#aab7c8"
BLUE = "#38bdf8"
GREEN = "#34d399"
ORANGE = "#fbbf24"
RED = "#fb7185"


def load_best_score():
    try:
        data = json.loads(BEST_SCORE_FILE.read_text(encoding="utf-8"))
        return max(0, int(data.get("best_score", 0)))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def save_best_score(score):
    try:
        BEST_SCORE_FILE.write_text(
            json.dumps({"best_score": score}, indent=4),
            encoding="utf-8"
        )
        return True
    except OSError:
        return False


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("540x620")
        self.root.minsize(500, 580)
        self.root.configure(bg=BG)

        self.level_var = tk.StringVar(value="Medium (1-100)")
        self.guess_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.range_var = tk.StringVar()
        self.attempts_var = tk.StringVar()
        self.score_var = tk.StringVar()
        self.best_var = tk.StringVar()

        self.best_score = load_best_score()
        self.build_ui()
        self.new_game()

    def build_ui(self):
        tk.Label(
            self.root,
            text="NUMBER GUESSING GAME",
            font=("Segoe UI", 19, "bold"),
            bg=BG, fg=BLUE
        ).pack(pady=(20, 4))

        tk.Label(
            self.root,
            text="Guess the hidden number!",
            font=("Segoe UI", 11),
            bg=BG, fg=MUTED
        ).pack(pady=(0, 16))

        panel = tk.Frame(self.root, bg=PANEL, padx=24, pady=20)
        panel.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        tk.Label(
            panel, text="Choose difficulty",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL, fg=TEXT
        ).pack(anchor="w")

        self.level_menu = tk.OptionMenu(
            panel, self.level_var, *LEVELS.keys(),
            command=self.on_level_change
        )
        self.level_menu.config(
            font=("Segoe UI", 10),
            bg="#26364b", fg=TEXT,
            activebackground="#344963",
            activeforeground=TEXT,
            relief="flat", highlightthickness=0
        )
        self.level_menu["menu"].config(
            bg="#26364b", fg=TEXT,
            activebackground=BLUE
        )
        self.level_menu.pack(fill="x", pady=(6, 16))

        tk.Label(
            panel, textvariable=self.range_var,
            font=("Segoe UI", 11),
            bg=PANEL, fg=MUTED
        ).pack(pady=(0, 12))

        tk.Label(
            panel, text="Enter your guess",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL, fg=TEXT
        ).pack(anchor="w")

        self.guess_entry = tk.Entry(
            panel, textvariable=self.guess_var,
            font=("Segoe UI", 18), justify="center",
            bg="#f4f7fb", fg="#101827",
            relief="flat"
        )
        self.guess_entry.pack(fill="x", ipady=8, pady=(7, 12))
        self.guess_entry.bind(
            "<Return>", lambda event: self.check_guess()
        )

        buttons = tk.Frame(panel, bg=PANEL)
        buttons.pack(fill="x", pady=(0, 14))

        self.guess_button = tk.Button(
            buttons, text="GUESS",
            command=self.check_guess,
            font=("Segoe UI", 10, "bold"),
            bg=BLUE, fg="#062033",
            activebackground="#7dd3fc",
            relief="flat", cursor="hand2"
        )
        self.guess_button.pack(
            side="left", fill="x", expand=True,
            ipady=8, padx=(0, 5)
        )

        tk.Button(
            buttons, text="PLAY AGAIN",
            command=self.new_game,
            font=("Segoe UI", 10, "bold"),
            bg="#334155", fg=TEXT,
            activebackground="#475569",
            relief="flat", cursor="hand2"
        ).pack(
            side="left", fill="x", expand=True,
            ipady=8, padx=(5, 0)
        )

        self.status_label = tk.Label(
            panel, textvariable=self.status_var,
            wraplength=420,
            font=("Segoe UI", 12, "bold"),
            bg=PANEL, fg=TEXT
        )
        self.status_label.pack(pady=(4, 12))

        stats = tk.Frame(panel, bg=PANEL)
        stats.pack(fill="x", pady=(4, 0))

        tk.Label(
            stats, textvariable=self.attempts_var,
            font=("Segoe UI", 10),
            bg=PANEL, fg=TEXT
        ).pack(side="left")

        tk.Label(
            stats, textvariable=self.score_var,
            font=("Segoe UI", 10, "bold"),
            bg=PANEL, fg=GREEN
        ).pack(side="right")

        tk.Label(
            panel, textvariable=self.best_var,
            font=("Segoe UI", 10),
            bg=PANEL, fg=ORANGE
        ).pack(pady=(12, 0))

        tk.Label(
            self.root, text="Built with Python + Tkinter",
            font=("Segoe UI", 9),
            bg=BG, fg=MUTED
        ).pack(pady=(0, 10))

    def new_game(self):
        settings = LEVELS[self.level_var.get()]
        self.maximum = settings["maximum"]
        self.max_attempts = settings["attempts"]

        self.secret_number = random.randint(1, self.maximum)
        self.attempts_used = 0
        self.score = 0
        self.game_over = False

        self.guess_var.set("")
        self.status_var.set(
            "Game started! Enter a number and press GUESS."
        )
        self.status_label.config(fg=TEXT)

        self.guess_entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.update_labels()
        self.guess_entry.focus_set()

    def on_level_change(self, selected_level):
        self.new_game()

    def update_labels(self):
        self.range_var.set(
            f"Guess a whole number from 1 to {self.maximum}"
        )
        self.attempts_var.set(
            f"Attempts: {self.attempts_used}/{self.max_attempts}"
        )
        self.score_var.set(f"Score: {self.score}")
        self.best_var.set(f"Best score: {self.best_score}")

    def finish_game(self):
        self.game_over = True
        self.guess_entry.config(state="disabled")
        self.guess_button.config(state="disabled")

    def check_guess(self):
        if self.game_over:
            return

        raw_guess = self.guess_var.get().strip()

        # Validate whole number
        try:
            guess = int(raw_guess)
        except ValueError:
            messagebox.showwarning(
                "Invalid input",
                "Please enter a whole number, such as 25."
            )
            self.guess_entry.focus_set()
            return

        # Validate selected range
        if not 1 <= guess <= self.maximum:
            messagebox.showwarning(
                "Out of range",
                f"Please enter a number from 1 to {self.maximum}."
            )
            self.guess_entry.focus_set()
            return

        self.attempts_used += 1

        if guess < self.secret_number:
            self.status_var.set("Too low! Try a higher number.")
            self.status_label.config(fg=ORANGE)

        elif guess > self.secret_number:
            self.status_var.set("Too high! Try a lower number.")
            self.status_label.config(fg=ORANGE)

        else:
            self.score = max(
                10,
                (self.max_attempts - self.attempts_used + 1) * 10
            )

            self.status_var.set(
                f"Correct! The number was {self.secret_number}. "
                f"You won in {self.attempts_used} attempt(s)!"
            )
            self.status_label.config(fg=GREEN)

            if self.score > self.best_score:
                self.best_score = self.score
                if not save_best_score(self.best_score):
                    messagebox.showwarning(
                        "Save warning",
                        "Best score could not be saved to a file."
                    )

            self.update_labels()
            self.finish_game()

            messagebox.showinfo(
                "You won!",
                f"Great job! You scored {self.score} points."
            )
            return

        # Check whether attempts are exhausted
        if self.attempts_used >= self.max_attempts:
            self.status_var.set(
                f"No attempts left! The number was {self.secret_number}."
            )
            self.status_label.config(fg=RED)
            self.finish_game()
        else:
            self.guess_var.set("")
            self.guess_entry.focus_set()

        self.update_labels()


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
