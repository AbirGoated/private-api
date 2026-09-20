import sqlite3

connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()

#table creation:
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0
)
""")

choice = input("""
    Choose an operation:
    1. Insert
    2. Read All (sorted)
    3. Read Specific Task
    4. Update Task To Completed
    5. Count Total Tasks
    6. Count Completed Tasks
    7. Delete
    
    Enter Choice: """)
if choice == "1":
    #data insertion in tables:
    title=input("Enter task to be added: ")
    cursor.execute("""
    INSERT INTO tasks(title, completed)
    VALUES (?, ?)
    """,(title, 0))
    print("Task added")
elif choice == "2":
    #read all sorted data:
    cursor.execute("""SELECT * FROM tasks ORDER BY id DESC""")
    rows = cursor.fetchall()
    print(rows)
elif choice == "3":
    #read specific data:
    task_id=int(input("Enter task id to view: "))
    cursor.execute("SELECT*FROM tasks WHERE id=?", (task_id,))
    row = cursor.fetchone()
    print(row)
elif choice == "4":
    #Update data:
    task_id=int(input("Enter task id to update: "))
    cursor.execute("""
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
        """, (1, task_id))
    if cursor.rowcount==1:
        print("Task Updated")
    else:
        print("Task not found")
elif choice == "5":
    cursor.execute("SELECT COUNT(*) FROM tasks")
    res = cursor.fetchone()
    print("Total tasks: ", res[0])
elif choice == "6":
    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE completed=?
    """, (1,))
    res=cursor.fetchone()
    print("Completed tasks: ", res[0])
elif choice == "7":
    #delete data:
    task_id=int(input("Enter task id: "))
    cursor.execute("""DELETE FROM tasks WHERE id = ?""", (task_id,))
    if cursor.rowcount==1:
        print("Task deleted")
    else:
        print("Task not found")
else:
    print("Invalid Choice")


connection.commit()
connection.close()