from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import qrcode
import os
from config import QR_FOLDER
from data_manager import mark_attendance, save_attendance
from manage_students import ManageStudentsDialog
from qr_scanner_thread import QRScannerThread
from info_popup import InfoPopup

class TeacherDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.setGeometry(300, 150, 700, 500)
        self.scanner_thread = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.btn_generate_qr = QPushButton("Generate QR Code")
        self.btn_start_scanner = QPushButton("Start QR Scanner")
        self.btn_stop_scanner = QPushButton("Stop QR Scanner")
        self.btn_manage_students = QPushButton("Manage Students")
        self.btn_export_attendance = QPushButton("Export Attendance")
        self.btn_open_qr_folder = QPushButton("Open QR Folder")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_generate_qr)
        btn_layout.addWidget(self.btn_start_scanner)
        btn_layout.addWidget(self.btn_stop_scanner)
        btn_layout.addWidget(self.btn_manage_students)
        btn_layout.addWidget(self.btn_export_attendance)
        btn_layout.addWidget(self.btn_open_qr_folder)

        layout.addLayout(btn_layout)

        # === QR Preview Section ===
        self.qr_label = QLabel("QR Preview will appear here")
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setFixedSize(220, 220)

        self.qr_info_label = QLabel("No QR generated yet")
        self.qr_info_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.qr_label)
        layout.addWidget(self.qr_info_label)

        # === Log Area ===
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

        self.btn_generate_qr.clicked.connect(self.generate_qr)
        self.btn_start_scanner.clicked.connect(self.start_scanner)
        self.btn_stop_scanner.clicked.connect(self.stop_scanner)
        self.btn_manage_students.clicked.connect(self.manage_students)
        self.btn_export_attendance.clicked.connect(self.export_attendance)

    def log(self, message):
        self.log_area.append(message)

    def generate_qr(self):
        try:
            dlg = ManageStudentsDialog(select_mode=True)
            if dlg.exec_() == dlg.Accepted:
                selected_id = dlg.get_selected_student_id()
                if selected_id:
                    qr_img = qrcode.make(selected_id)
                    qr_path = os.path.join(QR_FOLDER, f"{selected_id}.png")
                    qr_img.save(qr_path)

                    pix = QPixmap(qr_path)
                    self.qr_label.setPixmap(pix.scaled(200, 200, Qt.KeepAspectRatio))
                    self.qr_info_label.setText(f"QR Code for Student ID: {selected_id}")
                    self.log(f"QR code generated and saved for ID: {selected_id}")
                else:
                    self.log("No student ID selected.")
            else:
                self.log("QR generation cancelled.")
        except Exception as e:
            self.log(f"Error during QR generation: {e}")
            QMessageBox.critical(self, "QR Generation Error", str(e))

    def start_scanner(self):
        if self.scanner_thread and self.scanner_thread.isRunning():
            self.log("Scanner already running.")
            return
        self.scanner_thread = QRScannerThread()
        self.scanner_thread.scanned.connect(self.process_scan)
        self.scanner_thread.error.connect(self.log)
        self.scanner_thread.finished.connect(lambda: self.log("Scanner thread finished"))
        self.scanner_thread.start()
        self.log("Started QR code scanner.")

    def stop_scanner(self):
        if self.scanner_thread and self.scanner_thread.isRunning():
            self.scanner_thread.terminate()
            self.scanner_thread.wait()
            self.log("Stopped QR code scanner.")

    def process_scan(self, student_id):
        try:
            success, name = mark_attendance(student_id, self.log)
            if success:
                InfoPopup.show_message(f"Attendance marked: {name}", 1500)
            else:
                InfoPopup.show_message(f"Already marked: {name}", 1500)
        except Exception as e:
            self.log(f"Error in process_scan: {e}")

    def open_qr_folder(self):
        if os.path.exists(QR_FOLDER):
            try:
                import subprocess
                if os.name == 'nt':  # Windows
                    os.startfile(QR_FOLDER)
                elif os.name == 'posix':  # macOS or Linux
                    subprocess.Popen(['xdg-open', QR_FOLDER])
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open folder:\n{e}")
        else:
            QMessageBox.information(self, "QR Folder", "QR folder does not exist.")

    def manage_students(self):
        dlg = ManageStudentsDialog()
        dlg.exec_()

    def export_attendance(self):
        if save_attendance(self.log):
            InfoPopup.show_message("Attendance exported successfully", 2000)
        else:
            InfoPopup.show_message("Failed to export attendance", 2000)
