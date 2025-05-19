#Author Rishivardan V
#Date 20th March 2025

import os
from datetime import datetime
import json 

# File to store task in json format
TASKS_FILE = "tasks.json"

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
        print("There are no tasks to do.")
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
            task=tasks[index]
            new_taskname=input("Enter new task name (leave empty to keep unchanged): ")
            new_taskdesc=input("Enter new description (leave empty to keep unchanged): ")
            
            
            
            #update only if there any new input 
            if new_taskname:
                task["task_name"]=new_taskname
            if new_taskdesc:
                task["description"]=new_taskdesc
            
            #validation for priority
            new_priority=input("Enter new task priority (High/Medium/Low, leave empty to keep unchanged:").strip().capitalize()
            if new_priority:
                while new_priority not in["High","Medium","Low"]:
                    print("Invalid priority.Enter High, Medium or Low.")
                    new_priority=input("Enter a new priority again: ").strip().capitalize()
                task["priority"]=new_priority
                
            #validation for duedate
                new_duedate=""
                while True:
                    new_duedate=input("Enter a new duedate (YYYY-MM-DD,leave empty or keep unchanged): ").strip()
                    try:
                        datetime.strptime(new_duedate, "%Y-%m-%d")
                        task["due_date"]=new_duedate
                        break
                    except ValueError:
                        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
                        
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
    
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks=json.load(file)
        print(f"{len(tasks)} tasks loaded Successfully.")


# Function to save tasks
def save_task():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks,file,indent=4)
            


            

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


