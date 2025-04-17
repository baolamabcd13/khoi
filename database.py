import sqlite3

class DatabaseManager:
    def __init__(self, db_file="database.db"):
        self.db_file = db_file
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Tạo bảng nếu chưa tồn tại (KHÔNG xóa dữ liệu cũ)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            position TEXT NOT NULL,
            notes TEXT NOT NULL
        )''')
        
        conn.commit()
        conn.close()

    def insert_employee(self, name, email, position, notes):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO employees (name, email, position, notes)
        VALUES (?, ?, ?, ?)
        ''', (name, email, position, notes))
        
        # Lấy ID của record vừa thêm
        last_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return last_id

    def get_all_employees(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        
        conn.close()
        return employees

    def get_employee_by_id(self, id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees WHERE id = ?', (id,))
        employee = cursor.fetchone()
        
        conn.close()
        return employee