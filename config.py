import os

QR_FOLDER = "qr_codes"
EXCEL_FOLDER = "attendance_records"
USER_DB = "users.json"
STUDENT_DB = "students.json"
MAKEUP_DB = "makeup_requests.json"

os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(EXCEL_FOLDER, exist_ok=True)
