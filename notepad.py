import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk

class AdvancedNotepadApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Notepad")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab()

        self.create_menu()

    def add_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Untitled")
        
        text_widget = tk.Text(frame, wrap="word")
        text_widget.pack(side="left", expand=True, fill="both")
        
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        
        text_widget.config(yscrollcommand=scrollbar.set)
        
        line_numbers = tk.Text(frame, width=4, padx=4, takefocus=0, border=0, background='lightgrey', state='disabled')
        line_numbers.pack(side="left", fill="y")
        
        text_widget.bind('<KeyPress>', self.update_line_numbers)
        text_widget.bind('<Button-1>', self.update_line_numbers)
        text_widget.bind('<MouseWheel>', self.update_line_numbers)
        
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        text_widget = self.get_current_text_widget()
        line_numbers = self.get_current_line_numbers_widget()
        line_numbers.config(state='normal')
        line_numbers.delete('1.0', 'end')
        line_numbers.insert('1.0', '\n'.join(str(i) for i in range(1, int(text_widget.index('end').split('.')[0]))))
        line_numbers.config(state='disabled')

    def get_current_text_widget(self):
        current_tab_index = self.notebook.index("current")
        frame = self.notebook.winfo_children()[current_tab_index]
        return frame.winfo_children()[0]

    def get_current_line_numbers_widget(self):
        current_tab_index = self.notebook.index("current")
        frame = self.notebook.winfo_children()[current_tab_index]
        return frame.winfo_children()[2]

    def create_menu(self):
        menubar = tk.Menu(self.master)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Tab", command=self.add_tab)
        filemenu.add_command(label="Close Tab", command=self.close_tab)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As", command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=self.cut_text)
        editmenu.add_command(label="Copy", command=self.copy_text)
        editmenu.add_command(label="Paste", command=self.paste_text)
        editmenu.add_separator()
        editmenu.add_command(label="Find", command=self.find_text)
        editmenu.add_command(label="Replace", command=self.replace_text)
        menubar.add_cascade(label="Edit", menu=editmenu)

        formatmenu = tk.Menu(menubar, tearoff=0)
        formatmenu.add_command(label="Font", command=self.choose_font)
        menubar.add_cascade(label="Format", menu=formatmenu)

        toolsmenu = tk.Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="Word Count", command=self.word_count)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)

    def close_tab(self):
        self.notebook.forget(self.notebook.select())

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                text_widget = self.get_current_text_widget()
                text_widget.delete("1.0", tk.END)
                text_widget.insert(tk.END, file.read())

    def save_file(self):
        current_tab = self.notebook.select()
        file_path = self.notebook.tab(current_tab, 'text')
        text_widget = self.get_current_text_widget()
        if file_path == "Untitled":
            self.save_file_as()
        else:
            with open(file_path, "w") as file:
                file.write(text_widget.get("1.0", tk.END))

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.get_current_text_widget().get("1.0", tk.END))

    def cut_text(self):
        self.get_current_text_widget().event_generate("<<Cut>>")

    def copy_text(self):
        self.get_current_text_widget().event_generate("<<Copy>>")

    def paste_text(self):
        self.get_current_text_widget().event_generate("<<Paste>>")

    def find_text(self):
        search_dialog = tk.Toplevel(self.master)
        search_dialog.title("Find")
        
        find_label = tk.Label(search_dialog, text="Find:")
        find_label.pack(side="left")
        
        find_entry = tk.Entry(search_dialog, width=30)
        find_entry.pack(side="left")
        
        def find():
            search_str = find_entry.get()
            text_widget = self.get_current_text_widget()
            start = text_widget.search(search_str, "1.0", tk.END)
            if start:
                end = f"{start}+{len(search_str)}c"
                text_widget.tag_remove("sel", "1.0", tk.END)
                text_widget.tag_add("sel", start, end)
                text_widget.mark_set("insert", end)
                text_widget.see("insert")
            else:
                messagebox.showinfo("Not Found", f"Cannot find '{search_str}'")
        
        find_button = tk.Button(search_dialog, text="Find", command=find)
        find_button.pack(side="left")

    def replace_text(self):
        replace_dialog = tk.Toplevel(self.master)
        replace_dialog.title("Replace")
        
        find_label = tk.Label(replace_dialog, text="Find:")
        find_label.grid(row=0, column=0)
        
        replace_label = tk.Label(replace_dialog, text="Replace with:")
        replace_label.grid(row=1, column=0)
        
        find_entry = tk.Entry(replace_dialog, width=30)
        find_entry.grid(row=0, column=1)
        
        replace_entry = tk.Entry(replace_dialog, width=30)
        replace_entry.grid(row=1, column=1)
        
        def replace():
            find_str = find_entry.get()
            replace_str = replace_entry.get()
            text_widget = self.get_current_text_widget()
            text_widget.replace("1.0", tk.END, text_widget.get("1.0", tk.END).replace(find_str, replace_str))
            replace_dialog.destroy()
        
        replace_button = tk.Button(replace_dialog, text="Replace", command=replace)
        replace_button.grid(row=2, column=1)

    def choose_font(self):
        font_tuple = font.families()
        
        font_dialog = tk.Toplevel(self.master)
        font_dialog.title("Choose Font")
        
        font_label = tk.Label(font_dialog, text="Select Font:")
        font_label.grid(row=0, column=0)
        
        font_var = tk.StringVar()
        font_var.set(font_tuple[0])
        
        font_menu = tk.OptionMenu(font_dialog, font_var, *font_tuple)
        font_menu.grid(row=0, column=1)
        
        def apply_font():
            chosen_font = font_var.get()
            text_widget = self.get_current_text_widget()
            text_widget.config(font=(chosen_font, 12))
            font_dialog.destroy()
        
        apply_button = tk.Button(font_dialog, text="Apply", command=apply_font)
        apply_button.grid(row=1, column=1)

    def word_count(self):
        text_widget = self.get_current_text_widget()
        content = text_widget.get("1.0", tk.END)
        words = content.split()
        num_words = len(words)
        messagebox.showinfo("Word Count", f"Number of Words: {num_words}")

    def about(self):
        messagebox.showinfo("About", "This is a simple notepad application created using Python and Tkinter.")

def main():
    root = tk.Tk()
    app = AdvancedNotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()