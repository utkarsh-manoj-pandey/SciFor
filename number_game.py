import tkinter as tk
from tkinter import messagebox
import random
import time
import requests
from PIL import Image, ImageTk
from io import BytesIO

class NumberGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Guessing Game")
        self.master.geometry("400x500")
        self.master.configure(bg="#f5f5f5")

        # Download the background image from the provided URL
        response = requests.get("https://static.vecteezy.com/system/resources/previews/022/208/685/original/guessing-game-with-plastic-containers-and-a-ball-isolated-on-transparent-background-vector.jpg")
        image_data = response.content

        # Open the downloaded image using PIL
        self.background_image = Image.open(BytesIO(image_data))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label to display the background image
        self.background_label = tk.Label(self.master, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame for the main content
        self.frame = tk.Frame(self.master, bg="#ffffff", bd=2, relief=tk.RAISED)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=50)
        
        self.label_title = tk.Label(self.frame, text="Number Guessing Game", font=("Arial", 16, "bold"), bg="#ffffff")
        self.label_title.pack(pady=20)
        
        self.label_name = tk.Label(self.frame, text="Enter your name:", font=("Arial", 12), bg="#ffffff")
        self.label_name.pack()
        
        self.entry_name = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_name.pack(pady=5)
        
        self.label_difficulty = tk.Label(self.frame, text="Choose difficulty level:", font=("Arial", 12), bg="#ffffff")
        self.label_difficulty.pack()
        
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("1")  # Default to Easy
        self.difficulty_choices = [("Easy", "1"), ("Medium", "2"), ("Hard", "3")]
        for text, value in self.difficulty_choices:
            self.radio_difficulty = tk.Radiobutton(self.frame, text=text, variable=self.difficulty_var, value=value, bg="#ffffff", font=("Arial", 12))
            self.radio_difficulty.pack(anchor="w", padx=20)
        
        self.label_range = tk.Label(self.frame, text="Enter the range of numbers (min and max):", font=("Arial", 12), bg="#ffffff")
        self.label_range.pack(pady=(20, 5))
        
        self.min_num_entry = tk.Entry(self.frame, font=("Arial", 12), width=10)
        self.min_num_entry.pack(pady=5)
        
        self.max_num_entry = tk.Entry(self.frame, font=("Arial", 12), width=10)
        self.max_num_entry.pack(pady=5)
        
        self.start_button = tk.Button(self.frame, text="Start Game", command=self.start_game, bg="#4caf50", fg="white", font=("Arial", 12), bd=0, relief=tk.RAISED)
        self.start_button.pack(pady=20, ipadx=10, ipady=5)

    def start_game(self):
        name = self.entry_name.get()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        
        min_num = self.min_num_entry.get()
        max_num = self.max_num_entry.get()
        
        if not min_num.isdigit() or not max_num.isdigit():
            messagebox.showerror("Error", "Please enter valid numbers for the range.")
            return
        
        min_num, max_num = int(min_num), int(max_num)
        
        if min_num >= max_num:
            messagebox.showerror("Error", "Invalid range of numbers. Maximum number must be greater than minimum number.")
            return
        
        difficulty = self.difficulty_var.get()
        if difficulty == '1':
            max_attempts = 8
            difficulty = "Easy"
        elif difficulty == '2':
            max_attempts = 6
            difficulty = "Medium"
        elif difficulty == '3':
            max_attempts = 4
            difficulty = "Hard"
        
        secret_number = random.randint(min_num, max_num)
        
        self.play_game(name, min_num, max_num, max_attempts, difficulty, secret_number)
    
    def play_game(self, name, min_num, max_num, max_attempts, difficulty, secret_number):
        game_window = tk.Toplevel(self.master)
        game_window.title("Game")
        game_window.geometry("300x300")
        game_window.configure(bg="#f5f5f5")
        
        frame = tk.Frame(game_window, bg="#ffffff", bd=2, relief=tk.RAISED)
        frame.pack(expand=True, padx=20, pady=20)
        
        label_instruction = tk.Label(frame, text=f"Welcome, {name}! Guess the number between {min_num} and {max_num}.", bg="#ffffff", font=("Arial", 12))
        label_instruction.pack(padx=10, pady=(20, 10))
        
        label_attempts = tk.Label(frame, text=f"Attempts remaining: {max_attempts}", bg="#ffffff", font=("Arial", 12))
        label_attempts.pack(padx=10, pady=(0, 10))
        
        entry_guess = tk.Entry(frame, font=("Arial", 12), width=10)
        entry_guess.pack(padx=10, pady=10)
        
        button_guess = tk.Button(frame, text="Guess", command=lambda: check_guess(entry_guess.get()), bg="#4caf50", fg="white", font=("Arial", 12), bd=0, relief=tk.RAISED)
        button_guess.pack(padx=10, pady=10)
        
        def check_guess(guess):
            nonlocal max_attempts
            try:
                guess = int(guess)
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a number.")
                return
            
            if guess < min_num or guess > max_num:
                messagebox.showerror("Error", f"Please enter a number between {min_num} and {max_num}.")
                return
            
            max_attempts -= 1
            label_attempts.config(text=f"Attempts remaining: {max_attempts}")
            
            if guess < secret_number:
                messagebox.showinfo("Hint", "Too low! Try again.")
            elif guess > secret_number:
                messagebox.showinfo("Hint", "Too high! Try again.")
            else:
                end_time = time.time()
                elapsed_time = round(end_time - start_time, 2)
                messagebox.showinfo("Congratulations!", f"You've guessed the number {secret_number} correctly in {max_attempts} attempts!\nDifficulty: {difficulty}\nTime taken: {elapsed_time} seconds")
                game_window.destroy()
                return
        
            if max_attempts == 0:
                messagebox.showinfo("Game Over", f"Sorry, {name}, you've run out of attempts! The correct number was {secret_number}.\nBetter luck next time!")
                game_window.destroy()
                return
        
        start_time = time.time()
        
root = tk.Tk()
app = NumberGuessingGame(root)
root.mainloop()