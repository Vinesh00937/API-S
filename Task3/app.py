from flask import Flask, request
import secrets

app = Flask(__name__)

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "employee": {"password": "emp123", "role": "employee"}
}

tokens = {}

employees = [
    {"id": 1, "name": "Ayesha Khan", "department": "IT", "email": "ayesha@company.com"},
    {"id": 2, "name": "Bilal Ahmed", "department": "HR", "email": "bilal@company.com"}
]
next_id = 3

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = users.get(username)
    if not user or user["password"] != password:
        return {"error": "Invalid credentials"}, 401
    token = secrets.token_hex(16)
    tokens[token] = {"username": username, "role": user["role"]}
    return {"token": token, "role": user["role"]}

@app.route("/employees", methods=['GET'])
def get_employees():
    header = request.headers.get("Authorization", "")
    token = header.replace("Bearer ", "")
    user = tokens.get(token)
    if not user:
        return {"error": "Login required"}, 401
    return employees

@app.route("/employees/<int:id>", methods=['GET'])
def get_employee(id):
    header = request.headers.get("Authorization", "")
    token = header.replace("Bearer ", "")
    user = tokens.get(token)
    if not user:
        return {"error": "Login required"}, 401
    for emp in employees:
        if emp["id"] == id:
            return emp
    return {"error": "Employee not found"}, 404

@app.route("/employees", methods=['POST'])
def add_employee():
    header = request.headers.get("Authorization", "")
    token = header.replace("Bearer ", "")
    user = tokens.get(token)
    if not user:
        return {"error": "Login required"}, 401
    if user["role"] != "admin":
        return {"error": "Only admin can add"}, 403
    global next_id
    data = request.get_json()
    emp = {"id": next_id, "name": data.get("name"), "department": data.get("department"), "email": data.get("email")}
    next_id = next_id + 1
    employees.append(emp)
    return emp, 201

@app.route("/employees/<int:id>", methods=['PUT'])
def update_employee(id):
    header = request.headers.get("Authorization", "")
    token = header.replace("Bearer ", "")
    user = tokens.get(token)
    if not user:
        return {"error": "Login required"}, 401
    if user["role"] != "admin":
        return {"error": "Only admin can update"}, 403
    data = request.get_json()
    for emp in employees:
        if emp["id"] == id:
            emp["name"] = data.get("name", emp["name"])
            emp["department"] = data.get("department", emp["department"])
            emp["email"] = data.get("email", emp["email"])
            return emp
    return {"error": "Employee not found"}, 404

@app.route("/employees/<int:id>", methods=['DELETE'])
def delete_employee(id):
    header = request.headers.get("Authorization", "")
    token = header.replace("Bearer ", "")
    user = tokens.get(token)
    if not user:
        return {"error": "Login required"}, 401
    if user["role"] != "admin":
        return {"error": "Only admin can delete"}, 403
    for emp in employees:
        if emp["id"] == id:
            employees.remove(emp)
            return {"message": "Employee deleted"}
    return {"error": "Employee not found"}, 404

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
