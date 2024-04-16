import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import winsound

class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        
        # Initialize images
        self.rock_img = Image.open("rock.png")
        self.paper_img = Image.open("paper.png")
        self.scissor_img = Image.open("scissor.png")
        
        self.rock_img = self.rock_img.resize((50, 50))
        self.paper_img = self.paper_img.resize((50, 50))
        self.scissor_img = self.scissor_img.resize((50, 50))
        
        self.rock_img = ImageTk.PhotoImage(self.rock_img)
        self.paper_img = ImageTk.PhotoImage(self.paper_img)
        self.scissor_img = ImageTk.PhotoImage(self.scissor_img)
        
        # Initialize sounds
        self.win_sound = "win.mp3"
        self.loss_sound = "loss.mp3"
        
        # Initialize scoreboard
        self.player_score = 0
        self.player2_score = 0
        
        # Initialize multiplayer
        self.multiplayer_mode = False
        self.player2_choice = None
        
        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        self.player_choice = tk.StringVar()
        self.computer_choice = tk.StringVar()
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both")
        
        # Player Choice Frame
        self.choices_frame = tk.LabelFrame(self.main_frame, text="Player Choices", bg="#e3e3e3", padx=10, pady=10)
        self.choices_frame.pack(pady=10, padx=10)
        
        # Player Choice Buttons
        self.rock_btn = tk.Button(self.choices_frame, image=self.rock_img, command=lambda: self.select_choice("rock"))
        self.rock_btn.grid(row=0, column=0, padx=5)
        self.paper_btn = tk.Button(self.choices_frame, image=self.paper_img, command=lambda: self.select_choice("paper"))
        self.paper_btn.grid(row=0, column=1, padx=5)
        self.scissor_btn = tk.Button(self.choices_frame, image=self.scissor_img, command=lambda: self.select_choice("scissors"))
        self.scissor_btn.grid(row=0, column=2, padx=5)
        
        # Multiplayer Checkbox
        self.multiplayer_var = tk.IntVar()
        self.multiplayer_checkbox = tk.Checkbutton(self.choices_frame, text="Multiplayer Mode", variable=self.multiplayer_var, command=self.toggle_multiplayer)
        self.multiplayer_checkbox.grid(row=1, columnspan=3, pady=(5, 0))
        
        # Computer Choice Frame
        self.computer_frame = tk.LabelFrame(self.main_frame, text="Computer's Choice", bg="#e3e3e3", padx=10, pady=10)
        self.computer_frame.pack(pady=10, padx=10)
        
        # Computer Choice Label
        self.computer_choice_label = tk.Label(self.computer_frame, textvariable=self.computer_choice, font=("Arial", 16), bg="#e3e3e3")
        self.computer_choice_label.pack()
        
        # Play Button
        self.play_btn = tk.Button(self.main_frame, text="Play", command=self.play, font=("Arial", 12), bg="#4caf50", fg="white", padx=10, pady=5)
        self.play_btn.pack(pady=10)
        
        # Score Frame
        self.score_frame = tk.LabelFrame(self.main_frame, text="Scores", bg="#e3e3e3", padx=10, pady=10)
        self.score_frame.pack(pady=10, padx=10)
        
        # Player Score Label
        self.player_score_label = tk.Label(self.score_frame, text="Player 1: 0", font=("Arial", 12), bg="#e3e3e3")
        self.player_score_label.grid(row=0, column=0, padx=5)
        
        # Player 2 Score Label
        self.player2_score_label = tk.Label(self.score_frame, text="Player 2: 0", font=("Arial", 12), bg="#e3e3e3")
        self.player2_score_label.grid(row=0, column=1, padx=5)
        
        # Statistics Frame
        self.stats_frame = tk.LabelFrame(self.main_frame, text="Statistics", bg="#e3e3e3", padx=10, pady=10)
        self.stats_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Statistics Text
        self.stats_text = tk.Text(self.stats_frame, height=5, width=30, font=("Arial", 10))
        self.stats_text.pack(fill="both", expand=True)
        
        # Achievements Frame
        self.achievements_frame = tk.LabelFrame(self.main_frame, text="Achievements", bg="#e3e3e3", padx=10, pady=10)
        self.achievements_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Achievements Text
        self.achievements_text = tk.Text(self.achievements_frame, height=5, width=30, font=("Arial", 10))
        self.achievements_text.pack(fill="both", expand=True)

        # Update initial statistics and achievements display
        self.update_statistics()
        self.update_achievements()
        
    def toggle_multiplayer(self):
        self.multiplayer_mode = bool(self.multiplayer_var.get())
        if self.multiplayer_mode:
            messagebox.showinfo("Multiplayer Mode", "Multiplayer Mode Enabled. Player 1 and Player 2 will take turns.")
        else:
            messagebox.showinfo("Single Player Mode", "Single Player Mode Enabled. You are playing against the computer.")
        
    def select_choice(self, choice):
        if not self.multiplayer_mode:
            self.player_choice.set(choice)
        else:
            self.player2_choice = choice
        
    def play(self):
        if not self.multiplayer_mode:
            player_choice = self.player_choice.get()
        else:
            if self.player2_choice is None:
                messagebox.showwarning("Warning", "Player 2 has not selected a choice!")
                return
            player_choice = self.player2_choice
            
        computer_choice = random.choice(['rock', 'paper', 'scissors'])
        self.computer_choice.set(computer_choice)
        
        # Animate player and computer choices
        self.animate_choices(player_choice, computer_choice)
        
        # Calculate result after animation finishes
        self.root.after(2000, self.calculate_result, player_choice, computer_choice)
        
    def animate_choices(self, player_choice, computer_choice):
        # Animate player choice
        if player_choice == "rock":
            self.rock_btn.config(bg="#ffff99")
        elif player_choice == "paper":
            self.paper_btn.config(bg="#ffff99")
        elif player_choice == "scissors":
            self.scissor_btn.config(bg="#ffff99")
        
        # Animate computer choice
        self.root.after(1000, self.display_computer_choice, computer_choice)
        
    def display_computer_choice(self, computer_choice):
        self.computer_choice_label.config(text=computer_choice.capitalize())
        
    def calculate_result(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            result = "It's a tie!"
        elif (player_choice == 'rock' and computer_choice == 'scissors') or \
             (player_choice == 'scissors' and computer_choice == 'paper') or \
             (player_choice == 'paper' and computer_choice == 'rock'):
            result = "Player 1 wins!"
            self.player_score += 1
            self.play_sound(self.win_sound)
        else:
            if self.multiplayer_mode:
                result = "Player 2 wins!"
                self.player2_score += 1
            else:
                result = "Computer wins!"
            self.play_sound(self.loss_sound)
        
        self.update_statistics()
        self.update_achievements()
        
        messagebox.showinfo("Result", result)
        self.update_scores()
        self.reset_choices()

    def update_scores(self):
        self.player_score_label.config(text=f"Player 1: {self.player_score}")
        if self.multiplayer_mode:
            self.player2_score_label.config(text=f"Player 2: {self.player2_score}")
        
    def reset_choices(self):
        self.rock_btn.config(bg="#f0f0f0")
        self.paper_btn.config(bg="#f0f0f0")
        self.scissor_btn.config(bg="#f0f0f0")
        self.computer_choice_label.config(text="")
        self.player_choice.set("")
        self.player2_choice = None
        
    def play_sound(self, sound):
        winsound.PlaySound(sound, winsound.SND_FILENAME)
        
    def update_statistics(self):
        stats_info = ""
        if not self.multiplayer_mode:
            total_games = self.player_score + self.player2_score
            stats_info += f"Total Games Played: {total_games}\n"
            stats_info += f"Player 1 Wins: {self.player_score}\n"
            stats_info += f"Player 2 Wins: {self.player2_score}\n"
        else:
            total_games = self.player_score
            stats_info += f"Total Games Played: {total_games}\n"
            stats_info += f"Player 1 Wins: {self.player_score}\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, stats_info)
        
    def update_achievements(self):
        achievements_info = "Achievements:\n"
        if not self.multiplayer_mode:
            if self.player_score >= 5:
                achievements_info += "Master of Rock Paper Scissors: Unlocked!\n"
            if self.player_score >= 10:
                achievements_info += "Rock Paper Scissors Guru: Unlocked!\n"
        else:
            if self.player_score >= 5:
                achievements_info += "Player 1 Champion: Unlocked!\n"
            if self.player2_score >= 5:
                achievements_info += "Player 2 Champion: Unlocked!\n"

        self.achievements_text.delete('1.0', tk.END)
        self.achievements_text.insert(tk.END, achievements_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsGUI(root)
    root.mainloop()