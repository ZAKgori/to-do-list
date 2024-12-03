import argparse
import json
from datetime import datetime

# Main class to handle tasks
class ToDoList:
    def __init__(self):
        # List to hold tasks
        self.tasks = []

    def add_task(self, description, due_date=None, priority=None):
        """Add a new task with description, optional due date, and priority."""
        due_date = datetime.strptime(due_date, '%Y-%m-%d').isoformat() if due_date else None
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'due_date': due_date,  # In ISO format or None
            'priority': priority,  # 'low', 'medium', 'high' or None
            'completed': False
        }
        self.tasks.append(task)
        print(f"Task '{description}' added.")

    def list_tasks(self, filter_by=None, show_completed=False):
        """List tasks with optional filtering by priority, due date, or status."""
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
        """Mark a task as completed using the task ID."""
        task = next((task for task in self.tasks if task['id'] == task_id), None)
        if task:
            task['completed'] = True
            print(f"Task '{task['description']}' marked as completed.")
        else:
            print(f"Task with ID {task_id} not found.")

    def edit_task(self, task_id, description=None, due_date=None, priority=None):
        """Edit task details like description, due date, or priority."""
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
        """Delete a task by ID."""
        task = next((task for task in self.tasks if task['id'] == task_id), None)
        if task:
            self.tasks.remove(task)
            print(f"Task '{task['description']}' deleted.")
        else:
            print(f"Task with ID {task_id} not found.")

    def save_tasks(self, file_name='tasks.json'):
        """Save tasks to a file (e.g., JSON) to make them persistent."""
        with open(file_name, 'w') as f:
            json.dump(self.tasks, f)
        print("Tasks saved to file.")

    def load_tasks(self, file_name='tasks.json'):
        """Load tasks from a file on startup to restore saved tasks."""
        try:
            with open(file_name, 'r') as f:
                self.tasks = json.load(f)
            print("Tasks loaded from file.")
        except FileNotFoundError:
            # Handle case where file does not exist
            self.tasks = []
            print("No saved tasks found, starting with an empty list.")

# Function to handle command-line arguments
def handle_args():
    """Parse command-line arguments using argparse."""
    parser = argparse.ArgumentParser(description="Command-Line To-Do List Application")
    
    # Define subcommands for add, list, mark, edit, delete, etc.
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', type=str, help='Description of the task')
    add_parser.add_argument('--due_date', type=str, help='Due date of the task (YYYY-MM-DD)')
    add_parser.add_argument('--priority', type=str, choices=['low', 'medium', 'high'], help='Priority of the task')

    # List tasks command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--filter_by', type=str, choices=['priority', 'due_date', 'status'], help='Filter tasks by priority, due date, or status')
    list_parser.add_argument('--show_completed', action='store_true', help='Show completed tasks as well')

    # Mark completed command
    mark_parser = subparsers.add_parser('mark', help='Mark a task as completed')
    mark_parser.add_argument('task_id', type=int, help='ID of the task to mark as completed')

    # Edit task command
    edit_parser = subparsers.add_parser('edit', help='Edit an existing task')
    edit_parser.add_argument('task_id', type=int, help='ID of the task to edit')
    edit_parser.add_argument('--description', type=str, help='New description for the task')
    edit_parser.add_argument('--due_date', type=str, help='New due date for the task (YYYY-MM-DD)')
    edit_parser.add_argument('--priority', type=str, choices=['low', 'medium', 'high'], help='New priority for the task')

    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='ID of the task to delete')

    return parser.parse_args()

def main():
    # Instantiate ToDoList class
    todo_list = ToDoList()

    # Load existing tasks from file
    todo_list.load_tasks()

    # Parse command-line arguments
    args = handle_args()

    # Handle each command (add, list, mark, edit, delete)
    if args.command == 'add':
        todo_list.add_task(args.description, args.due_date, args.priority)
        todo_list.save_tasks()
    elif args.command == 'list':
        todo_list.list_tasks(args.filter_by, args.show_completed)
    elif args.command == 'mark':
        todo_list.mark_completed(args.task_id)
        todo_list.save_tasks()
    elif args.command == 'edit':
        todo_list.edit_task(args.task_id, args.description, args.due_date, args.priority)
        todo_list.save_tasks()
    elif args.command == 'delete':
        todo_list.delete_task(args.task_id)
        todo_list.save_tasks()
    else:
        print("No valid command provided. Use --help for usage information.")

if __name__ == '__main__':
    main()
