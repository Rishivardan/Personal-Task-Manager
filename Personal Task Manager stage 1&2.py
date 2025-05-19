#Author Rishivardan V
#Date 20th March 2025

import os
from datetime import datetime

# File to store task in tasks.txt
TASKS_FILE = "tasks.txt"

# List to store tasks
tasks = []


# Function to create task
def create_task():
    task_name = input("Enter task name: ")
    description = input("Enter task description: ")

    # Priority validation
    priority = ""
    while priority not in ["High", "Medium", "Low"]:
        priority = input("Enter task priority (High/Medium/Low): ").strip().capitalize()

    # Date validation
    while True:
        due_date = input("Enter task due date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")

    task = {"task_name": task_name, "description": description, "priority": priority, "due_date": due_date}
    tasks.append(task)
    save_task()  
    print("Task Created Successfully!")

# Function to view tasks
def view_task():
    if not tasks:
        print("There are no tasks.")
    else:
        print("\nCurrent Tasks:")
        for index, task in enumerate(tasks, start=1):
            print(f"Task No {index}.")
            print(f"  Task Name: {task['task_name']}")
            print(f"  Description: {task['description']}")
            print(f"  Priority: {task['priority']}")
            print(f"  DueDate: {task['due_date']}")
            print("-----")

# Function to update task
def update_task():
    view_task()
    try:
        index = int(input("Enter the task number to update: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["task_name"] = input("Enter new task name (leave empty to keep unchanged): ") or tasks[index]["task_name"]
            tasks[index]["description"] = input("Enter new description (leave empty to keep unchanged): ") or tasks[index]["description"]
            tasks[index]["priority"] = input("Enter new priority (High/Medium/Low), (leave empty to keep unchanged): ") or tasks[index]["priority"]
            tasks[index]["due_date"] = input("Enter new due date (YYYY-MM-DD, leave empty to keep unchanged): ") or tasks[index]["due_date"]
            save_task()  
            print("Task Updated Successfully!")
        else:
            print("Invalid Task Number")
    except ValueError:
        print("Please enter a valid task number.")

# Function to delete a task
def delete_task():
    view_task()
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed_task = tasks.pop(index)
            save_task()  
            print(f"Task '{removed_task['task_name']}' deleted!")
        else:
            print("Invalid Task Number")
    except ValueError:
        print("Please enter a valid task number.")


# Function to load tasks from file
def load_task():
    global tasks
    tasks = []  # Clear the list before loading
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            lines = file.readlines()
            task = {}
            for line in lines:
                line = line.strip()
                if line.startswith("Task Name: "):
                    task["task_name"] = line.replace("Task Name: ", "")
                elif line.startswith("Description: "):
                    task["description"] = line.replace("Description: ", "")
                elif line.startswith("Priority: "):
                    task["priority"] = line.replace("Priority: ", "")
                elif line.startswith("DueDate: "):
                    task["due_date"] = line.replace("DueDate: ", "")
                elif line.startswith("-----"):  
                    tasks.append(task)
                    task = {}  
        print(f"{len(tasks)} tasks loaded from file.")


# Function to save tasks
def save_task():
    with open(TASKS_FILE, "w") as file:
        for index, task in enumerate(tasks, start=1):
            file.write(f"Task No {index}.\n")
            file.write(f"Task Name: {task['task_name']}\n")
            file.write(f"Description: {task['description']}\n")
            file.write(f"Priority: {task['priority']}\n")
            file.write(f"DueDate: {task['due_date']}\n")
            file.write("-----\n")


            

# Main function calls to test CRUD
if __name__ == "__main__":
    load_task()  # Load tasks when the program starts

    while True:
        print("\nTask Manager Menu:")
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            create_task()
        elif choice == "2":
            view_task()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Exiting Task Manager.")
            break
        else:
            print("Invalid Choice! Please enter a number between 1 to 5.")

