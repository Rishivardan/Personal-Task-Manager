import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox

# Task Class
class Task:
    def __init__(self, name, description, priority, due_date):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date
        }

# Task Manager Class
class TaskManager:
    def __init__(self, json_file='tasks.json'):
        self.json_file = json_file
        self.tasks = []
        self.load_tasks_from_json()

    def load_tasks_from_json(self):
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                self.tasks = [Task(**item) for item in data]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks_to_json(self):
        with open(self.json_file, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None):
        filtered = self.tasks
        if name_filter:
            filtered = [t for t in filtered if name_filter.lower() in t.name.lower()]
        if priority_filter:
            filtered = [t for t in filtered if priority_filter.lower() == t.priority.lower()]
        if due_date_filter:
            filtered = [t for t in filtered if due_date_filter in t.due_date]
        return filtered

    def sort_tasks(self, sort_key='name'):
        self.tasks.sort(key=lambda x: getattr(x, sort_key).lower())

    def add_task(self, name, description, priority, due_date):
        new_task = Task(name, description, priority, due_date)
        self.tasks.append(new_task)
        self.save_tasks_to_json()

    def delete_task(self, task_name):
        self.tasks = [task for task in self.tasks if task.name != task_name]
        self.save_tasks_to_json()

# TaskManagerGUI Class
class TaskManagerGUI:
    def __init__(self, root):
        self.task_manager = TaskManager()
        self.root = root
        self.root.title("Personal Task Manager")
        self.setup_gui()
        self.populate_tree(self.task_manager.tasks)

    def setup_gui(self):
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(filter_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(filter_frame, text="Priority:").grid(row=0, column=2)
        self.priority_entry = ttk.Combobox(filter_frame, values=["High", "Medium", "Low"])
        self.priority_entry.grid(row=0, column=3)

        tk.Label(filter_frame, text="Due Date:").grid(row=0, column=4)
        self.due_date_entry = ttk.Entry(filter_frame)
        self.due_date_entry.grid(row=0, column=5)

        filter_btn = ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)
        filter_btn.grid(row=0, column=6, padx=5)

        sort_btn = ttk.Button(filter_frame, text="Sort by Name", command=lambda: self.sort_tasks('name'))
        sort_btn.grid(row=0, column=7, padx=5)

        # Additional input section for adding tasks
        add_frame = ttk.Frame(self.root)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Name:").grid(row=0, column=0)
        self.add_name_entry = ttk.Entry(add_frame)
        self.add_name_entry.grid(row=0, column=1)

        tk.Label(add_frame, text="Description:").grid(row=0, column=2)
        self.add_description_entry = ttk.Entry(add_frame)
        self.add_description_entry.grid(row=0, column=3)

        tk.Label(add_frame, text="Priority:").grid(row=0, column=4)
        self.add_priority_entry = ttk.Combobox(add_frame, values=["High", "Medium", "Low"])
        self.add_priority_entry.grid(row=0, column=5)

        tk.Label(add_frame, text="Due Date:").grid(row=0, column=6)
        self.add_due_date_entry = ttk.Entry(add_frame)
        self.add_due_date_entry.grid(row=0, column=7)

        add_btn = ttk.Button(add_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=0, column=8, padx=5)

        delete_btn = ttk.Button(add_frame, text="Delete Selected Task", command=self.delete_task)
        delete_btn.grid(row=0, column=9, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("Name", "Description", "Priority", "Due Date"), show='headings')
        for col in ("Name", "Description", "Priority", "Due Date"):
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_tasks(c.lower().replace(' ', '_')))
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def populate_tree(self, tasks):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in tasks:
            self.tree.insert('', 'end', values=(task.name, task.description, task.priority, task.due_date))

    def apply_filter(self):
        name = self.name_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()
        filtered_tasks = self.task_manager.get_filtered_tasks(name, priority, due_date)
        self.populate_tree(filtered_tasks)

    def sort_tasks(self, sort_key):
        self.task_manager.sort_tasks(sort_key)
        self.populate_tree(self.task_manager.tasks)

    def add_task(self):
        name = self.add_name_entry.get()
        description = self.add_description_entry.get()
        priority = self.add_priority_entry.get()
        due_date = self.add_due_date_entry.get()
        if name and description and priority and due_date:
            self.task_manager.add_task(name, description, priority, due_date)
            self.populate_tree(self.task_manager.tasks)
        else:
            mbox.showwarning("Missing Information", "Please fill out all fields to add a task.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            task_name = values[0]
            self.task_manager.delete_task(task_name)
            self.populate_tree(self.task_manager.tasks)
        else:
            mbox.showwarning("No selection", "Please select a task to delete.")

# --- Main Program Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
