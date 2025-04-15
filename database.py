import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            timestamp TEXT,
            session_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def mark_attendance(student_id, session_code):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO attendance (student_id, timestamp, session_code) VALUES (?, ?, ?)',
              (student_id, timestamp, session_code))
    conn.commit()
    conn.close()

def get_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance')
    data = c.fetchall()
    conn.close()
    return data

def get_attendance_by_session(session_code):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance WHERE session_code = ?', (session_code,))
    data = c.fetchall()
    conn.close()
    return data
