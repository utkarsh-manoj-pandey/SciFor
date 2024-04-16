import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Todo List App")
        self.master.geometry("500x400")

        self.tasks = []

        self.task_entry = tk.Entry(master, font=('Arial', 14))
        self.task_entry.pack(pady=10, padx=20, fill=tk.X)
        self.task_entry.focus()

        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        self.add_button = tk.Button(button_frame, text="Add Task", command=self.add_task, width=10)
        self.add_button.grid(row=0, column=0, padx=5)

        self.remove_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task, width=12)
        self.remove_button.grid(row=0, column=1, padx=5)

        self.edit_button = tk.Button(button_frame, text="Edit Task", command=self.edit_task, width=10)
        self.edit_button.grid(row=0, column=2, padx=5)

        self.complete_button = tk.Button(button_frame, text="Mark as Completed", command=self.mark_as_completed, width=15)
        self.complete_button.grid(row=0, column=3, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear Completed", command=self.clear_completed, width=12)
        self.clear_button.grid(row=0, column=4, padx=5)

        self.save_button = tk.Button(button_frame, text="Save", command=self.save_tasks, width=10)
        self.save_button.grid(row=0, column=5, padx=5)

        self.load_button = tk.Button(button_frame, text="Load", command=self.load_tasks, width=10)
        self.load_button.grid(row=0, column=6, padx=5)

        self.task_list = tk.Listbox(master, font=('Arial', 12), selectmode=tk.SINGLE, height=15)
        self.task_list.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        search_frame = tk.Frame(master)
        search_frame.pack(pady=5)

        self.search_label = tk.Label(search_frame, text="Search:", font=('Arial', 12))
        self.search_label.grid(row=0, column=0)

        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(search_frame, text="Search", command=self.search_tasks, width=10)
        self.search_button.grid(row=0, column=2, padx=5)

        self.load_tasks()
        self.update_task_list()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            due_date = None
            due_date_input = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
            if due_date_input:
                try:
                    due_date = datetime.strptime(due_date_input, "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showwarning("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
                    return
            self.tasks.append({"task": task, "completed": False, "due_date": due_date})
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            task_index = selected_index[0]
            del self.tasks[task_index]
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def edit_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            task_index = selected_index[0]
            old_task = self.tasks[task_index]["task"]
            new_task = simpledialog.askstring("Edit Task", "Enter new task:", initialvalue=old_task)
            if new_task:
                self.tasks[task_index]["task"] = new_task
                self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    def mark_as_completed(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            task_index = selected_index[0]
            self.tasks[task_index]["completed"] = not self.tasks[task_index]["completed"]
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")

    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.update_task_list()

    def search_tasks(self):
        query = self.search_entry.get().lower()
        if query:
            results = [task for task in self.tasks if query in task["task"].lower()]
            if results:
                result_list = "\n".join(task["task"] for task in results)
                messagebox.showinfo("Search Results", result_list)
            else:
                messagebox.showinfo("No Results", "No matching tasks found.")
        else:
            messagebox.showwarning("Empty Query", "Please enter a search query.")

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            if task["completed"]:
                self.task_list.insert(tk.END, f"{task['task']} (Completed)")
            else:
                self.task_list.insert(tk.END, task["task"])

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
            self.update_task_list()
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "No configuration file found.")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
