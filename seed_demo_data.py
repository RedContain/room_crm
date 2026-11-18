"""Add a small, clearly labeled demo dataset without clearing existing data."""

from datetime import date
import sys

from database_handler import DatabaseHandler

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


DEMO_BRANCHES = (
    ("ДЕМО — Северный учебный филиал", 2, "Демонстрационный адрес, корпус 1"),
    ("ДЕМО — Южный учебный филиал", 2, "Демонстрационный адрес, корпус 2"),
)

ROOMS = (
    ("ДЕМО-101", "Демо кабинет администрации", 1, 10, 4, 8, 12, 28.5),
    ("ДЕМО-102", "Демо серверная", 1, 4, 0, 0, 8, 12.0),
    ("ДЕМО-201", "Демо склад", 2, 2, 0, 0, 4, 18.0),
)

EQUIPMENT = (
    ("Демо ноутбук", "Электроника", "Ноутбук", "DEMO-NB-14", "ДемоТех", 2, 385000.0),
    ("Демо принтер", "Оргтехника", "Принтер", "DEMO-PR-01", "ДемоТех", 1, 92000.0),
    ("Демо сервер", "Сетевое оборудование", "Сервер", "DEMO-SRV-01", "ДемоТех", 1, 540000.0),
    ("Демо коммутатор", "Сетевое оборудование", "Коммутатор", "DEMO-SW-24", "ДемоТех", 1, 78000.0),
    ("Демо стол", "Мебель", "Стол", "DEMO-DESK-01", "ДемоМебель", 2, 24000.0),
    ("Демо шкаф", "Мебель", "Шкаф", "DEMO-CAB-01", "ДемоМебель", 1, 31500.0),
)


