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
    2. Read all
    3. Read specific data
    4. Update
    5. Delete
    
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
    #read all data:
    cursor.execute("""SELECT * FROM tasks""")
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
    print("Updated")
elif choice == "5":
    #delete data:
    task_id=int(input("Enter task id: "))
    cursor.execute("""DELETE FROM tasks WHERE id = ?""", (task_id,))
    print("Deleted")
else:
    print("Invalid Choice")


connection.commit()
connection.close()