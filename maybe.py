import json
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users(): #load users
    try:
        with open("user1.txt", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if file is missing/not found...
    except json.JSONDecodeError: #return emppty list if json code has an error ...
        return []

def save_tasks(tasks):
    with open("tasks.txt", "w") as f:
        json.dump(tasks, f, indent=4)

def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def add_user(username, password, role="user"):
    """Adds a new user to the system."""
    if username.lower().strip() == "admin":  # Check if the username is "admin"
        print("Username 'admin' is reserved. Please choose a different username.")
        return False 

    users = load_users()
    hashed_password = hash_password(password)
    new_user = {"username": username, "password": hashed_password, "role": "user"}
    users.append(new_user)

    with open("user1.txt", "w") as f:
        json.dump(users, f, indent=4)
    print("User added successfully!")

def authenticate_user():
    users = load_users()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    for user in users:
        if user['username'] == username and user['password'] == hashed_password and user.get('role')== 'user':
            print("Authentication successful!")
            return username

    print("Invalid username or password.")
    return None


    
def is_admin(username):
    """Checks if the user has admin privileges."""
    users = load_users()
    for user in users:
        if user['username'] == username and user.get('role') == 'admin':
            return True
            
        
    return False

def edit_task(tasks, username, is_admin=False):
    """Edits a task for the user or admin."""
    if is_admin:
        display_all_tasks(tasks)
    else:
        display_user_tasks(tasks, username)

    try:
        index = int(input("Enter the task number to edit (or 0 to cancel): ")) - 1 
        if index == -1:
            print("Task editing canceled.")
        elif 0 <= index < len(tasks):
            if is_admin or tasks[index]['user'] == username:
                new_description = input("Enter the new task description: ")
                new_date = input("Enter the new task date (YYYY-MM-DD): ")
                try:
                    task_date = datetime.strptime(new_date, '%Y-%m-%d')
                    if task_date < datetime.now():
                        print("Invalid date. Please enter a future date.")
                        return 
                    tasks[index]['task'] = new_description
                    tasks[index]['date'] = new_date
                    print("Task edited successfully.")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                    return
            else:
                print("You can only edit your own tasks.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
##################################################################################################################################
def display_user_tasks(tasks, username):
    """Displays tasks for a specific user."""
    user_tasks = []
    for task in tasks:
        if task['user'] == username:
            user_tasks.append(task)
    if not user_tasks:
        print("No tasks available.")
        return [] 

    for i, task in enumerate(user_tasks, 1):

        if task['completed']:
             status = "Completed"
        else:
              
              status = "Pending"
        date = task.get('date', 'No date')
        print(f"{i}. {task['task']} ({status}) - Date: {date}")
    return user_tasks



def add_task(tasks, username):
    #Adds a new task for the user.
    while True: 
        task_description = input("Enter a new task: ")
        task_date = input("Enter the task date (YYYY-MM-DD): ")
        try:
            task_date_obj = datetime.strptime(task_date, '%Y-%m-%d') 
            if task_date_obj < datetime.now(): 
                print("Invalid date. Please enter a future date.")
            else:
                tasks.append({"task": task_description, "completed": False, "user": username, "date": task_date})
                print("Task added successfully.")
                break  # Exit the loop after successful addition
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")



def mark_task_as_complete(tasks, username):
    """Marks a task as complete for the user."""
    user_tasks = display_user_tasks(tasks, username)
    if not user_tasks:
        return

    try:
        index = int(input("Enter the task number to mark as complete (or 0 to cancel): ")) - 1
        if index == -1:
            print("Task marking canceled.")
        elif 0 <= index < len(user_tasks):
            user_tasks[index]['completed'] = True
            print("Task marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
#####
def view_tasks(tasks, username):
    """Views tasks for the user with optional filtering."""
    search_query = input("Enter search query (optional): ").lower()
    filter_completed = input("Filter completed tasks? (yes/no): ").strip().lower() == "yes" #if no he will countinue


    user_tasks = []
    for task in tasks:
        if task['user'] == username:
          user_tasks.append(task)

          
    filtered_tasks = []
    for task in user_tasks:
        query_matches = False
        if not search_query:
            query_matches = True
        elif search_query in task['task'].lower():
            query_matches = True

        completion_matches = False
        if not filter_completed:
            completion_matches = True
        elif not task['completed']:
            completion_matches = True

        if query_matches and completion_matches:
            filtered_tasks.append(task)

        if not filtered_tasks:
            print("No tasks match your criteria.")
            return

    for i, task in enumerate(filtered_tasks, 1):
        if task['completed'] == True:
            status = "Completed"
        else:
            status = "Pending"
        date = task.get('date', 'No date')
        print(f"{i}. {task['task']} ({status}) - Date: {date}")

def delete_task(tasks, username, is_admin=False):
    """Deletes a task for the user or admin."""
    if is_admin:
        display_all_tasks(tasks)
    else:
        display_user_tasks(tasks, username)
    
    try:
        index = int(input("Enter the task number to delete (or 0 to cancel): ")) - 1 # حنيكه
        if index == -1:
            print("Deletion canceled.")
        elif 0 <= index < len(tasks):
            if is_admin or tasks[index]['user'] == username:
                tasks.pop(index)
                print("Task deleted.")
            else:
                print("You can only delete your own tasks.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def create_account():
    """Function to create a new user account."""
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    role = "user"
    add_user(username, password, role)
    print("Account created successfully!")


def display_all_tasks(tasks):
    """Displays all tasks for the admin."""
    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks, 1):
        if task['completed']:
            status = "Completed"
        else:
            status = "Pending"
        date = task.get('date', 'No date')
        print(f"{i}. {task['task']} ({status}) - User: {task['user']} - Date: {date}")


