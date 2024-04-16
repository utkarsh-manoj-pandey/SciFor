import tkinter as tk

class SquareDrawerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Square Drawer")
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()
        
        self.squares = []  # List to store square objects
        self.selected_square = None  # Currently selected square
        self.square_colors = ["red", "green", "blue", "orange"]  # Available colors for squares
        
        # Draw initial squares
        self.draw_square(50, 50, 150, 150, "red")
        self.draw_square(250, 50, 350, 150, "green")
        self.draw_square(50, 250, 150, 350, "blue")
        self.draw_square(250, 250, 350, 350, "orange")
        
        # Bind events
        self.canvas.bind("<Button-1>", self.select_square)
        self.canvas.bind("<B1-Motion>", self.move_square)
        self.canvas.bind("<ButtonRelease-1>", self.release_square)
        self.canvas.bind("<Double-Button-1>", self.change_color)
        self.canvas.bind("<Button-3>", self.delete_square)
        
        # Label to display coordinates and size of the selected square
        self.label = tk.Label(self.master, text="")
        self.label.pack()

    def draw_square(self, x1, y1, x2, y2, color):
        square = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
        self.squares.append(square)
        
    def select_square(self, event):
        x, y = event.x, event.y
        for square in self.squares:
            if self.canvas.coords(square)[0] <= x <= self.canvas.coords(square)[2] and self.canvas.coords(square)[1] <= y <= self.canvas.coords(square)[3]:
                self.selected_square = square
                break
        if self.selected_square:
            self.update_label()

    def move_square(self, event):
        if self.selected_square:
            x, y = event.x, event.y
            self.canvas.coords(self.selected_square, x-50, y-50, x+50, y+50)
            self.update_label()

    def release_square(self, event):
        self.selected_square = None

    def change_color(self, event):
        if self.selected_square:
            color_index = self.square_colors.index(self.canvas.itemcget(self.selected_square, "fill"))
            new_color_index = (color_index + 1) % len(self.square_colors)
            self.canvas.itemconfig(self.selected_square, fill=self.square_colors[new_color_index])
            self.update_label()

    def delete_square(self, event):
        if self.selected_square:
            self.canvas.delete(self.selected_square)
            self.selected_square = None
            self.label.config(text="")

    def update_label(self):
        x1, y1, x2, y2 = self.canvas.coords(self.selected_square)
        width = x2 - x1
        height = y2 - y1
        self.label.config(text=f"Coordinates: ({x1}, {y1}), Size: {width}x{height}")

def main():
    root = tk.Tk()
    app = SquareDrawerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()