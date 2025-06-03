from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QHBoxLayout, QMessageBox
from makeup_request import MakeupRequestDialog
from data_manager import students_info, save_students, makeup_requests, save_makeup_requests
from data_manager import attendance_df, save_attendance
import pandas as pd

class StudentDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Student Dashboard - {username}")
        self.setGeometry(300, 150, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_welcome = QLabel(f"Welcome, {self.username}")
        layout.addWidget(self.label_welcome)

        self.btn_view_attendance = QPushButton("View Attendance")
        self.btn_export_attendance = QPushButton("Export Attendance to Excel")
        self.btn_makeup_request = QPushButton("Request Makeup Class")
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        layout.addWidget(self.btn_view_attendance)
        layout.addWidget(self.btn_export_attendance)
        layout.addWidget(self.btn_makeup_request)
        layout.addWidget(self.text_area)

        self.setLayout(layout)

        self.btn_view_attendance.clicked.connect(self.view_attendance)
        self.btn_export_attendance.clicked.connect(self.export_attendance)
        self.btn_makeup_request.clicked.connect(self.open_makeup_request)

    def view_attendance(self):
        student_id = self.username
        if student_id not in students_info:
            QMessageBox.warning(self, "Error", "Student info not found.")
            return
        df = attendance_df[attendance_df['ID'] == student_id]
        if df.empty:
            self.text_area.setText("No attendance records found.")
            return
        text = df.to_string(index=False)
        self.text_area.setText(text)

    def export_attendance(self):
        if save_attendance():
            QMessageBox.information(self, "Exported", "Attendance exported successfully.")
        else:
            QMessageBox.warning(self, "Error", "Failed to export attendance.")

    def open_makeup_request(self):
        dialog = MakeupRequestDialog(self.username)
        dialog.exec_()
