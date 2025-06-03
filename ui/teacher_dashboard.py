from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class TeacherDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome, Teacher"))

        layout.addWidget(QPushButton("📄 Generate QR Codes (Coming Soon)"))
        layout.addWidget(QPushButton("📷 Start QR Scanner (Coming Soon)"))
        layout.addWidget(QPushButton("💾 Save Attendance (Coming Soon)"))
        layout.addWidget(QPushButton("👥 Manage Students (Coming Soon)"))

        self.setLayout(layout)
