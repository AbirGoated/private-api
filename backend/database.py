import sqlite3

def get_connection():
    connection = sqlite3.connect("tasks.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

connection = get_connection()
cursor = connection.cursor()

#project table creation:
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

#tasks table creation:
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    project_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)
""")

connection.commit()
connection.close()

def create_task(title, project_id=None):
    cursor.execute("""INSERT INTO tasks (title, completed, project_id) VALUES (?, ?, ?)""", (title, 0, project_id))
    connection.commit()
    task_id = cursor.lastrowid
    connection.close()
    return task_id


def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT tasks.id, tasks.title, tasks.completed, tasks.project_id, projects.name FROM tasks LEFT JOIN projects ON tasks.project_id = projects.id ORDER BY tasks.id DESC""")
    tasks = cursor.fetchall()
    connection.close()
    return tasks


def get_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT tasks.id, tasks.title, tasks.completed, tasks.project_id, projects.name FROM tasks LEFT JOIN projects ON tasks.project_id = projects.id WHERE tasks.id = ?""", (task_id,))
    task = cursor.fetchall()
    connection.close()
    return task

def complete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""UPDATE tasks SET completed = 1 WHERE id = ?""", (task_id,))
    connection.commit()
    rows = cursor.rowcount
    connection.close()
    return rows


def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM tasks WHERE id = ?""", (task_id,))
    connection.commit()
    rows = cursor.rowcount
    connection.close()
    return rows


# choice = input("""
#     Choose an operation:
#     1. Insert Task
#     2. Read All (sorted)
#     3. Read Specific Task
#     4. Update Task To Completed
#     5. Count Total Tasks
#     6. Count Completed Tasks
#     7. Read Latest Tasks
#     8. Search Tasks
#     9. Delete Task
#     10. Insert Project
#     11. Read Projects
#     12. Delete Project
#     Enter Choice: """)
# if choice == "1":
#     title=input("Enter task title: ")
#     project_id=input("Enter project id or leave blank if none: ")
#     if project_id == "":
#         project_id = None
#     else:
#         project_id = int(project_id)
#     cursor.execute("""
#     INSERT INTO tasks(title, completed, project_id)
#     VALUES (?, ?, ?)
#     """,(title, 0, project_id))
#     print("Task added")
# elif choice == "2":
#     cursor.execute("""SELECT tasks.id, tasks.title, tasks.completed, tasks.project_id, projects.name FROM tasks LEFT JOIN projects ON tasks.project_id = projects.id ORDER BY tasks.id DESC""")
#     rows = cursor.fetchall()
#     print(rows)
# elif choice == "3":
#     task_id=int(input("Enter task id to view: "))
#     cursor.execute("""SELECT tasks.id, tasks.title, tasks.completed, tasks.project_id, projects.name FROM tasks LEFT JOIN projects ON tasks.project_id = projects.id WHERE tasks.id = ?""", (task_id,))
#     row = cursor.fetchone()
#     print(row)
# elif choice == "4":
#     task_id=int(input("Enter task id to update: "))
#     cursor.execute("""
#         UPDATE tasks
#         SET completed = ?
#         WHERE id = ?
#         """, (1, task_id))
#     if cursor.rowcount==1:
#         print("Task Updated")
#     else:
#         print("Task not found")
# elif choice == "5":
#     cursor.execute("SELECT COUNT(*) FROM tasks")
#     res = cursor.fetchone()
#     print("Total tasks: ", res[0])
# elif choice == "6":
#     cursor.execute("""
#         SELECT COUNT(*)
#         FROM tasks
#         WHERE completed=?
#     """, (1,))
#     res=cursor.fetchone()
#     print("Completed tasks: ", res[0])
# elif choice == "7":
#     lim=int(input("How many tasks do you wish to see? "))
#     cursor.execute("""SELECT * FROM tasks ORDER BY id DESC LIMIT ?""", (lim,))
#     rows = cursor.fetchall()
#     print(rows)
# elif choice == "8":
#     search=input("Enter task: ")
#     cursor.execute("""SELECT * FROM tasks WHERE title LIKE ?""", (f"%{search}%",))
#     rows = cursor.fetchall()
#     print(rows)
# elif choice == "9":
#     task_id=int(input("Enter task id: "))
#     cursor.execute("""DELETE FROM tasks WHERE id = ?""", (task_id,))
#     if cursor.rowcount==1:
#         print("Task deleted")
#     else:
#         print("Task not found")
# elif choice == "10":
#     project_name=input("Enter project name: ")
#     cursor.execute("""INSERT INTO projects (name) VALUES (?)""", (project_name,))
#     print("Project Added")
# elif choice == "11":
#     cursor.execute("SELECT * FROM projects")
#     projects = cursor.fetchall()
#     print(projects)
# elif choice == "12":
#     project_id = int(input("Enter project id to be deleted: "))
#     cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
#     if cursor.rowcount==1:
#         print("Project deleted")
#     else:
#         print("Project not found")
# else:
#     print("Invalid Choice")


# connection.commit()
# connection.close()