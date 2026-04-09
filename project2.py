import streamlit as st

# -----------------------
# Initialize Session State
# -----------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "admin", "role": "admin"},
        "teacher1": {"password": "teach123", "role": "teacher"},
        "student1": {"password": "stud123", "role": "student"}
    }

if "questions" not in st.session_state:
    st.session_state.questions = []

if "results" not in st.session_state:
    st.session_state.results = {}

if "internal_marks" not in st.session_state:
    st.session_state.internal_marks = {}

# -----------------------
# Admin Menu
# -----------------------
def admin_menu():
    st.subheader("Admin Menu")
    choice = st.radio("Select Option", ["Add User", "View Users"])
    
    if choice == "Add User":
        username = st.text_input("New Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["teacher", "student"])
        if st.button("Add"):
            st.session_state.users[username] = {"password": password, "role": role}
            st.success(role.capitalize() + " added successfully!")
    
    elif choice == "View Users":
        st.write("### Registered Users")
        for u, d in st.session_state.users.items():
            st.write(u + " → " + d["role"])

# -----------------------
# Teacher Menu
# -----------------------
def teacher_menu(username):
    st.subheader("Teacher Menu")
    choice = st.radio("Select Option", ["Add Question", "Enter Internal Marks"])
    
    if choice == "Add Question":
        q = st.text_input("Enter question")
        opt1 = st.text_input("Option 1")
        opt2 = st.text_input("Option 2")
        opt3 = st.text_input("Option 3")
        opt4 = st.text_input("Option 4")
        ans = st.selectbox("Correct Option", ["1", "2", "3", "4"])
        if st.button("Save Question"):
            st.session_state.questions.append({"q": q, "options": [opt1, opt2, opt3, opt4], "ans": ans})
            st.success("Question added!")
    
    elif choice == "Enter Internal Marks":
        student = st.selectbox("Select Student", [u for u, d in st.session_state.users.items() if d["role"] == "student"])
        marks = st.number_input("Enter Marks", 0, 100)
        if st.button("Save Marks"):
            st.session_state.internal_marks[student] = marks
            st.success("Marks updated!")

# -----------------------
# Student Menu
# -----------------------
def student_menu(username):
    st.subheader("Student Menu")
    choice = st.radio("Select Option", ["Give Exam", "View Result"])
    
    if choice == "Give Exam":
        answers = {}
        for i, q in enumerate(st.session_state.questions, 1):
            st.write(f"Q{i}. {q['q']}")
            answers[i] = st.radio("Choose Option", q["options"], key=f"q{i}")
        
        if st.button("Finish Exam"):
            score = 0
            for i, q in enumerate(st.session_state.questions, 1):
                if str(q["options"].index(answers[i]) + 1) == q["ans"]:
                    score += 1
            st.session_state.results[username] = score
            st.success(f"Exam finished! Score: {score}/{len(st.session_state.questions)}")
    
    elif choice == "View Result":
        s = st.session_state.results.get(username, "Not given exam")
        im = st.session_state.internal_marks.get(username, 0)
        st.write("Exam Score:", s)
        st.write("Internal Marks:", im)

# -----------------------
# MAIN PROGRAM
# -----------------------
def main():
    st.title("📘 Online Examination System")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = st.session_state.users.get(username)
        if user and user["password"] == password:
            role = user["role"]
            st.success("Welcome " + username + " (" + role + ")")
            
            if role == "admin":
                admin_menu()
            elif role == "teacher":
                teacher_menu(username)
            elif role == "student":
                student_menu(username)
        else:
            st.error("Invalid username or password!")

if __name__ == "__main__":
    main()
