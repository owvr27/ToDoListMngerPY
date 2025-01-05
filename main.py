import maybe


def main():
    """Main function to run the task manager."""
    while True:
        print("""
        ==== Welcome to Task Manager ====
        1. Sign In
        2. Create Account
        3. Quit
        """)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            username = maybe.authenticate_user()
            if username:
                print(f"Welcome, {username}!")
                tasks = maybe.load_tasks()
                is_user_admin = maybe.is_admin(username)
                while True:
                    print("""
                    ==== Task Manager ====
                    1. Add Task
                    2. Mark Task as Complete
                    3. View Tasks
                    4. Edit Task
                    5. Delete Task
                    6. sign out
                    """)
                    if is_user_admin:
                        print("                    7. View All Tasks (Admin Only)")
                        print("                    8. Edit Any Task (Admin Only)")
                        print("                    9. Delete Any Task (Admin Only)")

                    choice = input("Enter your choice: ").strip()

                    if choice == "1":
                        maybe.add_task(tasks, username)
                    elif choice == "2":
                        maybe.mark_task_as_complete(tasks, username)
                    elif choice == "3":
                        maybe.view_tasks(tasks, username)
                    elif choice == "4":
                        maybe.edit_task(tasks, username)
                    elif choice == "5":
                        maybe.delete_task(tasks, username)
                    elif choice == "6":
                        maybe.save_tasks(tasks)
                        print("Tasks saved. Goodbye!")
                        break
                    elif choice == "7" and is_user_admin:
                        maybe.display_all_tasks(tasks)
                    elif choice == "8" and is_user_admin:
                        maybe.edit_task(tasks, username, is_admin=True)
                    elif choice == "9" and is_user_admin:
                        maybe.delete_task(tasks, username, is_admin=True)
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password. Exiting.")
        elif choice == "2":
            maybe.create_account()
        elif choice == "3":
            print("Goodbye! ")
            break
        else:
            print("Invalid choice. Please try again.")

main()