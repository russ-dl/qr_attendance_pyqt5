import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QMessageBox
)

STUDENT_DB = "students.json"


class ManageStudentsDialog(QDialog):
    def __init__(self, select_mode=False):
        super().__init__()
        self.select_mode = select_mode
        self.selected_student_id = None
        self.setWindowTitle("Select Student" if select_mode else "Manage Students")
        self.setFixedSize(500, 400)

        self.students = self.load_students()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Name"])
        layout.addWidget(self.table)

        form_layout = QHBoxLayout()
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        self.btn_close = QPushButton("Close")

        self.btn_add.clicked.connect(self.add_student)
        self.btn_edit.clicked.connect(self.edit_student)
        self.btn_delete.clicked.connect(self.delete_student)
        self.btn_close.clicked.connect(self.close)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)

        if self.select_mode:
            self.btn_add.hide()
            self.btn_edit.hide()
            self.btn_delete.hide()

            self.btn_select = QPushButton("Select")
            self.btn_select.clicked.connect(self.select_student)
            btn_layout.addWidget(self.btn_select)

        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_table()

    def load_students(self):
        if not os.path.exists(STUDENT_DB):
            return {}
        with open(STUDENT_DB, "r") as f:
            return json.load(f)

    def save_students(self):
        with open(STUDENT_DB, "w") as f:
            json.dump(self.students, f, indent=4)

    def load_table(self):
        self.table.setRowCount(0)
        for row, (student_id, name) in enumerate(self.students.items()):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(student_id))
            self.table.setItem(row, 1, QTableWidgetItem(name))

    def add_student(self):
        sid = self.id_input.text().strip()
        name = self.name_input.text().strip()
        if not sid or not name:
            QMessageBox.warning(self, "Error", "Please enter ID and Name.")
            return
        if sid in self.students:
            QMessageBox.warning(self, "Error", "Student ID already exists.")
            return
        self.students[sid] = name
        self.save_students()
        self.load_table()
        self.id_input.clear()
        self.name_input.clear()

    def edit_student(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Select a student to edit.")
            return
        sid = self.table.item(row, 0).text()
        new_name = self.name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Error", "Enter a new name.")
            return
        self.students[sid] = new_name
        self.save_students()
        self.load_table()
        self.name_input.clear()

    def delete_student(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Select a student to delete.")
            return
        sid = self.table.item(row, 0).text()
        del self.students[sid]
        self.save_students()
        self.load_table()

    def select_student(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Select a student.")
            return
        self.selected_student_id = self.table.item(row, 0).text()
        self.accept()

    def get_selected_student_id(self):
        return self.selected_student_id
