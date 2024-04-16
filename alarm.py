from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
import datetime
from threading import Thread
import winsound

def set_alarm():
    set_alarm_time = f"{hour_var.get()}:{minute_var.get()}:{second_var.get()} {am_pm_var.get()}"
    label.config(text=f"Alarm set for: {set_alarm_time}")

    # Start the alarm thread
    t1 = Thread(target=alarm, args=(set_alarm_time,))
    t1.start()

def alarm(set_alarm_time):
    while True:
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        if current_time == set_alarm_time:
            label.config(text="Time's up!", fg="red", font=("Helvetica", 16, "bold"))
            winsound.PlaySound(r"C:\Users\utkar\OneDrive\Desktop\Scifor\beep-04.wav", winsound.SND_FILENAME)

root = Tk()
root.title("Elegant Alarm Clock")
root.geometry("500x400")

# Background Image
bg_image = PhotoImage(file=r"C:\Users\utkar\OneDrive\Desktop\Scifor\clock.gif")
bg_label = Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

frame = Frame(root, padx=20, pady=20, bg="#f2f2f2", bd=5, relief=SOLID, borderwidth=2)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Stylish Font
font_style = ("Arial", 12, "bold")

# Styling for Hour
hour_label = Label(frame, text="Hour:", bg="#5CE1E6", font=font_style)
hour_label.grid(row=0, column=0, padx=10, pady=10)
hour_var = StringVar()
hour_var.set('01')
hour_combobox = Combobox(frame, textvariable=hour_var, values=('01', '02', '03', '04', '05', '06', '07',
                                             '08', '09', '10', '11', '12'), font=font_style)
hour_combobox.grid(row=0, column=1, pady=10)

# Styling for Minute
minute_label = Label(frame, text="Minute:", bg="#5CE1E6", font=font_style)
minute_label.grid(row=0, column=2, padx=10, pady=10)
minute_var = StringVar()
minute_var.set('00')
minute_combobox = Combobox(frame, textvariable=minute_var, values=('00', '01', '02', '03', '04', '05', '06', '07',
                                                 '08', '09', '10', '11', '12', '13', '14', '15',
                                                 '16', '17', '18', '19', '20', '21', '22', '23',
                                                 '24', '25', '26', '27', '28', '29', '30', '31',
                                                 '32', '33', '34', '35', '36', '37', '38', '39',
                                                 '40', '41', '42', '43', '44', '45', '46', '47',
                                                 '48', '49', '50', '51', '52', '53', '54', '55'), font=font_style)
minute_combobox.grid(row=0, column=3, pady=10)

# Styling for Second
second_label = Label(frame, text="Second:", bg="#5CE1E6", font=font_style)
second_label.grid(row=0, column=4, padx=10, pady=10)
second_var = StringVar()
second_var.set('00')
second_combobox = Combobox(frame, textvariable=second_var, values=('00', '01', '02', '03', '04', '05', '06', '07',
                                                 '08', '09', '10', '11', '12', '13', '14', '15',
                                                 '16', '17', '18', '19', '20', '21', '22', '23',
                                                 '24', '25', '26', '27', '28', '29', '30', '31',
                                                 '32', '33', '34', '35', '36', '37', '38', '39',
                                                 '40', '41', '42', '43', '44', '45', '46', '47',
                                                 '48', '49', '50', '51', '52', '53', '54', '55'), font=font_style)
second_combobox.grid(row=0, column=5, pady=10)

# Styling for AM/PM
am_pm_var = StringVar(value="AM")
am_pm_label = Label(frame, text="AM/PM:", bg="#5CE1E6", font=font_style)
am_pm_label.grid(row=0, column=6, padx=10, pady=10)
am_pm_style = ("Arial", 10, "italic", "bold")
am_pm_radiobutton_am = Radiobutton(frame, text="AM", variable=am_pm_var, value="AM", bg="#5CE1E6", font=am_pm_style)
am_pm_radiobutton_pm = Radiobutton(frame, text="PM", variable=am_pm_var, value="PM", bg="#5CE1E6", font=am_pm_style)
am_pm_radiobutton_am.grid(row=0, column=7, pady=10)
am_pm_radiobutton_pm.grid(row=0, column=8, pady=10)


# Styling for AM/PM
am_pm_var = StringVar(value="AM")
am_pm_label = Label(frame, text="AM/PM:", bg="#5CE1E6", font=font_style)
am_pm_label.grid(row=0, column=6, padx=10, pady=10)
am_pm_style = ("Arial", 10, "italic", "bold")
am_pm_radiobutton_am = Radiobutton(frame, text="AM", variable=am_pm_var, value="AM", bg="#5CE1E6", font=font_style)
am_pm_radiobutton_pm = Radiobutton(frame, text="PM", variable=am_pm_var, value="PM", bg="#5CE1E6", font=font_style)
am_pm_radiobutton_am.grid(row=0, column=7, pady=10)
am_pm_radiobutton_pm.grid(row=0, column=8, pady=10)

# Stylish Label
label = Label(root, text="", font=("Helvetica", 14, "italic"))
label.pack()

# Stylish "Set Alarm" Button
set_button = Button(root, text="Set Alarm", command=set_alarm, bg="#133B70", fg="white", font=font_style, padx=20, pady=10, bd=5, relief=RAISED)
set_button.place(relx=0.5, rely=0.8, anchor=CENTER)

root.mainloop()