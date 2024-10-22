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
        task = {
            'description': description,
            'due_date': due_date,  # Should be in datetime format or None
            'priority': priority,  # Could be 'low', 'medium', 'high'
            'completed': False
        }
        self.tasks.append(task)

    def list_tasks(self, filter_by=None, show_completed=False):
        """List tasks with optional filtering by priority, due date, or status."""
        # Example: filter_by could be 'priority', 'due_date', or 'status'
        # Use 'show_completed' flag to control whether completed tasks are shown or not
        pass

    def mark_completed(self, task_id):
        """Mark a task as completed using the task ID."""
        pass

    def edit_task(self, task_id, description=None, due_date=None, priority=None):
        """Edit task details like description, due date, or priority."""
        pass

    def delete_task(self, task_id):
        """Delete a task by ID."""
        pass

    def save_tasks(self, file_name='tasks.json'):
        """Save tasks to a file (e.g., JSON) to make them persistent."""
        with open(file_name, 'w') as f:
            json.dump(self.tasks, f)

    def load_tasks(self, file_name='tasks.json'):
        """Load tasks from a file on startup to restore saved tasks."""
        try:
            with open(file_name, 'r') as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            # Handle case where file does not exist
            self.tasks = []

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

    # More subcommands for mark, edit, delete...

    return parser.parse_args()

def main():
    # Instantiate ToDoList class
    todo_list = ToDoList()

    # Load existing tasks from file
    todo_list.load_tasks()

    # Parse command-line arguments
    args = handle_args()

    # Handle each command (add, list, mark, etc.)
    if args.command == 'add':
        todo_list.add_task(args.description, args.due_date, args.priority)
        todo_list.save_tasks()
    elif args.command == 'list':
        todo_list.list_tasks(args.filter_by, args.show_completed)
    # Handle other commands like mark, edit, delete...

if __name__ == '__main__':
    main()
