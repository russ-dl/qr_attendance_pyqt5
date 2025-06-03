import json
import os
import pandas as pd
from datetime import datetime
from config import USER_DB, STUDENT_DB, MAKEUP_DB, EXCEL_FOLDER

# Global data stores
users = {}
students_info = {}
makeup_requests = []
attendance_df = pd.DataFrame(columns=['ID', 'Name', 'Section', 'Date', 'Time', 'Present'])

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f:
                content = f.read().strip()
                return json.loads(content) if content else default
        except json.JSONDecodeError:
            return default
    else:
        return default

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def load_all():
    global users, students_info, makeup_requests
    users.clear()
    users.update(load_json(USER_DB, {}))

    students_info.clear()
    students_info.update(load_json(STUDENT_DB, {}))

    makeup_requests.clear()
    makeup_requests.extend(load_json(MAKEUP_DB, []))


def save_users():
    save_json(USER_DB, users)

def save_students():
    save_json(STUDENT_DB, students_info)

def save_makeup_requests():
    save_json(MAKEUP_DB, makeup_requests)

def mark_attendance(student_id, log_func=None):
    global attendance_df
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    student_data = students_info.get(student_id, {})
    student_name = student_data.get("name", "Unknown")
    student_section = student_data.get("section", "Unknown")

    if not ((attendance_df['ID'] == student_id) & (attendance_df['Date'] == current_date)).any():
        new_entry = {
            'ID': student_id,
            'Name': student_name,
            'Section': student_section,
            'Date': current_date,
            'Time': current_time,
            'Present': True
        }
        attendance_df = pd.concat([attendance_df, pd.DataFrame([new_entry])], ignore_index=True)
        if log_func:
            log_func(f"🎯 {student_name} ({student_id}) marked present at {current_time}")
        return True, student_name
    else:
        if log_func:
            log_func(f"⚠️ {student_name} ({student_id}) already marked for today.")
        return False, student_name

def save_attendance(log_func=None):
    filename = os.path.join(EXCEL_FOLDER, f"attendance_{datetime.now().strftime('%Y-%m-%d')}.xlsx")
    try:
        attendance_df.to_excel(filename, index=False, engine='openpyxl')
        if log_func:
            log_func(f"📂 Attendance saved to {filename}")
        return True, filename
    except Exception as e:
        if log_func:
            log_func(f"❌ Error saving attendance: {e}")
        return False, str(e)
