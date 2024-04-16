import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")

        # Main Canvas
        self.canvas = tk.Canvas(master, width=400, height=400, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Frame for buttons and labels
        self.control_frame = tk.Frame(master, bg="#34495e", bd=2, relief=tk.RIDGE)
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Start and Restart Buttons
        self.start_button = tk.Button(self.control_frame, text="Start Game", command=self.start_game, bg="#3498db", fg="white", font=("Helvetica", 12))
        self.restart_button = tk.Button(self.control_frame, text="Restart", command=self.restart_game, state=tk.DISABLED, bg="#e74c3c", fg="white", font=("Helvetica", 12))

        # Add padding between buttons
        self.start_button.pack(side=tk.BOTTOM, pady=5, padx=10, ipadx=5)
        self.restart_button.pack(side=tk.BOTTOM, pady=5, padx=10, ipadx=5)

        # Labels
        self.high_score = 0
        self.high_score_label = tk.Label(self.control_frame, text="High Score: 0", fg="white", bg="#34495e", font=("Helvetica", 12))
        self.score_label = tk.Label(self.control_frame, text="Score: 0", fg="white", bg="#34495e", font=("Helvetica", 12))

        # Pack Labels
        self.high_score_label.pack(pady=5)
        self.score_label.pack(pady=5)

        self.snake = [(200, 200), (190, 200), (180, 200)]
        self.food = self.spawn_food()
        self.direction = "Right"
        self.score = 0
        self.game_over_text = None
        self.draw_snake()
        self.draw_food()
        self.master.bind("<Key>", self.change_direction)

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)
        self.score = 0
        self.update_score()
        self.move()

    def restart_game(self):
        self.snake = [(200, 200), (190, 200), (180, 200)]
        self.food = self.spawn_food()
        self.direction = "Right"
        self.score = 0
        self.update_score()
        self.game_over_text = None
        self.canvas.delete("game_over")
        self.draw_snake()
        self.draw_food()
        self.move()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x1, y1 = segment
            x2, y2 = x1 + 10, y1 + 10
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2ecc71", outline="", tags="snake", width=2)

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(x, y, x+10, y+10, fill="#e74c3c", outline="", tags="food")

    def spawn_food(self):
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        return x, y

    def move(self):
        if self.game_over_text:
            return

        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - 10)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 10)
        elif self.direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + 10, head[1])

        self.snake.insert(0, new_head)
        if self.snake[0] == self.food:
            self.score += 10
            self.update_score()
            self.food = self.spawn_food()
            self.draw_food()
        else:
            self.snake.pop()

        self.draw_snake()

        if (new_head[0] < 0 or new_head[0] >= 400 or
                new_head[1] < 0 or new_head[1] >= 400 or
                new_head in self.snake[1:]):
            self.game_over()
        else:
            self.master.after(100, self.move)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            if (event.keysym == "Up" and self.direction != "Down" or
                    event.keysym == "Down" and self.direction != "Up" or
                    event.keysym == "Left" and self.direction != "Right" or
                    event.keysym == "Right" and self.direction != "Left"):
                self.direction = event.keysym

    def game_over(self):
        self.game_over_text = self.canvas.create_text(200, 200, text=f"Game Over\nScore: {self.score}", fill="white", font=("Helvetica", 20), tags="game_over")
        self.start_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    root.resizable(False, False)
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()