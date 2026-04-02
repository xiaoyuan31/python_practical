import json 

def show_menu():
    print("Task Manager")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Edit Task")
    print("6. Exit")


def main():
    tasks = []

    try: 
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except:
        tasks = []

    while True:
        show_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice in [1,2,3,4,5,6]:
                break 
            else :
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice == 1:
            task = input("Enter the task: ")
            tasks.append({"task": task, "completed": False})
            print("Task added successfully!")
            
        elif choice == 2:
            if not tasks:
                print("No tasks available.")
            else:
                print("Tasks:")
                for idx, task in enumerate(tasks, start=1):
                    status = "✓" if task["completed"] else "❌"
                    print(f"{idx}. [{status}] {task['task']}")
                    
        elif choice == 3:
            if not tasks:
                print("No tasks to complete.")
            else:
                task_num = int(input("Enter the task number to complete: "))
                if 1 <= task_num <= len(tasks):
                    tasks[task_num - 1]["completed"] = True
                    print(f"Task '{tasks[task_num - 1]['task']}' marked as completed!")
                else:
                    print("Invalid task number.")
        elif choice == 4:
            if not tasks:
                print("No tasks to delete.")
            else:
                task_num = int(input("Enter the task number to delete: "))
                if 1 <= task_num <= len(tasks):
                    deleted_task = tasks.pop(task_num - 1)
                    print(f"Task '{deleted_task['task']}' deleted successfully!")
                else:
                    print("Invalid task number.")
        elif choice == 5:
            if not tasks:
                print("No tasks to edit.")
            else:
                task_num = int(input("Enter the task number to edit: "))
                if 1 <= task_num <= len(tasks):
                    new_task = input("Enter the new task description: ")
                    tasks[task_num - 1]["task"] = new_task
                    print(f"Task '{new_task}' updated successfully!")
                else:
                    print("Invalid task number.")
        elif choice == 6:
            print("Exiting Task Manager. Goodbye!")
            with open("tasks.json", "w") as file:
                json.dump(tasks, file)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":    main()