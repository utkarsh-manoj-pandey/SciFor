import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import cmath
import math
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, diff, integrate, sympify

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Calculator")
        self.root.geometry("1200x800")
        self.root.tk_setPalette(background='#f0f0f0', foreground='#000000')

        self.result_var = tk.StringVar()
        self.expression_history = []

        # Entry widget to display and input expressions
        self.entry = ttk.Entry(root, textvariable=self.result_var, font=("Arial", 20), justify="right", style='Calc.TEntry')
        self.entry.grid(row=0, column=0, columnspan=8, ipadx=8, ipady=8)

        # Buttons
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("sin", 5, 0), ("cos", 5, 1), ("tan", 5, 2), ("sqrt", 5, 3),
            ("(", 6, 0), (")", 6, 1), ("^", 6, 2), ("log", 6, 3),
            ("π", 7, 0), ("e", 7, 1), ("AC", 7, 2), ("DEL", 7, 3),
            ("history", 8, 0), ("MC", 8, 1), ("MR", 8, 2), ("convert", 8, 3),
            ("sinh", 9, 0), ("cosh", 9, 1), ("tanh", 9, 2), ("exp", 9, 3),
            ("ceil", 10, 0), ("floor", 10, 1), ("fabs", 10, 2), ("degrees", 10, 3),
            ("radians", 11, 0), ("atan", 11, 1), ("asin", 11, 2), ("acos", 11, 3),
            ("history_viewer", 12, 0), ("theme", 12, 1), ("complex", 12, 2),
            ("trig_mode", 12, 3), ("plot", 13, 0), ("clear_plot", 13, 1),
            ("save_plot", 13, 2), ("custom_function", 13, 3), ("console", 14, 0),
            ("diff", 14, 1), ("integrate", 14, 2)
        ]

        for (text, row, column) in buttons:
            button = ttk.Button(root, text=text, command=lambda t=text: self.on_button_click(t), width=10, style='Calc.TButton')
            button.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
            root.grid_columnconfigure(column, weight=1)
            root.grid_rowconfigure(row, weight=1)

        # Configure button equal to expand horizontally
        root.grid_columnconfigure(2, weight=1)

        # Initialize unit registry for conversion
        self.ureg = None
        self.memory = None

        # Scientific mode flags
        self.complex_mode = False
        self.trig_mode_deg = True  # Trigonometric mode: Degrees by default

        # Matplotlib Figure for interactive graph plotting
        self.plot_figure = Figure(figsize=(6, 4), tight_layout=True, facecolor='#f0f0f0')
        self.plot_axes = self.plot_figure.add_subplot(111)
        self.plot_axes.set_title("Graph Plot", color='#000000')
        self.plot_axes.set_facecolor('#ffffff')
        self.plot_axes.grid(color='#d0d0d0')
        self.plot_axes.tick_params(axis='both', colors='#000000')
        self.plot_canvas = FigureCanvasTkAgg(self.plot_figure, master=root)
        self.plot_canvas_widget = self.plot_canvas.get_tk_widget()
        self.plot_canvas_widget.grid(row=1, column=8, rowspan=13, padx=10, pady=10, sticky="nsew")

        # History of plotted graphs
        self.plot_history = []

        # Custom functions for graphing
        self.custom_functions = {}

        # Console
        self.console_text = tk.Text(root, height=5, width=40, wrap="word", font=("Courier New", 12), bg='#f0f0f0')
        self.console_text.grid(row=14, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")

        console_scroll = tk.Scrollbar(root, command=self.console_text.yview)
        console_scroll.grid(row=14, column=8, padx=10, pady=10, sticky="nsew")

        self.console_text['yscrollcommand'] = console_scroll.set
        self.console_text.insert(tk.END, "Welcome to the Console!\nType Python commands here.")

        # Move the "Run console" button, "Integration" button, and "Differentiation" button below the graph plot
        console_button_frame = tk.Frame(root)
        console_button_frame.grid(row=15, column=8, padx=10, pady=10, sticky="nsew")

        run_console_button = tk.Button(console_button_frame, text="Run Console", command=self.open_console, width=10, height=2)
        run_console_button.grid(row=0, column=0, padx=2, pady=2)

        integrate_button = ttk.Button(console_button_frame, text="Integration", command=self.integrate_expression, width=10, style='Calc.TButton')
        integrate_button.grid(row=0, column=1, padx=2, pady=2)

        differentiate_button = ttk.Button(console_button_frame, text="Differentiation", command=self.differentiate_expression, width=10, style='Calc.TButton')
        differentiate_button.grid(row=0, column=2, padx=2, pady=2)


    def set_day_theme(self):
            self.root.tk_setPalette(background='#f0f0f0', foreground='#000000')
            self.entry['style'] = 'Calc.TEntry'
            for child in self.root.winfo_children():
                if isinstance(child, ttk.Button):
                    child['style'] = 'Calc.TButton'
                elif isinstance(child, tk.Text) and child is not self.console_text:
                    child['style'] = 'Calc.TEntry'
            self.console_text.config(bg='#f0f0f0', fg='#000000')
            self.console_text.tag_configure('Calc.TEntry', foreground='#000000')

            # Add this line to set the style for the entry widget in the console_text
            self.console_text.tag_configure('Calc.TEntry', foreground='#000000')

    def set_night_theme(self):
            self.root.tk_setPalette(background='#212121', foreground='#ffffff')
            self.entry['style'] = 'CalcDark.TEntry'
            for child in self.root.winfo_children():
                if isinstance(child, ttk.Button):
                    child['style'] = 'CalcDark.TButton'
                elif isinstance(child, tk.Text) and child is not self.console_text:
                    child['style'] = 'CalcDark.TEntry'
            self.console_text.config(bg='#212121', fg='#ffffff')
            self.console_text.tag_configure('CalcDark.TEntry', foreground='#ffffff')


            # Add this line to set the style for the entry widget in the console_text
            self.console_text.tag_configure('CalcDark.TEntry', foreground='#ffffff')

    def on_button_click(self, value):
        current_text = self.result_var.get()

        if value == "=":
            try:
                result = self.evaluate_expression(current_text)
                self.result_var.set(str(result))
                self.expression_history.append(current_text + " = " + str(result))
                self.update_history_viewer()
            except Exception as e:
                messagebox.showerror("Error", "Invalid expression")

        elif value == "AC":
            self.result_var.set("")
        elif value == "DEL":
            self.result_var.set(current_text[:-1])
        elif value == "π":
            self.result_var.set(current_text + str(math.pi))
        elif value == "e":
            self.result_var.set(current_text + str(math.e))
        elif value == "sqrt":
            self.result_var.set(current_text + "np.sqrt(")
        elif value == "log":
            self.result_var.set(current_text + "np.log(")
        elif value == "sin":
            self.result_var.set(current_text + "np.sin(")
        elif value == "cos":
            self.result_var.set(current_text + "np.cos(")
        elif value == "tan":
            self.result_var.set(current_text + "np.tan(")
        elif value == "^":
            self.result_var.set(current_text + "^")
        elif value == "history":
            self.show_history()
        elif value == "MC":
            self.memory = None
        elif value == "MR":
            if self.memory is not None:
                self.result_var.set(current_text + str(self.memory))
        elif value == "convert":
            self.unit_conversion()
        elif value == "sinh":
            self.result_var.set(current_text + "np.sinh(")
        elif value == "cosh":
            self.result_var.set(current_text + "np.cosh(")
        elif value == "tanh":
            self.result_var.set(current_text + "np.tanh(")
        elif value == "exp":
            self.result_var.set(current_text + "np.exp(")
        elif value == "ceil":
            self.result_var.set(current_text + "np.ceil(")
        elif value == "floor":
            self.result_var.set(current_text + "np.floor(")
        elif value == "fabs":
            self.result_var.set(current_text + "np.fabs(")
        elif value == "degrees":
            self.result_var.set(current_text + "np.degrees(")
        elif value == "radians":
            self.result_var.set(current_text + "np.radians(")
        elif value == "atan":
            self.result_var.set(current_text + "np.arctan(")
        elif value == "asin":
            self.result_var.set(current_text + "np.arcsin(")
        elif value == "acos":
            self.result_var.set(current_text + "np.arccos(")
        elif value == "history_viewer":
            self.show_history_viewer()
        elif value == "theme":
            self.toggle_day_night_theme()
        elif value == "complex":
            self.toggle_complex_mode()
        elif value == "trig_mode":
            self.toggle_trig_mode()
        elif value == "plot":
            self.plot_graph()
        elif value == "clear_plot":
            self.clear_graph()
        elif value == "save_plot":
            self.save_plot()
        elif value == "custom_function":
            self.define_custom_function()
        elif value == "console":
            self.open_console()
        elif value == "diff":
            self.differentiate_expression()
        elif value == "integrate":
            self.integrate_expression()
        else:
            self.result_var.set(current_text + value)

    def evaluate_expression(self, expression):
        expression = expression.replace("sqrt", "np.sqrt")
        expression = expression.replace("log", "np.log")
        expression = expression.replace("sin", "np.sin")
        expression = expression.replace("cos", "np.cos")
        expression = expression.replace("tan", "np.tan")
        expression = expression.replace("^", "**")
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))

        if self.complex_mode:
            result = eval(expression)
        else:
            result = eval(expression).real

        return result

    def differentiate_expression(self):
        current_text = self.result_var.get()
        try:
            x = symbols('x')
            expression = sympify(current_text)
            derivative = diff(expression, x)
            self.result_var.set(str(derivative))
        except Exception as e:
            messagebox.showerror("Error", "Invalid expression for differentiation")

    def integrate_expression(self):
        current_text = self.result_var.get()
        try:
            x = symbols('x')
            expression = sympify(current_text)
            integral = integrate(expression, x)
            self.result_var.set(str(integral))
        except Exception as e:
            messagebox.showerror("Error", "Invalid expression for integration")

    def show_history(self):
        history_text = "\n".join(self.expression_history)
        messagebox.showinfo("History", history_text)

    def update_history_viewer(self):
        self.plot_axes.clear()
        self.plot_axes.set_title("Graph Plot")
        self.plot_canvas.draw()

    def show_history_viewer(self):
        self.update_history_viewer()
        self.root.deiconify()

    def unit_conversion(self):
        current_text = self.result_var.get()
        try:
            converted_value = self.ureg(current_text)
            converted_value = converted_value.to_base_units().magnitude
            self.result_var.set(str(converted_value))
        except Exception as e:
            messagebox.showerror("Error", "Invalid unit conversion")

    def toggle_day_night_theme(self):
        current_theme = self.root.tk_getPalette()
        if current_theme == 'light':
            self.set_night_theme()
        else:
            self.set_day_theme()

    def set_day_theme(self):
        self.root.tk_setPalette(background='#f0f0f0', foreground='#000000')
        self.entry['style'] = 'Calc.TEntry'
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Button):
                child['style'] = 'Calc.TButton'
        self.console_text.config(bg='#f0f0f0', fg='#000000')

    def set_night_theme(self):
        self.root.tk_setPalette(background='#212121', foreground='#ffffff')
        self.entry['style'] = 'CalcDark.TEntry'
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Button):
                child['style'] = 'CalcDark.TButton'
        self.console_text.config(bg='#212121', fg='#ffffff')

    def toggle_complex_mode(self):
        self.complex_mode = not self.complex_mode
        messagebox.showinfo("Complex Mode", f"Complex Mode {'Enabled' if self.complex_mode else 'Disabled'}")

    def toggle_trig_mode(self):
        self.trig_mode_deg = not self.trig_mode_deg
        messagebox.showinfo("Trigonometric Mode", f"Trigonometric Mode {'Degrees' if self.trig_mode_deg else 'Radians'}")

    def plot_graph(self):
        try:
            expression = self.result_var.get()
            x_values = np.linspace(-10, 10, 1000)
            y_values = np.array([eval(expression.replace("x", str(x))) for x in x_values])

            self.plot_axes.clear()
            self.plot_axes.plot(x_values, y_values, color='#1f77b4', linewidth=2)
            self.plot_axes.set_title("Graph Plot", color='#000000')
            self.plot_axes.set_facecolor('#ffffff')
            self.plot_axes.grid(color='#d0d0d0')
            self.plot_axes.tick_params(axis='both', colors='#000000')
            self.plot_canvas.draw()

            # Add the graph to the plot history
            self.plot_history.append((expression, x_values, y_values))
        except Exception as e:
            messagebox.showerror("Error", "Invalid expression for plotting")

    def clear_graph(self):
        self.plot_axes.clear()
        self.plot_axes.set_title("Graph Plot", color='#000000')
        self.plot_axes.set_facecolor('#ffffff')
        self.plot_axes.grid(color='#d0d0d0')
        self.plot_axes.tick_params(axis='both', colors='#000000')
        self.plot_canvas.draw()

    def save_plot(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.plot_canvas.print_png(file_path)
                messagebox.showinfo("Save Plot", f"Plot saved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", "Unable to save the plot")

    def define_custom_function(self):
        try:
            function_name = simpledialog.askstring("Define Custom Function", "Enter function name:")
            if function_name:
                expression = simpledialog.askstring("Define Custom Function", f"Enter expression for {function_name}(x):")
                if expression:
                    self.custom_functions[function_name] = expression
                    messagebox.showinfo("Define Custom Function", f"Custom function {function_name}(x) defined successfully.")
        except Exception as e:
            messagebox.showerror("Error", "Unable to define custom function")

    def open_console(self):
        console_window = tk.Toplevel(self.root)
        console_window.title("Python Console")

        console_text = tk.Text(console_window, height=20, width=60, wrap="word", font=("Courier New", 12))
        console_text.pack()

        def execute_command():
            command = console_text.get("1.0", tk.END)
            try:
                result = eval(command)
                console_text.insert(tk.END, f"\n{result}\n", "output")
            except Exception as e:
                console_text.insert(tk.END, f"\nError: {str(e)}\n", "error")

        execute_button = tk.Button(console_window, text="Execute Command", command=execute_command, width=20, height=2)
        execute_button.pack()

        console_text.tag_configure("output", foreground="green")
        console_text.tag_configure("error", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()

    app = AdvancedCalculator(root)
    root.mainloop()