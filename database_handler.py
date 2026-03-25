import sqlite3
import os
from datetime import datetime
import paths


class DatabaseHandler:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = paths.get_db_file_path()

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        print(f"🔄 Подключение к БД: {db_path}")
        self.create_tables()
        self.check_and_add_default_data()
        self._ensure_new_columns()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS branches (
                                                               branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                               name TEXT NOT NULL,
                                                               floors_count INTEGER NOT NULL DEFAULT 1,
                                                               address TEXT NOT NULL DEFAULT ''
                       )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS employees (
                                                                worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name_id TEXT NOT NULL,
                                                                job_title TEXT NOT NULL,
                                                                report_count INTEGER NOT NULL DEFAULT 0,
                                                                date_of_work TEXT NOT NULL,
                                                                branch_id INTEGER,
                                                                phone TEXT,
                                                                email TEXT,
                                                                FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE SET NULL
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS environment (
                                                                  environment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                  environment_name TEXT NOT NULL,
                                                                  branch_id INTEGER NOT NULL,
                                                                  FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE CASCADE
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS room (
                                                           room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                           room_number TEXT NOT NULL,
                                                           room_name TEXT NOT NULL,
                                                           branch_id INTEGER,
                                                           floor INTEGER DEFAULT 1,
                                                           capacity INTEGER DEFAULT 0,
                                                           desks_count INTEGER DEFAULT 0,
                                                           chairs_count INTEGER DEFAULT 0,
                                                           sockets_count INTEGER DEFAULT 0,
                                                           area REAL DEFAULT 0.0,
                                                           responsible_employee_id INTEGER,
                                                           notes TEXT DEFAULT '',
                                                           FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE CASCADE,
                           FOREIGN KEY (responsible_employee_id) REFERENCES employees(worker_id) ON DELETE SET NULL
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS equipment (
                                                                equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name TEXT NOT NULL,
                                                                category TEXT DEFAULT '',
                                                                type TEXT DEFAULT '',
                                                                model TEXT DEFAULT '',
                                                                manufacturer TEXT DEFAULT '',
                                                                quantity INTEGER NOT NULL DEFAULT 1,
                                                                serial_number TEXT UNIQUE,
                                                                inventory_number TEXT DEFAULT '',
                                                                price REAL DEFAULT 0,
                                                                date_incoming TEXT,
                                                                supplier TEXT DEFAULT '',
                                                                phone_supplier TEXT DEFAULT '',
                                                                email_supplier TEXT DEFAULT '',
                                                                status TEXT DEFAULT 'in_use',
                                                                last_inventory_date TEXT,
                                                                notes TEXT DEFAULT '',
                                                                room_id INTEGER,
                                                                branch_id INTEGER,
                                                                workplace_number INTEGER DEFAULT NULL,
                                                                FOREIGN KEY (room_id) REFERENCES room(room_id) ON DELETE SET NULL,
                           FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE CASCADE
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS arrivals (
                                                               arrival_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                               name TEXT NOT NULL,
                                                               order_number TEXT,
                                                               description TEXT,
                                                               branch_id INTEGER,
                                                               employee_id INTEGER,
                                                               date TEXT,
                                                               doc_number TEXT,
                                                               supplier_name TEXT,
                                                               supplier_inn TEXT,
                                                               supplier_phone TEXT,
                                                               supplier_email TEXT,
                                                               total_amount REAL,
                                                               waybill_number TEXT,
                                                               contract_number TEXT,
                                                               notes TEXT,
                                                               FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE SET NULL,
                           FOREIGN KEY (employee_id) REFERENCES employees(worker_id) ON DELETE SET NULL
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS reports (
                                                              report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                              report_name TEXT NOT NULL,
                                                              report_date TIMESTAMP NOT NULL,
                                                              description TEXT NOT NULL,
                                                              order_number INTEGER NOT NULL,
                                                              worker_id INTEGER,
                                                              environment_id INTEGER,
                                                              equipment_id INTEGER,
                                                              FOREIGN KEY (worker_id) REFERENCES employees(worker_id) ON DELETE SET NULL,
                           FOREIGN KEY (environment_id) REFERENCES environment(environment_id) ON DELETE SET NULL,
                           FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE SET NULL
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS inventory_log (
                                                                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    report_id INTEGER NOT NULL,
                                                                    equipment_id INTEGER NOT NULL,
                                                                    old_status TEXT,
                                                                    new_status TEXT,
                                                                    comment TEXT,
                                                                    inventory_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                                    worker_id INTEGER,
                                                                    FOREIGN KEY (report_id) REFERENCES reports(report_id) ON DELETE CASCADE,
                           FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE,
                           FOREIGN KEY (worker_id) REFERENCES employees(worker_id) ON DELETE SET NULL
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users (
                                                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            username TEXT UNIQUE NOT NULL,
                                                            password TEXT NOT NULL,
                                                            role TEXT DEFAULT 'user'
                       )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS company (
                                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                              name TEXT NOT NULL
                       )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS floor_maps (
                                                                 map_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                 branch_id INTEGER NOT NULL,
                                                                 floor_number INTEGER NOT NULL,
                                                                 image_path TEXT NOT NULL,
                                                                 UNIQUE(branch_id, floor_number),
                           FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE CASCADE
                           )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS room_markers (
                                                                   marker_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                   map_id INTEGER NOT NULL,
                                                                   room_id INTEGER NOT NULL,
                                                                   x REAL NOT NULL,
                                                                   y REAL NOT NULL,
                                                                   UNIQUE(map_id, room_id),
                           FOREIGN KEY (map_id) REFERENCES floor_maps(map_id) ON DELETE CASCADE,
                           FOREIGN KEY (room_id) REFERENCES room(room_id) ON DELETE CASCADE
                           )
                       ''')

        conn.commit()
        conn.close()
        print("✅ Таблицы созданы/проверены!")

    def _ensure_new_columns(self):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(equipment)")
            columns = [col['name'] for col in cursor.fetchall()]

            new_columns = {
                'model': 'TEXT DEFAULT ""',
                'manufacturer': 'TEXT DEFAULT ""',
                'inventory_number': 'TEXT DEFAULT ""',
                'workplace_number': 'INTEGER DEFAULT NULL'
            }

            for col_name, col_def in new_columns.items():
                if col_name not in columns:
                    try:
                        cursor.execute(f"ALTER TABLE equipment ADD COLUMN {col_name} {col_def}")
                        print(f"✅ Добавлена колонка {col_name} в equipment")
                    except Exception as e:
                        print(f"⚠️ Не удалось добавить колонку {col_name}: {e}")

            conn.commit()
        except Exception as e:
            print(f"⚠️ Ошибка при добавлении колонок: {e}")
        finally:
            conn.close()

    def hard_reset_database(self):
        """Полный сброс базы данных - удаляет все данные и создает заново"""
        try:
            print("\n" + "="*60)
            print("⚠️ ВНИМАНИЕ: Полный сброс базы данных!")
            print("="*60)

            conn = self.get_connection()
            cursor = conn.cursor()

            # Удаляем все данные из всех таблиц в правильном порядке (сначала зависимые)
            tables = [
                'inventory_log', 'reports', 'room_markers', 'floor_maps',
                'equipment', 'arrivals', 'room', 'environment',
                'employees', 'branches', 'company', 'users'
            ]

            for table in tables:
                try:
                    cursor.execute(f"DELETE FROM {table}")
                    print(f"   ✅ Очищена таблица: {table}")
                except Exception as e:
                    print(f"   ⚠️ Не удалось очистить {table}: {e}")

            # Сбрасываем автоинкремент
            for table in tables:
                try:
                    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
                except:
                    pass

            conn.commit()
            conn.close()

            print("✅ База данных полностью очищена!")

            # Добавляем тестовые данные
            self.check_and_add_default_data()

            print("✅ Тестовые данные добавлены!")
            return True

        except Exception as e:
            print(f"❌ Ошибка при сбросе БД: {e}")
            return False

    def check_and_add_default_data(self):
        """Проверяет и добавляет данные по умолчанию если БД пуста"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ("admin", "admin", "admin"))
            print("✅ Добавлен пользователь admin")

        cursor.execute("SELECT COUNT(*) FROM branches")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO branches (name, floors_count, address) VALUES (?, ?, ?)",
                           ("Главный офис", 3, "г. Москва, ул. Ленина, 1"))
            branch_id = cursor.lastrowid

            cursor.execute("""
                           INSERT INTO employees (name_id, job_title, report_count, date_of_work, branch_id)
                           VALUES (?, ?, ?, ?, ?)
                           """, ("Иванов Иван Иванович", "Директор", 0, datetime.now().strftime("%Y-%m-%d"), branch_id))

            cursor.execute("""
                           INSERT INTO room (room_number, room_name, branch_id, floor, capacity, desks_count, chairs_count)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           """, ("101", "Кабинет директора", branch_id, 1, 5, 1, 5))

            print("✅ Добавлены тестовые данные")

        conn.commit()
        conn.close()

    # ==================== ВСЕ ОСТАЛЬНЫЕ МЕТОДЫ (без изменений) ====================

    def get_all_branches(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT branch_id, name, floors_count, address FROM branches ORDER BY name")
        branches = cursor.fetchall()
        conn.close()
        return branches

    def get_branch(self, branch_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT branch_id, name, floors_count, address FROM branches WHERE branch_id = ?", (branch_id,))
        branch = cursor.fetchone()
        conn.close()
        return branch

    def add_branch(self, name, floors_count=1, address=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO branches (name, floors_count, address) VALUES (?, ?, ?)",
                       (name, floors_count, address))
        branch_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return branch_id

    def update_branch(self, branch_id, name, floors_count, address):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE branches SET name = ?, floors_count = ?, address = ? WHERE branch_id = ?",
                       (name, floors_count, address, branch_id))
        conn.commit()
        conn.close()

    def delete_branch(self, branch_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM branches WHERE branch_id = ?", (branch_id,))
        conn.commit()
        conn.close()

    def get_employees(self, branch_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if branch_id:
            cursor.execute("""
                           SELECT worker_id, name_id, job_title, report_count, date_of_work
                           FROM employees
                           WHERE branch_id = ?
                           ORDER BY name_id
                           """, (branch_id,))
        else:
            cursor.execute("""
                           SELECT worker_id, name_id, job_title, report_count, date_of_work
                           FROM employees
                           ORDER BY name_id
                           """)
        employees = cursor.fetchall()
        conn.close()
        return employees

    def get_employee_by_id(self, employee_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT worker_id, name_id, job_title, report_count, date_of_work, phone, email, branch_id
                           FROM employees
                           WHERE worker_id = ?
                           """, (employee_id,))
            employee = cursor.fetchone()
            return employee
        except Exception as e:
            print(f"Ошибка получения сотрудника: {e}")
            return None
        finally:
            conn.close()

    def add_employee(self, name, job_title, date_of_work, branch_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO employees (name_id, job_title, report_count, date_of_work, branch_id)
                       VALUES (?, ?, ?, ?, ?)
                       """, (name, job_title, 0, date_of_work, branch_id))
        employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return employee_id

    def update_employee(self, worker_id, name, job_title, date_of_work):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE employees
                       SET name_id = ?, job_title = ?, date_of_work = ?
                       WHERE worker_id = ?
                       """, (name, job_title, date_of_work, worker_id))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def delete_employee(self, employee_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE worker_id = ?", (employee_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def get_all_rooms(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT room_id, room_number, room_name, floor, branch_id,
                              capacity, desks_count, chairs_count, sockets_count, area
                       FROM room
                       ORDER BY room_number
                       """)
        rooms = cursor.fetchall()
        conn.close()
        return rooms

    def get_rooms_by_branch(self, branch_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT room_id, room_number, room_name, floor, capacity,
                              desks_count, chairs_count, sockets_count, area, responsible_employee_id, notes
                       FROM room
                       WHERE branch_id = ?
                       ORDER BY floor, room_number
                       """, (branch_id,))
        rooms = cursor.fetchall()
        conn.close()
        return rooms

    def get_rooms(self, branch_id=None):
        return self.get_rooms_by_branch(branch_id)

    def get_rooms_by_branch_and_floor(self, branch_id, floor):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT room_id, room_number, room_name, capacity
                           FROM room
                           WHERE branch_id = ? AND floor = ?
                           ORDER BY room_number
                           """, (branch_id, floor))
            rooms = cursor.fetchall()
            return rooms
        except Exception as e:
            print(f"Ошибка загрузки комнат: {e}")
            return []
        finally:
            conn.close()

    def get_room(self, room_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT
                           room_id, room_number, room_name, floor, capacity,
                           desks_count, chairs_count, sockets_count, area,
                           responsible_employee_id, notes, branch_id
                       FROM room
                       WHERE room_id = ?
                       """, (room_id,))
        room = cursor.fetchone()
        conn.close()
        return room

    def add_room(self, room_number, room_name, branch_id=None, floor=1,
                 capacity=0, desks_count=0, chairs_count=0, sockets_count=0,
                 area=0.0, responsible_id=None, notes=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO room (
                           room_number, room_name, branch_id, floor,
                           capacity, desks_count, chairs_count, sockets_count,
                           area, responsible_employee_id, notes
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, (
                           room_number, room_name, branch_id, floor,
                           capacity, desks_count, chairs_count, sockets_count,
                           area, responsible_id, notes
                       ))
        room_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return room_id

    def update_room(self, room_id, room_number, room_name, floor=1,
                    capacity=0, desks_count=0, chairs_count=0, sockets_count=0,
                    area=0.0, responsible_id=None, notes=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE room SET
                                       room_number = ?,
                                       room_name = ?,
                                       floor = ?,
                                       capacity = ?,
                                       desks_count = ?,
                                       chairs_count = ?,
                                       sockets_count = ?,
                                       area = ?,
                                       responsible_employee_id = ?,
                                       notes = ?
                       WHERE room_id = ?
                       """, (
                           room_number, room_name, floor,
                           capacity, desks_count, chairs_count,
                           sockets_count, area, responsible_id,
                           notes, room_id
                       ))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def delete_room(self, room_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE equipment SET room_id = NULL WHERE room_id = ?", (room_id,))
        cursor.execute("DELETE FROM room WHERE room_id = ?", (room_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def get_all_equipment(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT equipment_id, name, category, type, serial_number, status, quantity, room_id
                           FROM equipment
                           ORDER BY name
                           """)
            equipment = cursor.fetchall()
            return equipment
        except Exception as e:
            print(f"Ошибка загрузки оборудования: {e}")
            return []
        finally:
            conn.close()

    def get_equipment_by_room(self, room_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT equipment_id, name, category, type, serial_number, status, quantity
                           FROM equipment
                           WHERE room_id = ?
                           ORDER BY name
                           """, (room_id,))
            equipment = cursor.fetchall()
            return equipment
        except Exception as e:
            print(f"Ошибка загрузки оборудования: {e}")
            return []
        finally:
            conn.close()

    def get_equipment_for_distribution(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT
                               equipment_id, name, category, type, model, manufacturer,
                               serial_number, inventory_number, quantity, price, date_incoming,
                               supplier, status
                           FROM equipment
                           WHERE room_id IS NULL OR room_id = 0
                           ORDER BY name
                           """)
            equipment = cursor.fetchall()
            return equipment
        except Exception as e:
            print(f"Ошибка загрузки оборудования: {e}")
            return []
        finally:
            conn.close()

    def get_equipment_by_id(self, equipment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT equipment_id, name, category, type, model, manufacturer,
                                  serial_number, inventory_number, quantity, price,
                                  date_incoming, supplier, phone_supplier, email_supplier,
                                  status, notes, room_id, branch_id
                           FROM equipment
                           WHERE equipment_id = ?
                           """, (equipment_id,))
            equipment = cursor.fetchone()
            return equipment
        except Exception as e:
            print(f"Ошибка получения оборудования: {e}")
            return None
        finally:
            conn.close()

    def add_equipment(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           INSERT INTO equipment (
                               name, category, type, quantity, serial_number,
                               supplier, price, date_incoming,
                               phone_supplier, email_supplier, status, notes,
                               inventory_number, model, manufacturer
                           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           """, (
                               data.get('name', ''),
                               data.get('category', ''),
                               data.get('type', ''),
                               data.get('quantity', 1),
                               data.get('serial_number', ''),
                               data.get('supplier', ''),
                               data.get('price', 0),
                               data.get('date_incoming', datetime.now().strftime("%Y-%m-%d")),
                               data.get('phone_supplier', ''),
                               data.get('email_supplier', ''),
                               data.get('status', 'in_use'),
                               data.get('notes', ''),
                               data.get('inventory_number', ''),
                               data.get('model', ''),
                               data.get('manufacturer', '')
                           ))
            equip_id = cursor.lastrowid
            conn.commit()
            return equip_id
        except Exception as e:
            print(f"Ошибка добавления оборудования: {e}")
            return None
        finally:
            conn.close()

    def update_equipment_room(self, equipment_id, room_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE equipment SET room_id = ? WHERE equipment_id = ?",
                           (room_id, equipment_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка обновления оборудования: {e}")
            return False
        finally:
            conn.close()

    def reset_equipment_to_stock(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE equipment SET room_id = NULL, workplace_number = NULL")
            affected = cursor.rowcount
            conn.commit()
            return affected
        except Exception as e:
            print(f"Ошибка сброса: {e}")
            return 0
        finally:
            conn.close()

    def get_company_name(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM company LIMIT 1")
            result = cursor.fetchone()
            return result['name'] if result else "ГБОУ Больница 2 г. Апшеронск"
        except:
            return "ГБОУ Больница 2 г. Апшеронск"
        finally:
            conn.close()

    def save_company_name(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM company")
            cursor.execute("INSERT INTO company (name) VALUES (?)", (name,))
            conn.commit()
        except Exception as e:
            print(f"Ошибка сохранения названия: {e}")
        finally:
            conn.close()

    def get_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT username, role FROM users")
            users = cursor.fetchall()
            return users
        except:
            return []
        finally:
            conn.close()

    def change_password(self, username, new_password):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
            conn.commit()
            success = True
        except:
            success = False
        conn.close()
        return success

    def authenticate_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id, username, role FROM users WHERE username = ? AND password = ?",
                           (username, password))
            user = cursor.fetchone()
            return user
        except:
            return None
        finally:
            conn.close()

    def add_report(self, report_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           INSERT INTO reports (
                               report_name, report_date, description, order_number,
                               worker_id, environment_id
                           ) VALUES (?, ?, ?, ?, ?, ?)
                           """, (
                               report_data.get('name', ''),
                               report_data.get('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                               report_data.get('description', ''),
                               report_data.get('order_number', 0),
                               report_data.get('worker_id'),
                               report_data.get('environment_id')
                           ))
            report_id = cursor.lastrowid
            conn.commit()
            return report_id
        except Exception as e:
            print(f"Ошибка добавления отчета: {e}")
            return None
        finally:
            conn.close()

    def get_all_reports(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT report_id, report_name, report_date, description, order_number
                           FROM reports
                           ORDER BY report_date DESC
                           """)
            reports = cursor.fetchall()
            return reports
        except Exception as e:
            print(f"Ошибка загрузки отчетов: {e}")
            return []
        finally:
            conn.close()

    def get_report(self, report_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT report_id, report_name, report_date, description, order_number,
                                  worker_id, environment_id
                           FROM reports
                           WHERE report_id = ?
                           """, (report_id,))
            report = cursor.fetchone()
            return report
        except Exception as e:
            print(f"Ошибка загрузки отчета: {e}")
            return None
        finally:
            conn.close()

    def save_floor_map(self, branch_id, floor_num, img_path):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO floor_maps (branch_id, floor_number, image_path)
                VALUES (?, ?, ?)
            """, (branch_id, floor_num, img_path))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def add_marker(self, map_id, room_id, x, y):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO room_markers (map_id, room_id, x, y)
                VALUES (?, ?, ?, ?)
            """, (map_id, room_id, x, y))
            conn.commit()
        finally:
            conn.close()

    def get_map_data(self, branch_id, floor_num):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT map_id, image_path FROM floor_maps WHERE branch_id = ? AND floor_number = ?",
                           (branch_id, floor_num))
            map_info = cursor.fetchone()
            if not map_info:
                return None, []
            cursor.execute("""
                           SELECT rm.x, rm.y, rm.room_id, r.room_name, r.room_number
                           FROM room_markers rm
                                    JOIN room r ON rm.room_id = r.room_id
                           WHERE rm.map_id = ?
                           """, (map_info['map_id'],))
            markers = cursor.fetchall()
            return map_info, markers
        finally:
            conn.close()

    def delete_markers_by_map(self, map_id):
        conn = self.get_connection()
        conn.execute("DELETE FROM room_markers WHERE map_id = ?", (map_id,))
        conn.commit()
        conn.close()

    def delete_full_map(self, map_id):
        conn = self.get_connection()
        conn.execute("DELETE FROM floor_maps WHERE map_id = ?", (map_id,))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    db = DatabaseHandler()
    print("\n✅ DatabaseHandler готов к работе!")