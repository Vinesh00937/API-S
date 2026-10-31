import streamlit as st
import requests

API = "http://127.0.0.1:5000/students"

st.title("Student Management")

# Get all students and show them in a table
students = requests.get(API).json()
st.subheader("All Students")
st.table(students)

# Form to add a new student
# Each box needs a different key, otherwise Streamlit gets confused
st.subheader("Add a New Student")
name = st.text_input("Name", key="add_name")
department = st.text_input("Department", key="add_department")
email = st.text_input("Email", key="add_email")
if st.button("Add"):
    r = requests.post(API, json={"name": name, "department": department, "email": email})
    if r.status_code == 201:
        st.success("Student added!")
        st.rerun()
    else:
        st.error("Could not add the student, please check again")

# Update or delete an existing student
if students:
    st.subheader("Update / Delete a Student")
    names = []
    for s in students:
        names.append(str(s["id"]) + " - " + s["name"])
    choice = st.selectbox("Select a student", names)
    sid = int(choice.split(" - ")[0])
    old = None
    for s in students:
        if s["id"] == sid:
            old = s
    new_name = st.text_input("Name", old["name"], key="update_name")
    new_dept = st.text_input("Department", old["department"], key="update_department")
    new_email = st.text_input("Email", old["email"], key="update_email")
    if st.button("Update"):
        r = requests.put(API + "/" + str(sid), json={"name": new_name, "department": new_dept, "email": new_email})
        if r.status_code == 200:
            st.success("Student updated!")
            st.rerun()
    if st.button("Delete"):
        r = requests.delete(API + "/" + str(sid))
        if r.status_code == 200:
            st.success("Student deleted!")
            st.rerun()
