from flask import Flask, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("students.db")
conn.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, department TEXT, email TEXT)")
conn.commit()
conn.close()

@app.route("/students", methods=['GET'])
def get_students():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({"id": row["id"], "name": row["name"], "department": row["department"], "email": row["email"]})
    return result

@app.route("/students/<int:id>", methods=['GET'])
def get_student(id):
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row is None:
        return {"error": "Student not found"}, 404
    return {"id": row["id"], "name": row["name"], "department": row["department"], "email": row["email"]}

@app.route("/students", methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get("name")
    department = data.get("department")
    email = data.get("email")
    if not name or not department or not email:
        return {"error": "All fields are required"}, 400
    conn = sqlite3.connect("students.db")
    cur = conn.execute("INSERT INTO students (name, department, email) VALUES (?, ?, ?)", (name, department, email))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "name": name, "department": department, "email": email}, 201

@app.route("/students/<int:id>", methods=['PUT'])
def update_student(id):
    data = request.get_json()
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    if row is None:
        conn.close()
        return {"error": "Student not found"}, 404
    name = data.get("name", row["name"])
    department = data.get("department", row["department"])
    email = data.get("email", row["email"])
    conn.execute("UPDATE students SET name = ?, department = ?, email = ? WHERE id = ?", (name, department, email, id))
    conn.commit()
    conn.close()
    return {"id": id, "name": name, "department": department, "email": email}

@app.route("/students/<int:id>", methods=['DELETE'])
def delete_student(id):
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    if row is None:
        conn.close()
        return {"error": "Student not found"}, 404
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Student deleted"}

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
