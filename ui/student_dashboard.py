from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class StudentDashboard(QWidget):
    def __init__(self, student_id):
        super().__init__()
        self.setWindowTitle("Student Dashboard")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Welcome, {student_id}"))

        layout.addWidget(QPushButton("📄 View Attendance (Coming Soon)"))
        layout.addWidget(QPushButton("📤 Export Attendance (Coming Soon)"))
        layout.addWidget(QPushButton("📋 Request Makeup Class (Coming Soon)"))

        self.setLayout(layout)
