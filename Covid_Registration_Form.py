import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests

def submit_registration():
    # Collecting form data
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    address = address_text.get("1.0", "end-1c")
    email = email_entry.get()
    contact_no = contact_entry.get()
    country = country_entry.get()
    state = state_entry.get()
    diseases = [disease.get() for disease in disease_vars]

    # Displaying collected data (You can modify this part to store the data in a database)
    print("Name:", name)
    print("Age:", age)
    print("Gender:", gender)
    print("Address:", address)
    print("Email:", email)
    print("Contact No:", contact_no)
    print("Country:", country)
    print("State:", state)
    print("Selected Diseases:", diseases)

# Create main window
root = tk.Tk()
root.title("COVID Vaccine Registration Form")

# Download image from the web
url = "https://www.engineeringforkids.com/wp-content/themes/efk/public/images/contact-form-bg.jpg"  # Replace with the actual image URL
response = requests.get(url, stream=True)

# Convert response content to PhotoImage
bg_image = ImageTk.PhotoImage(Image.open(response.raw))

# Set background image for the main window
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

# Header
header_frame = ttk.Frame(root, padding="20", style="Header.TFrame")
header_frame.pack()

style = ttk.Style()
style.configure("Header.TFrame", background="#2C3E50")  # Header background color

header_label = tk.Label(header_frame, text="COVID Vaccine Registration", font=("Helvetica", 20, "bold"), fg="white", bg="#2C3E50", pady=20)
header_label.pack()

# Container Frame
container_frame = ttk.Frame(root, padding="20", style="Container.TFrame")
container_frame.pack(pady=20, ipadx=10, ipady=10)  # Increase borderwidth by adjusting ipadx and ipady

style.configure("Container.TFrame", background="white", borderwidth=3, relief="solid")  # Container background color

# Body
body_frame = ttk.Frame(container_frame, padding="20")
body_frame.pack()

# Name section
name_label = ttk.Label(body_frame, text="Name of the visitor:", font=("Helvetica", 12, "bold"))
name_label.grid(row=0, column=0, sticky="w", pady=5)

name_entry = ttk.Entry(body_frame, font=("Helvetica", 10))
name_entry.grid(row=0, column=1, pady=5, padx=5)

# Age
age_label = ttk.Label(body_frame, text="Age of the visitor:", font=("Helvetica", 12, "bold"))
age_label.grid(row=1, column=0, sticky="w", pady=5)

age_entry = ttk.Entry(body_frame, font=("Helvetica", 10))
age_entry.grid(row=1, column=1, pady=5, padx=5)

# Gender
gender_label = ttk.Label(body_frame, text="Gender:", font=("Helvetica", 12, "bold"))
gender_label.grid(row=2, column=0, sticky="w", pady=5)

gender_var = tk.StringVar()
gender_choices = ["Male", "Female", "Other"]
for i, choice in enumerate(gender_choices):
    ttk.Radiobutton(body_frame, text=choice, variable=gender_var, value=choice, style="TRadiobutton").grid(row=2, column=i+1, pady=5, padx=5)

# Address
address_label = ttk.Label(body_frame, text="Address:", font=("Helvetica", 12, "bold"))
address_label.grid(row=3, column=0, sticky="w", pady=5)

address_text = tk.Text(body_frame, height=4, width=30, font=("Helvetica", 10))
address_text.grid(row=3, column=1, pady=5, padx=5)

# Email
email_label = ttk.Label(body_frame, text="Email ID:", font=("Helvetica", 12, "bold"))
email_label.grid(row=4, column=0, sticky="w", pady=5)

email_entry = ttk.Entry(body_frame, font=("Helvetica", 10))
email_entry.grid(row=4, column=1, pady=5, padx=5)

# Contact No
contact_label = ttk.Label(body_frame, text="Contact No:", font=("Helvetica", 12, "bold"))
contact_label.grid(row=5, column=0, sticky="w", pady=5)

contact_entry = ttk.Entry(body_frame, font=("Helvetica", 10))
contact_entry.grid(row=5, column=1, pady=5, padx=5)

# Country and State
country_label = ttk.Label(body_frame, text="Country:", font=("Helvetica", 12, "bold"))
country_label.grid(row=6, column=0, sticky="w", pady=5)

country_entry = ttk.Entry(body_frame, font=("Helvetica", 10))
country_entry.grid(row=6, column=1, pady=5, padx=5)

state_label = ttk.Label(body_frame, text="State:", font=("Helvetica", 12, "bold"))
state_label.grid(row=7, column=0, sticky="w", pady=5)

state_entry = ttk.Entry(body_frame, font=("Helvetica", 10))
state_entry.grid(row=7, column=1, pady=5, padx=5)

# Diseases
disease_label = ttk.Label(body_frame, text="Select if you have any of the following diseases:", font=("Helvetica", 12, "bold"))
disease_label.grid(row=8, column=0, pady=5, columnspan=2, sticky="w")

disease_vars = [tk.StringVar() for _ in range(4)]
disease_choices = ["Cold", "Cough", "Fever", "Headache"]
for i, choice in enumerate(disease_choices):
    ttk.Checkbutton(body_frame, text=choice, variable=disease_vars[i], style="TCheckbutton").grid(row=9, column=i, pady=5, padx=5, sticky="w")

# Apply styles
style.configure("TEntry", padding=5, width=20)
style.configure("TRadiobutton", font=("Helvetica", 10))
style.configure("TCheckbutton", font=("Helvetica", 10))


# Submit Button (outside the container)
submit_button = ttk.Button(root, text="Submit Registration", command=submit_registration, style="Submit.TButton")
submit_button.pack(pady=20)

style.configure("Submit.TButton", background="#3498db", foreground="black", font=("Helvetica", 12, "bold"))
style.map("Submit.TButton", background=[("active", "#2980b9")])

# Run the application
root.mainloop()