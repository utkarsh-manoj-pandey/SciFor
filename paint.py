import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

class Shape:
    def __init__(self, shape_id, shape_type, start_x, start_y, end_x, end_y, color):
        self.shape_id = shape_id
        self.shape_type = shape_type
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color

class PaintApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Paint")
        self.master.geometry("800x600")
        
        self.shapes = []
        self.current_shape = None
        self.pen_color = "black"
        self.pen_size = 3
        self.tool = "pen"
        self.start_x = None
        self.start_y = None
        self.selected_shape = None
        self.drag_start_x = None
        self.drag_start_y = None
        
        self.create_widgets()
        
    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.controls_frame = ttk.Frame(self.master)
        self.controls_frame.pack(pady=10)
        
        style = ttk.Style()
        style.configure('ToolButton.TButton', font=('Helvetica', 10), background='#e0e0e0', foreground='#333333', borderwidth=1)
        
        self.pen_button = ttk.Button(self.controls_frame, text="Pen", style='ToolButton.TButton', command=lambda: self.select_tool("pen"))
        self.pen_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.brush_button = ttk.Button(self.controls_frame, text="Brush", style='ToolButton.TButton', command=lambda: self.select_tool("brush"))
        self.brush_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.color_button = ttk.Button(self.controls_frame, text="Color", style='ToolButton.TButton', command=self.choose_color)
        self.color_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.eraser_button = ttk.Button(self.controls_frame, text="Eraser", style='ToolButton.TButton', command=lambda: self.select_tool("eraser"))
        self.eraser_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.size_label = ttk.Label(self.controls_frame, text="Size:", font=("Helvetica", 12))
        self.size_label.grid(row=0, column=4, padx=5, pady=5)
        
        self.size_scale = ttk.Scale(self.controls_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_size, length=150)
        self.size_scale.grid(row=0, column=5, padx=5, pady=5)
        
        self.size_scale.set(self.pen_size)
        
        self.clear_button = ttk.Button(self.controls_frame, text="Clear", style='ToolButton.TButton', command=self.clear_canvas)
        self.clear_button.grid(row=0, column=6, padx=5, pady=5)
        
        self.shapes_frame = ttk.LabelFrame(self.controls_frame, text="Shapes")
        self.shapes_frame.grid(row=0, column=7, padx=5, pady=5)
        
        self.line_button = ttk.Button(self.shapes_frame, text="Line", style='ToolButton.TButton', command=lambda: self.select_tool("line"))
        self.line_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.rectangle_button = ttk.Button(self.shapes_frame, text="Rectangle", style='ToolButton.TButton', command=lambda: self.select_tool("rectangle"))
        self.rectangle_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.circle_button = ttk.Button(self.shapes_frame, text="Circle", style='ToolButton.TButton', command=lambda: self.select_tool("circle"))
        self.circle_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        self.canvas.bind("<ButtonPress-3>", self.select_shape)
        self.canvas.bind("<B3-Motion>", self.move_shape)
        self.canvas.bind("<ButtonRelease-3>", self.release_shape)
        
    def start_draw(self, event):
        if self.tool in ["line", "rectangle", "circle"]:
            self.start_x = event.x
            self.start_y = event.y
            self.current_shape = self.create_shape(self.tool, self.start_x, self.start_y, self.start_x, self.start_y, self.pen_color)
        elif self.tool == "pen" or self.tool == "brush" or self.tool == "eraser":
            self.paint(event)
        
    def draw(self, event):
        if self.tool in ["line", "rectangle", "circle"] and self.current_shape:
            self.canvas.delete(self.current_shape.shape_id)
            self.current_shape.end_x = event.x
            self.current_shape.end_y = event.y
            if self.tool == "line":
                self.current_shape.shape_id = self.canvas.create_line(self.current_shape.start_x, self.current_shape.start_y, self.current_shape.end_x, self.current_shape.end_y, fill=self.current_shape.color, width=self.pen_size * 2)
            elif self.tool == "rectangle":
                self.current_shape.shape_id = self.canvas.create_rectangle(self.current_shape.start_x, self.current_shape.start_y, self.current_shape.end_x, self.current_shape.end_y, fill=self.current_shape.color, outline="")
            elif self.tool == "circle":
                self.current_shape.shape_id = self.canvas.create_oval(self.current_shape.start_x, self.current_shape.start_y, self.current_shape.end_x, self.current_shape.end_y, fill=self.current_shape.color, outline="")
        elif self.tool == "pen" or self.tool == "brush" or self.tool == "eraser":
            self.paint(event)
        
    def stop_draw(self, event):
        if self.current_shape:
            self.shapes.append(self.current_shape)
            self.current_shape = None
        
    def create_shape(self, shape_type, start_x, start_y, end_x, end_y, color):
        shape_id = None
        if shape_type == "line":
            shape_id = self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.pen_size * 2)
        elif shape_type == "rectangle":
            shape_id = self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline="")
        elif shape_type == "circle":
            shape_id = self.canvas.create_oval(start_x, start_y, end_x, end_y, fill=color, outline="")
        return Shape(shape_id, shape_type, start_x, start_y, end_x, end_y, color)
        
    def select_shape(self, event):
        self.selected_shape = None
        x, y = event.x, event.y
        shapes = self.canvas.find_overlapping(x, y, x, y)
        if shapes:
            self.selected_shape = shapes[-1]
            self.drag_start_x = x
            self.drag_start_y = y
        
    def move_shape(self, event):
        if self.selected_shape:
            x, y = event.x, event.y
            dx = x - self.drag_start_x
            dy = y - self.drag_start_y
            self.canvas.move(self.selected_shape, dx, dy)
            self.drag_start_x = x
            self.drag_start_y = y
        
    def release_shape(self, event):
        self.selected_shape = None
        
    def select_tool(self, tool):
        self.tool = tool
        
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.pen_color)
        if color[1]:
            self.pen_color = color[1]
        
    def change_size(self, value):
        self.pen_size = int(float(value))
        
    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes = []
        
    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        if self.tool == "pen":
            self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color, width=self.pen_size)
        elif self.tool == "brush":
            self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color, width=self.pen_size * 2)
        elif self.tool == "eraser":
            self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white", width=self.pen_size * 2)

def main():
    root = tk.Tk()
    root.configure(bg="#f0f0f0")
    
    style = ttk.Style()
    style.configure('ToolButton.TButton', font=('Helvetica', 10), background='#f0f0f0', foreground='#333333', borderwidth=1)
    style.configure('TLabel', background='#f0f0f0', foreground='#333333', font=('Helvetica', 12))
    style.configure('Horizontal.TScale', background='#f0f0f0', troughcolor='#cccccc', sliderlength=20)
    
    app = PaintApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()