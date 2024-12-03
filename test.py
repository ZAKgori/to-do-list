
import argparse
import json
from datetime import datetime
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Additional colors for priorities and warnings
    HIGH_PRIORITY = '\033[91m'  # Bright red for high priority
    MEDIUM_PRIORITY = '\033[93m'  # Yellow for medium priority
    LOW_PRIORITY = '\033[92m'  # Green for low priority
    
    # Actions
    DELETE_ACTION = '\033[95m'  # Magenta for delete warnings
    EDIT_ACTION = '\033[94m'  # Blue for edit actions
    
    # Neutral or informational
    INFO = '\033[90m'  # Gray for less critical information
    RESET = '\033[0m'  # Alias for ENDC for easier readability

# Main class to handle tasks
class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, due_date=None, priority=None):
        due_date = datetime.strptime(due_date, '%Y-%m-%d').isoformat() if due_date else None
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'completed': False
        }
        self.tasks.append(task)
        print(f"Task '{description}' added.")

    def list_tasks(self, filter_by=None, show_completed=False):
        filtered_tasks = [
            task for task in self.tasks
            if (show_completed or not task['completed']) and 
               (filter_by is None or task.get(filter_by) is not None)
        ]
        if not filtered_tasks:
            print("No tasks found.")
            return

        print("Tasks:")
        for task in filtered_tasks:
            due_date = task['due_date'] if task['due_date'] else "No due date"
            status = "Completed" if task['completed'] else "Pending"
            print(f"ID: {task['id']} | {task['description']} | Due: {due_date} | Priority: {task['priority']} | Status: {status}")

    def mark_completed(self, task_id):
        task = next((task for task in self.tasks if task['id'] == task_id), None)
        if task:
            task['completed'] = True
            print(f"Task '{task['description']}' marked as completed.")
        else:
            print(f"Task with ID {task_id} not found.")

    def edit_task(self, task_id, description=None, due_date=None, priority=None):
        task = next((task for task in self.tasks if task['id'] == task_id), None)
        if task:
            if description:
                task['description'] = description
            if due_date:
                task['due_date'] = datetime.strptime(due_date, '%Y-%m-%d').isoformat()
            if priority:
                task['priority'] = priority
            print(f"Task '{task_id}' updated.")
        else:
            print(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        task = next((task for task in self.tasks if task['id'] == task_id), None)
        if task:
            self.tasks.remove(task)
            print(f"Task '{task['description']}' deleted.")
        else:
            print(f"Task with ID {task_id} not found.")

    def save_tasks(self, file_name='tasks.json'):
        with open(file_name, 'w') as f:
            json.dump(self.tasks, f)
        print("Tasks saved to file.")

    def load_tasks(self, file_name='tasks.json'):
        try:
            with open(file_name, 'r') as f:
                self.tasks = json.load(f)
            print("Tasks loaded from file.")
        except FileNotFoundError:
            self.tasks = []

# Command-Line Interface for To-Do List
def cli():
    todo_list = ToDoList()
    todo_list.load_tasks()

    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Completed")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD) (optional): ")
            due_date = due_date if due_date else None
            priority = input(F"Enter priority ({bcolors.LOW_PRIORITY}low{bcolors.ENDC}, {bcolors.MEDIUM_PRIORITY}medium{bcolors.ENDC}, {bcolors.HIGH_PRIORITY}high{bcolors.ENDC}) {bcolors.INFO}(optional){bcolors.ENDC}: ")
            priority = priority if priority in ['low', 'medium', 'high'] else None
            todo_list.add_task(description, due_date, priority)
            todo_list.save_tasks()

        elif choice == '2':
            show_completed = input(F"Show completed tasks? ({bcolors.OKGREEN}yes{bcolors.ENDC}/{bcolors.FAIL}no{bcolors.ENDC}):: ").strip().lower() == 'yes'
            todo_list.list_tasks(show_completed=show_completed)

        elif choice == '3':
            try:
                show_completed = input(f"Show all tasks? ({bcolors.OKGREEN}yes{bcolors.ENDC}/{bcolors.FAIL}no{bcolors.ENDC}): ").strip().lower() == 'yes'
                todo_list.list_tasks(show_completed=True)
                task_id = int(input("Enter task ID to mark as completed: "))
                todo_list.mark_completed(task_id)
                todo_list.save_tasks()
            except ValueError:
                print(f"{bcolors.WARNING}Invalid ID format. Please enter a number.{bcolors.ENDC}")

        elif choice == '4':
            try:
                show_completed = input(F"Show all tasks? ({bcolors.OKGREEN}yes{bcolors.ENDC}/{bcolors.FAIL}no{bcolors.ENDC}): ").strip().lower() == 'yes'
                todo_list.list_tasks(show_completed=True)
                task_id = int(input("Enter task ID to edit: "))
                description = input("Enter new description (leave blank to keep current): ")
                due_date = input("Enter new due date (YYYY-MM-DD) (leave blank to keep current): ")
                priority = input(f"Enter new priority ({bcolors.LOW_PRIORITY}low{bcolors.ENDC}, {bcolors.MEDIUM_PRIORITY}medium{bcolors.ENDC}, {bcolors.HIGH_PRIORITY}high{bcolors.ENDC}) {bcolors.INFO}(leave blank to keep current){bcolors.ENDC}: ")
                todo_list.edit_task(task_id, description or None, due_date or None, priority or None)
                todo_list.save_tasks()
            except ValueError:
                print(f"{bcolors.WARNING}Invalid ID format. Please enter a number.{bcolors.ENDC}")

        elif choice == '5':
            try:
                show_completed = input(f"Show all tasks? ({bcolors.OKGREEN}yes{bcolors.ENDC}/{bcolors.FAIL}no{bcolors.ENDC}): ").strip().lower() == 'yes'
                todo_list.list_tasks(show_completed=True)
                task_id = int(input(f"{bcolors.DELETE_ACTION}Enter task ID to delete: {bcolors.ENDC}"))
                todo_list.delete_task(task_id)
                todo_list.save_tasks()
            except ValueError:
                print(f"{bcolors.WARNING}Invalid ID format. Please enter a number.{bcolors.ENDC}")

        elif choice == '6':
            print(f"{bcolors.WARNING}Invalid option. Please try again.{bcolors.ENDC}")
            print(f"{bcolors.UNDERLINE}Exiting the application.{bcolors.ENDC}")
            break

        else:
            print(f"{bcolors.WARNING}Invalid option. Please try again.{bcolors.ENDC}")

if __name__ == '__main__':
    cli()

'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Additional colors for priorities and warnings
    HIGH_PRIORITY = '\033[91m'  # Bright red for high priority
    MEDIUM_PRIORITY = '\033[93m'  # Yellow for medium priority
    LOW_PRIORITY = '\033[92m'  # Green for low priority
    
    # Actions
    DELETE_ACTION = '\033[95m'  # Magenta for delete warnings
    EDIT_ACTION = '\033[94m'  # Blue for edit actions
    
    # Neutral or informational
    INFO = '\033[90m'  # Gray for less critical information
    RESET = '\033[0m'  # Alias for ENDC for easier readability


# Example Usage    
print(f"{bcolors.HIGH_PRIORITY}High Priority Task: Finish project report{bcolors.ENDC}")
print(f"{bcolors.MEDIUM_PRIORITY}Medium Priority Task: Buy groceries{bcolors.ENDC}")
print(f"{bcolors.LOW_PRIORITY}Low Priority Task: Water the plants{bcolors.ENDC}")
print(f"{bcolors.DELETE_ACTION}Warning: Are you sure you want to delete this task?{bcolors.ENDC}")
print(f"{bcolors.INFO}Note: Editing tasks is only allowed for tasks you created.{bcolors.ENDC}")
'''