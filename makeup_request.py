from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from data_manager import makeup_requests, save_makeup_requests
from datetime import datetime

class MakeupRequestDialog(QDialog):
    def __init__(self, student_id):
        super().__init__()
        self.setWindowTitle("Makeup Class Request")
        self.student_id = student_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Makeup Class Request Form")
        self.reason_edit = QLineEdit()
        self.submit_btn = QPushButton("Submit Request")

        layout.addWidget(self.label)
        layout.addWidget(QLabel("Reason:"))
        layout.addWidget(self.reason_edit)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

        self.submit_btn.clicked.connect(self.submit_request)

    def submit_request(self):
        reason = self.reason_edit.text().strip()
        if reason:
            makeup_requests.append({
                "student_id": self.student_id,
                "reason": reason,
                "status": "Pending",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_makeup_requests()
            QMessageBox.information(self, "Submitted", "Your makeup request was submitted.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Reason cannot be empty.")
