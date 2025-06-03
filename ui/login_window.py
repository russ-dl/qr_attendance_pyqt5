from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
from core.auth import login_user, signup_user
from ui.student_dashboard import StudentDashboard
from ui.teacher_dashboard import TeacherDashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Signup")
        self.setFixedSize(300, 250)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.role = QComboBox()
        self.role.addItems(["Student", "Teacher"])

        login_btn = QPushButton("Login")
        signup_btn = QPushButton("Signup")

        login_btn.clicked.connect(self.handle_login)
        signup_btn.clicked.connect(self.handle_signup)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role)
        layout.addWidget(login_btn)
        layout.addWidget(signup_btn)
        self.setLayout(layout)

    def handle_login(self):
        user = login_user(self.username.text(), self.password.text())
        if user:
            if user["role"] == "Student":
                self.dashboard = StudentDashboard(self.username.text())
            else:
                self.dashboard = TeacherDashboard()
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials!")

    def handle_signup(self):
        success = signup_user(self.username.text(), self.password.text(), self.role.currentText())
        if success:
            QMessageBox.information(self, "Signup Successful", "You can now log in.")
        else:
            QMessageBox.warning(self, "Signup Failed", "Username already exists.")
