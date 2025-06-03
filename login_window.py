from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, QMessageBox
from utils import hash_password
from data_manager import users, save_users, load_all
from student_dashboard import StudentDashboard
from teacher_dashboard import TeacherDashboard


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Attendance Login/Signup")
        self.setGeometry(300, 200, 350, 280)
        load_all()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_title = QLabel("<h2>Welcome</h2>")
        layout.addWidget(self.label_title)

        self.combo_role = QComboBox()
        self.combo_role.addItems(["Student", "Teacher"])
        layout.addWidget(self.combo_role)

        self.edit_username = QLineEdit()
        self.edit_username.setPlaceholderText("Username")
        layout.addWidget(self.edit_username)

        self.edit_password = QLineEdit()
        self.edit_password.setPlaceholderText("Password")
        self.edit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_password)

        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("Login")
        self.btn_signup = QPushButton("Sign Up")
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_signup)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_login.clicked.connect(self.login)
        self.btn_signup.clicked.connect(self.signup)

    def login(self):
        role = self.combo_role.currentText()
        username = self.edit_username.text().strip()
        password = self.edit_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password.")
            return

        if username in users:
            user = users[username]
            if user["role"] == role and user["password"] == hash_password(password):
                QMessageBox.information(self, "Success", f"Logged in as {role}: {username}")
                self.open_dashboard(role, username)
            else:
                QMessageBox.warning(self, "Error", "Incorrect credentials or role.")
        else:
            QMessageBox.warning(self, "Error", "User does not exist.")

    def signup(self):
        role = self.combo_role.currentText()
        username = self.edit_username.text().strip()
        password = self.edit_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password.")
            return

        if username in users:
            QMessageBox.warning(self, "Error", "User already exists.")
            return

        users[username] = {
            "role": role,
            "password": hash_password(password)
        }
        save_users()
        QMessageBox.information(self, "Success", "User registered successfully.")

    def open_dashboard(self, role, username):
        self.hide()
        if role == "Student":
            self.student_dashboard = StudentDashboard(username)
            self.student_dashboard.show()
        else:
            self.teacher_dashboard = TeacherDashboard()
            self.teacher_dashboard.show()
