import tkinter as tk
from PIL import Image, ImageTk
import requests
from tkinter import filedialog
from io import BytesIO

def display_name():
    name = name_entry.get()
    name_label.config(text="My name is: " + name, fg=text_color_var.get(), font=(font_var.get(), 14))

def clear_name():
    name_entry.delete(0, tk.END)
    name_label.config(text="")

def change_background():
    global background_image_label
    # Open file dialog to choose image
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if filename:
        image = Image.open(filename)
        # Resize the image to fit the window
        image = image.resize((800, 600), Image.LANCZOS)
        background_image = ImageTk.PhotoImage(image)
        background_image_label.configure(image=background_image)
        background_image_label.image = background_image

# Create the main window
root = tk.Tk()
root.title("Advanced Name Display App")

# Initialize default text color and font
default_text_color = "black"
default_font = "Arial"

# Download the default background image from the URL
response = requests.get("https://solvid.co.uk/wp-content/uploads/2020/12/Group-251.png")
image_data = response.content

# Convert the image data to an image
image = Image.open(BytesIO(image_data))
# Resize the image to fit the window
image = image.resize((800, 600), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image)

# Create a label to hold the background image
background_image_label = tk.Label(root, image=background_image)
background_image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame with a contrasting background color
frame = tk.Frame(root, bg="#ffffff", bd=5, relief=tk.RIDGE)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Create a label and entry for name input inside the frame
name_label = tk.Label(frame, text="Enter your name:", font=("Arial", 14), bg="#ffffff")
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(frame, font=("Arial", 14))
name_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a button to display the name
display_button = tk.Button(frame, text="Display Name", command=display_name, font=("Arial", 14))
display_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a button to clear the name
clear_button = tk.Button(frame, text="Clear", command=clear_name, font=("Arial", 14))
clear_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Label to display the name
name_display_label = tk.Label(frame, text="", font=("Arial", 14))
name_display_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Button to change background image
change_bg_button = tk.Button(frame, text="Change Background", command=change_background, font=("Arial", 14))
change_bg_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Option to choose text color
text_color_var = tk.StringVar()
text_color_var.set(default_text_color)
text_color_option = tk.OptionMenu(frame, text_color_var, "black", "red", "blue", "green")
text_color_option.config(font=("Arial", 12))
text_color_option.grid(row=5, column=0, padx=10, pady=10)

# Option to choose font style
font_var = tk.StringVar()
font_var.set(default_font)
font_option = tk.OptionMenu(frame, font_var, "Arial", "Times New Roman", "Courier", "Verdana")
font_option.config(font=("Arial", 12))
font_option.grid(row=5, column=1, padx=10, pady=10)

# Run the main event loop
root.mainloop()