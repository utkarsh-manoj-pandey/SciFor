import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        
        # Styling
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12))
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TCombobox', font=('Helvetica', 12))
        
        # Header
        header_label = ttk.Label(root, text="BMI Calculator", font=("Helvetica", 20))
        header_label.pack(pady=10)
        
        # Profile Frame
        self.profile_frame = tk.Frame(root)
        self.profile_frame.pack(padx=20, pady=10, fill='both')
        
        self.user_profiles = {}
        self.current_user = tk.StringVar()
        
        # User Profile Label
        profile_label = ttk.Label(self.profile_frame, text="User Profile:")
        profile_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        # User Profile Combobox
        self.profile_combobox = ttk.Combobox(self.profile_frame, textvariable=self.current_user, state='readonly')
        self.profile_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.profile_combobox.bind("<<ComboboxSelected>>", self.load_user_profile)
        self.update_profile_combobox()
        
        # Create Profile Button
        create_profile_button = ttk.Button(self.profile_frame, text="Create Profile", command=self.create_profile)
        create_profile_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Container
        self.container = tk.Frame(root, bd=5, relief=tk.GROOVE)
        self.container.pack(padx=20, pady=(0, 20), fill=tk.BOTH, expand=True)
        
        # Height
        height_label = ttk.Label(self.container, text="Height (cm):")
        height_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.height_entry = ttk.Entry(self.container)
        self.height_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Weight
        weight_label = ttk.Label(self.container, text="Weight (kg):")
        weight_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.weight_entry = ttk.Entry(self.container)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Units
        self.unit_var = tk.StringVar()
        units_label = ttk.Label(self.container, text="Units:")
        units_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        
        self.units_combobox = ttk.Combobox(self.container, textvariable=self.unit_var, values=["Metric", "Imperial"], state='readonly')
        self.units_combobox.current(0)
        self.units_combobox.grid(row=2, column=1, padx=10, pady=10)
        
        # Calculate Button
        calculate_button = ttk.Button(self.container, text="Calculate BMI", command=self.calculate_bmi)
        calculate_button.grid(row=3, columnspan=2, padx=10, pady=10)
        
        # BMI Result Label
        bmi_label = ttk.Label(self.container, text="BMI:")
        bmi_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        
        self.bmi_result_label = ttk.Label(self.container, text="")
        self.bmi_result_label.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        
        # Save Button
        save_button = ttk.Button(self.container, text="Save Record", command=self.save_record)
        save_button.grid(row=5, columnspan=2, padx=10, pady=10)
        
        # Export Button
        export_button = ttk.Button(self.container, text="Export Data", command=self.export_data)
        export_button.grid(row=6, columnspan=2, padx=10, pady=10)
        
        # Graph Frame
        graph_frame = tk.Frame(root)
        graph_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('BMI')
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_profile_combobox(self):
        profiles = list(self.user_profiles.keys())
        self.profile_combobox['values'] = profiles
    
    def create_profile(self):
        profile_name = simpledialog.askstring("Create Profile", "Enter Profile Name:")
        if profile_name:
            self.user_profiles[profile_name] = {"height": 0, "weight": 0, "unit": "Metric"}
            self.update_profile_combobox()
            self.current_user.set(profile_name)
            messagebox.showinfo("Profile Created", f"Profile '{profile_name}' created successfully!")
    
    def load_user_profile(self, event):
        selected_profile = self.current_user.get()
        if selected_profile in self.user_profiles:
            profile_data = self.user_profiles[selected_profile]
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(profile_data["height"]))
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, str(profile_data["weight"]))
            self.unit_var.set(profile_data["unit"])
    
    def calculate_bmi(self):
        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            units = self.unit_var.get()
            
            if height == 0 or weight == 0:
                messagebox.showerror("Error", "Please enter valid height and weight.")
                return
            
            if units == "Imperial":
                height *= 0.393701  # convert cm to inches
                weight *= 0.453592  # convert kg to pounds
            
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            
            self.bmi_result_label.config(text=f"BMI: {round(bmi, 2)}")
            
            # BMI Status
            if bmi < 18.5:
                status = "Underweight"
                color = "red"
            elif bmi >= 18.5 and bmi < 24.9:
                status = "Normal"
                color = "green"
            else:
                status = "Overweight"
                color = "red"
            
            messagebox.showinfo("BMI Status", status)
            self.bmi_result_label.configure(foreground=color)
            
            # Update Graph
            self.ax.plot(date.today(), bmi, 'bo')
            self.ax.plot(date.today(), bmi, 'b-')
            self.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for height and weight.")
    
    def save_record(self):
        try:
            selected_profile = self.current_user.get()
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            units = self.unit_var.get()
            
            if selected_profile in self.user_profiles:
                self.user_profiles[selected_profile] = {"height": height, "weight": weight, "unit": units}
                messagebox.showinfo("Record Saved", "BMI record saved successfully!")
            else:
                messagebox.showerror("Error", "Please select a valid user profile.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for height and weight.")

    def export_data(self):
        try:
            selected_profile = self.current_user.get()
            if selected_profile in self.user_profiles:
                profile_data = self.user_profiles[selected_profile]
                file_name = f"{selected_profile}_bmi_data.csv"
                with open(file_name, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Date", "Height (cm)", "Weight (kg)", "BMI", "Units"])
                    writer.writerow([date.today(), profile_data["height"], profile_data["weight"], self.bmi_result_label.cget('text').split(":")[1].strip(), profile_data["unit"]])
                messagebox.showinfo("Data Exported", f"BMI data exported to {file_name} successfully!")
            else:
                messagebox.showerror("Error", "Please select a valid user profile.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()