def seed_demo_data():
    db = DatabaseHandler()
    added = {"branches": 0, "employees": 0, "rooms": 0, "equipment": 0, "arrivals": 0}
    branch_records = []
    employee_records = {}
    room_records = {}

    with db.get_connection() as conn:
        for branch_index, (branch_name, floors, address) in enumerate(DEMO_BRANCHES, start=1):
            branch = conn.execute(
                "SELECT branch_id FROM branches WHERE name = ?", (branch_name,)
            ).fetchone()
            if branch:
                branch_id = branch["branch_id"]
            else:
                cursor = conn.execute(
                    "INSERT INTO branches (name, floors_count, address) VALUES (?, ?, ?)",
                    (branch_name, floors, address),
                )
                branch_id = cursor.lastrowid
                added["branches"] += 1
            branch_records.append((branch_index, branch_id, branch_name))

            employees = []
            for employee_index, (employee_name, job_title) in enumerate((
                (f"ДЕМО — Сотрудник филиала {branch_index} №1", "Демо администратор"),
                (f"ДЕМО — Сотрудник филиала {branch_index} №2", "Демо системный специалист"),
            ), start=1):
                employee = conn.execute(
                    "SELECT worker_id FROM employees WHERE name_id = ? AND branch_id = ?",
                    (employee_name, branch_id),
                ).fetchone()
                if employee:
                    employee_id = employee["worker_id"]
                else:
                    cursor = conn.execute(
                        """INSERT INTO employees
                           (name_id, job_title, report_count, date_of_work, branch_id)
                           VALUES (?, ?, 0, ?, ?)""",
                        (employee_name, job_title, date.today().isoformat(), branch_id),
                    )
                    employee_id = cursor.lastrowid
                    added["employees"] += 1
                employees.append(employee_id)
            employee_records[branch_id] = employees

            rooms = []
            for room_number, room_name, floor, capacity, desks, chairs, sockets, area in ROOMS:
                room = conn.execute(
                    """SELECT room_id FROM room
                       WHERE branch_id = ? AND room_number = ? AND room_name = ?""",
                    (branch_id, room_number, room_name),
                ).fetchone()
                if room:
                    room_id = room["room_id"]
                else:
                    cursor = conn.execute(
                        """INSERT INTO room
                           (room_number, room_name, branch_id, floor, capacity, desks_count,
                            chairs_count, sockets_count, area, responsible_employee_id, notes)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (room_number, room_name, branch_id, floor, capacity, desks, chairs,
                         sockets, area, employees[0], "ДЕМО: помещение для проверки интерфейса"),
                    )
                    room_id = cursor.lastrowid
                    added["rooms"] += 1
                rooms.append((room_id, room_number, room_name, floor))
            room_records[branch_id] = rooms

        serial_index = 1
        for branch_index, branch_id, branch_name in branch_records:
            rooms = room_records[branch_id]
            for room_index, room in enumerate(rooms):
                room_id, room_number, room_name, floor = room
                equipment_pair = EQUIPMENT[room_index * 2:room_index * 2 + 2]
                for name, category, type_name, model, manufacturer, quantity, price in equipment_pair:
                    serial_number = f"DEMO-SN-{serial_index:04d}"
                    inventory_number = f"DEMO-INV-{serial_index:04d}"
                    exists = conn.execute(
                        "SELECT equipment_id FROM equipment WHERE serial_number = ?",
                        (serial_number,),
                    ).fetchone()
                    if not exists:
                        conn.execute(
                            """INSERT INTO equipment
                               (name, category, type, model, manufacturer, quantity, serial_number,
                                inventory_number, price, date_incoming, supplier, phone_supplier,
                                email_supplier, status, notes, room_id, branch_id)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?, 'in_use', ?, ?, ?)""",
                            (name, category, type_name, model, manufacturer, quantity,
                             serial_number, inventory_number, price, date.today().isoformat(),
                             "ДЕМО — Поставщик", "demo@example.invalid",
                             f"ДЕМО: оборудование в помещении {room_number}", room_id, branch_id),
                        )
                        added["equipment"] += 1
                    serial_index += 1

            order_number = f"DEMO-ARR-{branch_index:02d}"
            total_amount = sum(item[5] * item[6] for item in EQUIPMENT)
            arrival = conn.execute(
                "SELECT arrival_id FROM arrivals WHERE order_number = ?", (order_number,)
            ).fetchone()
            if not arrival:
                conn.execute(
                    """INSERT INTO arrivals
                       (name, order_number, description, branch_id, employee_id, date, doc_number,
                        supplier_name, supplier_inn, supplier_phone, supplier_email, total_amount,
                        waybill_number, contract_number, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"ДЕМО — Поступление филиала {branch_index}", order_number,
                     f"Демонстрационная запись поступления для: {branch_name}", branch_id,
                     employee_records[branch_id][0], date.today().isoformat(),
                     f"DEMO-DOC-{branch_index:02d}", "ДЕМО — Поставщик", "DEMO-INN",
                     "", "demo@example.invalid", total_amount,
                     f"DEMO-WAYBILL-{branch_index:02d}", f"DEMO-CONTRACT-{branch_index:02d}",
                     "ДЕМО: запись создана автоматически для проверки программы"),
                )
                added["arrivals"] += 1

        stock_items = (
            ("Демо монитор на складе", "Электроника", "Монитор", "DEMO-MON-01", "ДемоТех", 3, 68000.0),
            ("Демо мышь на складе", "Комплектующие", "Мышь", "DEMO-MOUSE-01", "ДемоТех", 5, 1800.0),
            ("Демо кресло на складе", "Мебель", "Кресло", "DEMO-CHAIR-01", "ДемоМебель", 2, 28500.0),
        )
        stock_branch_id = branch_records[0][1]
        for index, (name, category, type_name, model, manufacturer, quantity, price) in enumerate(stock_items, start=1):
            serial_number = f"DEMO-STOCK-{index:04d}"
            exists = conn.execute(
                "SELECT equipment_id FROM equipment WHERE serial_number = ?", (serial_number,)
            ).fetchone()
            if not exists:
                conn.execute(
                    """INSERT INTO equipment
                       (name, category, type, model, manufacturer, quantity, serial_number,
                        inventory_number, price, date_incoming, supplier, phone_supplier,
                        email_supplier, status, notes, room_id, branch_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?, 'in_stock', ?, NULL, ?)""",
                    (name, category, type_name, model, manufacturer, quantity,
                     serial_number, f"DEMO-INV-STOCK-{index:02d}", price,
                     date.today().isoformat(), "ДЕМО — Поставщик", "demo@example.invalid",
                     "ДЕМО: демонстрационный остаток на складе", stock_branch_id),
                )
                added["equipment"] += 1

    conn.close()
    return added


if __name__ == "__main__":
    counts = seed_demo_data()
    print("Добавлены демонстрационные записи (существующие данные сохранены):")
    for entity, count in counts.items():
        print(f"  {entity}: {count}")
