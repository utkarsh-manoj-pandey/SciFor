import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class EconomicsCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Economics Calculator")
        self.geometry("500x400")

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Label and Entry Frames
        label_frame = ttk.Frame(self)
        label_frame.pack(side=tk.LEFT, padx=10, pady=10)

        input_frame = ttk.Frame(self)
        input_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Labels and Entry Fields
        labels = ["Consumption:", "Investment:", "Government Spending:", "Exports:", "Imports:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(label_frame, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            entry = ttk.Entry(input_frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        # Calculate Button
        self.calculate_button = ttk.Button(self, text="Calculate", command=self.calculate)
        self.calculate_button.pack(side=tk.BOTTOM, pady=10)

        # Plot Button
        self.plot_button = ttk.Button(self, text="Plot", command=self.plot_data)
        self.plot_button.pack(side=tk.BOTTOM, pady=5)

        # Result Display
        self.result_label = ttk.Label(self)
        self.result_label.pack(side=tk.BOTTOM, pady=10)

        # Plot Area
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def calculate(self):
        try:
            consumption = float(self.entries["Consumption:"].get())
            investment = float(self.entries["Investment:"].get())
            govt_spending = float(self.entries["Government Spending:"].get())
            exports = float(self.entries["Exports:"].get())
            imports = float(self.entries["Imports:"].get())

            gdp = consumption + investment + govt_spending + (exports - imports)
            inflation_rate = ((gdp - (consumption + investment + govt_spending)) / (
                    consumption + investment + govt_spending)) * 100
            unemployment_rate = ((govt_spending - exports) / (exports + imports)) * 100

            result_text = f"GDP: {gdp:.2f}\nInflation Rate: {inflation_rate:.2f}%\nUnemployment Rate: {unemployment_rate:.2f}%"
            self.result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only.")

    def plot_data(self):
        try:
            consumption = float(self.entries["Consumption:"].get())
            investment = float(self.entries["Investment:"].get())
            govt_spending = float(self.entries["Government Spending:"].get())
            exports = float(self.entries["Exports:"].get())
            imports = float(self.entries["Imports:"].get())

            labels = ['Consumption', 'Investment', 'Government Spending', 'Exports', 'Imports']
            values = [consumption, investment, govt_spending, exports, imports]

            fig, ax = plt.subplots()
            ax.bar(labels, values, color=['blue', 'green', 'red', 'orange', 'purple'])
            ax.set_ylabel('Amount')
            ax.set_title('Economic Indicators')
            ax.yaxis.grid(True)

            # Clear previous plot
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            # Embedding Matplotlib plot into tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only.")


if __name__ == "__main__":
    app = EconomicsCalculator()
    app.mainloop()
