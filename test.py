#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для заполнения базы данных тестовыми данными
Запуск: python test.py
"""

import sys
import os
from datetime import datetime, timedelta
import random
import uuid

# Добавляем путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from database_handler import DatabaseHandler


class TestDataGenerator:
    def __init__(self):
        self.db = DatabaseHandler()
        print("=" * 60)
        print("ГЕНЕРАТОР ТЕСТОВЫХ ДАННЫХ")
        print("=" * 60)

    def clear_all_data(self):
        """Очищает все таблицы перед заполнением"""
        print("\n🗑️  Очистка существующих данных...")
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Порядок важен из-за внешних ключей
        tables = [
            'room_markers', 'floor_maps', 'inventory_log', 'reports',
            'arrivals', 'equipment', 'room', 'employees', 'branches', 'users'
        ]

        for table in tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   Очищена таблица: {table}")
            except Exception as e:
                print(f"   Ошибка очистки {table}: {e}")

        conn.commit()
        conn.close()
        print("✅ База данных очищена")

    def generate_branches(self):
        """Генерирует филиалы"""
        print("\n🏢 Генерация филиалов...")
        branches = [
            ("Главный офис", 5, "г. Москва, ул. Тверская, д. 1"),
            ("Северный филиал", 3, "г. Санкт-Петербург, Невский пр., д. 25"),
            ("Южный филиал", 4, "г. Краснодар, ул. Красная, д. 10"),
            ("Восточный филиал", 2, "г. Казань, ул. Баумана, д. 15"),
            ("Западный филиал", 3, "г. Калининград, пр. Мира, д. 8"),
        ]

        branch_ids = []
        for name, floors, address in branches:
            branch_id = self.db.add_branch(name, floors, address)
            branch_ids.append(branch_id)
            print(f"   ✅ Добавлен филиал: {name} (ID: {branch_id}, этажей: {floors})")

        return branch_ids

    def generate_employees(self, branch_ids):
        """Генерирует сотрудников"""
        print("\n👥 Генерация сотрудников...")

        positions = [
            "Директор", "Заместитель директора", "Главный бухгалтер", "Бухгалтер",
            "Начальник отдела", "Инженер", "Системный администратор", "Менеджер",
            "Администратор", "Секретарь", "Кладовщик", "Электрик", "Уборщик",
            "Охранник", "Водитель"
        ]

        first_names = ["Иван", "Петр", "Сергей", "Алексей", "Дмитрий", "Александр",
                       "Михаил", "Андрей", "Владимир", "Николай", "Елена", "Мария",
                       "Ольга", "Анна", "Татьяна", "Светлана", "Наталья", "Ирина"]

        last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Волков",
                      "Соколов", "Лебедев", "Козлов", "Новиков", "Морозов", "Попов",
                      "Васильева", "Петрова", "Сидорова", "Кузнецова", "Смирнова"]

        employees = []
        start_date = datetime.now() - timedelta(days=365)

        for branch_id in branch_ids:
            # Для каждого филиала создаем от 5 до 15 сотрудников
            num_employees = random.randint(5, 15)

            for i in range(num_employees):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                name = f"{first_name} {last_name}"
                position = random.choice(positions)

                # Случайная дата трудоустройства (от 1 до 365 дней назад)
                days_ago = random.randint(1, 365)
                hire_date = (start_date + timedelta(days=days_ago)).strftime("%Y-%m-%d")

                employee_id = self.db.add_employee(name, position, hire_date, branch_id)
                employees.append({
                    'id': employee_id,
                    'name': name,
                    'position': position,
                    'branch_id': branch_id
                })
                print(f"   ✅ Добавлен сотрудник: {name} ({position}) в филиал {branch_id}")

        print(f"   Всего добавлено сотрудников: {len(employees)}")
        return employees

    def generate_rooms(self, branch_ids):
        """Генерирует комнаты"""
        print("\n🚪 Генерация комнат...")

        room_names = [
            "Кабинет директора", "Переговорная", "Бухгалтерия", "Отдел кадров",
            "Серверная", "Архив", "Склад", "Кладовка", "Столовая", "Кухня",
            "Туалет", "Коридор", "Холл", "Конференц-зал", "Учебный класс",
            "Лаборатория", "Мастерская", "Гардероб", "Душевая", "Тренажерный зал"
        ]

        room_numbers = []
        for i in range(1, 101):
            room_numbers.append(str(i).zfill(3))

        rooms = []

        for branch_id in branch_ids:
            # Получаем количество этажей в филиале
            branch = self.db.get_branch(branch_id)
            floors_count = branch['floors_count'] if branch else 3

            # Для каждого этажа создаем от 5 до 15 комнат
            for floor in range(1, floors_count + 1):
                num_rooms = random.randint(5, 15)

                for i in range(num_rooms):
                    room_number = random.choice(room_numbers)
                    room_name = random.choice(room_names)

                    # Случайные параметры комнаты
                    capacity = random.randint(1, 50)
                    desks = random.randint(0, capacity // 2)
                    chairs = random.randint(desks, desks * 2)
                    sockets = random.randint(desks, desks * 3)
                    area = round(random.uniform(10, 100), 1)

                    room_id = self.db.add_room(
                        room_number=room_number,
                        room_name=room_name,
                        branch_id=branch_id,
                        floor=floor,
                        capacity=capacity,
                        desks_count=desks,
                        chairs_count=chairs,
                        sockets_count=sockets,
                        area=area
                    )

                    rooms.append({
                        'id': room_id,
                        'number': room_number,
                        'name': room_name,
                        'branch_id': branch_id,
                        'floor': floor
                    })
                    print(f"   ✅ Добавлена комната: {room_number} - {room_name} (этаж {floor}) в филиал {branch_id}")

        print(f"   Всего добавлено комнат: {len(rooms)}")
        return rooms

    def generate_equipment(self, rooms, employees):
        """Генерирует оборудование"""
        print("\n💻 Генерация оборудования...")

        equipment_categories = [
            ("Электроника", [
                "Телевизор", "Монитор", "Ноутбук", "Планшет", "Смартфон",
                "Проектор", "Интерактивная доска", "Принтер", "Сканер", "МФУ"
            ]),
            ("Комплектующие", [
                "Процессор", "Материнская плата", "Оперативная память",
                "Видеокарта", "SSD диск", "HDD диск", "Блок питания",
                "Системный блок", "Кулер", "Wi-Fi адаптер"
            ]),
            ("Сетевое оборудование", [
                "Маршрутизатор", "Коммутатор", "Медиаконвертер",
                "Wi-Fi точка доступа", "Сервер", "Сетевая карта",
                "Патч-панель", "Розетка RJ-45", "Оптический модуль"
            ]),
            ("Мебель", [
                "Стол", "Стул", "Кресло", "Шкаф", "Тумба",
                "Стеллаж", "Полка", "Вешалка", "Диван", "Кушетка"
            ]),
            ("Оргтехника", [
                "Калькулятор", "Ламинатор", "Брошюровщик", "Резак",
                "Уничтожитель бумаги", "Телефон", "Факс", "Диктофон"
            ]),
            ("Инструменты", [
                "Отвертка", "Молоток", "Дрель", "Шуруповерт",
                "Перфоратор", "Пассатижи", "Мультиметр", "Паяльник"
            ])
        ]

        manufacturers = [
            "Samsung", "LG", "Sony", "HP", "Dell", "Lenovo", "Apple",
            "Asus", "Acer", "MSI", "Intel", "AMD", "Cisco", "TP-Link",
            "Ikea", "Hoff", "Bosch", "Makita", "Stanley"
        ]

        suppliers = [
            "ООО ТехноПарк", "ИП Иванов", "ООО Компьютерный мир",
            "ЗАО ОфисСнаб", "ООО МебельПро", "ИП Петров",
            "ООО ЭлектроТорг", "ЗАО СтройМаркет", "ООО ХозТовары"
        ]

        # Список статусов
        statuses = ['in_use', 'in_stock', 'written_off']

        equipment_list = []
        equipment_counter = 0

        # Генерируем оборудование для каждой комнаты
        for room in rooms:
            # В каждой комнате от 5 до 30 предметов
            num_items = random.randint(5, 30)

            for i in range(num_items):
                category_data = random.choice(equipment_categories)
                category = category_data[0]
                type_name = random.choice(category_data[1])

                # Генерируем название
                if random.choice([True, False]):
                    name = f"{type_name} {random.choice(manufacturers)}"
                else:
                    name = type_name

                # Количество
                quantity = random.randint(1, 10)

                # Серийный номер (уникальный)
                serial = f"{type_name[:3].upper()}-{random.randint(10000, 99999)}-{uuid.uuid4().hex[:6].upper()}"

                # Инвентарный номер
                equipment_counter += 1
                inventory = f"INV-{datetime.now().year}-{equipment_counter:05d}"

                # Цена
                if category in ["Электроника", "Комплектующие", "Сетевое оборудование"]:
                    price = random.randint(1000, 100000)
                elif category == "Мебель":
                    price = random.randint(2000, 50000)
                else:
                    price = random.randint(100, 20000)

                # Дата поступления (от 1 до 365 дней назад)
                days_ago = random.randint(1, 365)
                date_incoming = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

                # Производитель
                manufacturer = random.choice(manufacturers)

                # Модель
                model = f"{type_name[:2].upper()}-{random.randint(100, 999)}"

                # Поставщик
                supplier = random.choice(suppliers)

                # Статус (в основном в использовании)
                status = random.choice(statuses)

                equipment_data = {
                    'name': name,
                    'category': category,
                    'type': type_name,
                    'model': model,
                    'manufacturer': manufacturer,
                    'quantity': quantity,
                    'serial_number': serial,
                    'inventory_number': inventory,
                    'price': price,
                    'date_incoming': date_incoming,
                    'supplier': supplier,
                    'phone_supplier': f"+7(9{random.randint(10, 99)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                    'email_supplier': f"info@{supplier.replace(' ', '').lower()}.ru",
                    'status': status,
                    'notes': f"Тестовое оборудование, создано {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    'room_id': room['id']
                }

                # Добавляем оборудование
                eq_id = self.db.add_equipment(equipment_data)

                if eq_id:
                    equipment_list.append({
                        'id': eq_id,
                        'name': name,
                        'category': category,
                        'type': type_name,
                        'room_id': room['id'],
                        'room_name': f"{room['number']} - {room['name']}",
                        'price': price,
                        'quantity': quantity
                    })

                    if len(equipment_list) % 50 == 0:
                        print(f"   📦 Создано {len(equipment_list)} единиц оборудования...")
                else:
                    print(f"   ⚠️ Ошибка добавления оборудования: {name}")

        # Добавляем немного оборудования на склад (без комнаты)
        warehouse_items = random.randint(10, 30)
        for i in range(warehouse_items):
            category_data = random.choice(equipment_categories)
            category = category_data[0]
            type_name = random.choice(category_data[1])

            equipment_counter += 1
            name = f"{type_name} (Склад) {random.choice(manufacturers)}"
            quantity = random.randint(1, 5)
            serial = f"STOCK-{random.randint(10000, 99999)}-{uuid.uuid4().hex[:6].upper()}"
            inventory = f"INV-{datetime.now().year}-{equipment_counter:05d}"
            price = random.randint(100, 50000)
            date_incoming = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")

            equipment_data = {
                'name': name,
                'category': category,
                'type': type_name,
                'model': f"{type_name[:2].upper()}-{random.randint(100, 999)}",
                'manufacturer': random.choice(manufacturers),
                'quantity': quantity,
                'serial_number': serial,
                'inventory_number': inventory,
                'price': price,
                'date_incoming': date_incoming,
                'supplier': random.choice(suppliers),
                'phone_supplier': f"+7(9{random.randint(10, 99)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                'email_supplier': f"info@{random.choice(suppliers).replace(' ', '').lower()}.ru",
                'status': 'in_stock',
                'notes': "Оборудование на складе",
                'room_id': None  # Без комнаты
            }

            eq_id = self.db.add_equipment(equipment_data)

            if eq_id:
                equipment_list.append({
                    'id': eq_id,
                    'name': name,
                    'category': category,
                    'type': type_name,
                    'room_id': None,
                    'room_name': "Склад",
                    'price': price,
                    'quantity': quantity
                })

        print(f"   Всего добавлено оборудования: {len(equipment_list)}")
        return equipment_list

    def generate_arrivals(self, employees, equipment_list):
        """Генерирует записи о поступлениях"""
        print("\n📦 Генерация поступлений...")

        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Берем первые 50 единиц оборудования для создания поступлений
        arrivals_count = min(50, len(equipment_list))

        for i in range(arrivals_count):
            eq = equipment_list[i]

            # Выбираем случайного сотрудника
            employee = random.choice(employees)

            # Генерируем данные поступления
            arrival_data = {
                'name': f"Поступление №{i+1:03d} - {eq['name']}",
                'order_number': f"ПР-{datetime.now().year}-{random.randint(1000, 9999)}",
                'description': f"Поступление оборудования: {eq['name']}",
                'branch_id': employee['branch_id'],
                'employee_id': employee['id'],
                'date': (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d %H:%M:%S"),
                'doc_number': f"ДС-{random.randint(10000, 99999)}",
                'supplier_name': random.choice(["ООО ТехноПарк", "ИП Иванов", "ООО Компьютерный мир"]),
                'supplier_inn': f"{random.randint(1000000000, 9999999999)}",
                'supplier_phone': f"+7(9{random.randint(10, 99)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                'supplier_email': f"supplier{random.randint(1, 100)}@example.ru",
                'total_amount': eq.get('price', random.randint(1000, 50000)) * eq.get('quantity', 1),
                'waybill_number': f"ТН-{random.randint(10000, 99999)}",
                'contract_number': f"ДГ-{random.randint(1000, 9999)}",
                'notes': f"Тестовое поступление от {datetime.now().strftime('%Y-%m-%d')}"
            }

            try:
                cursor.execute("""
                               INSERT INTO arrivals (
                                   name, order_number, description, branch_id, employee_id, date,
                                   doc_number, supplier_name, supplier_inn, supplier_phone, supplier_email,
                                   total_amount, waybill_number, contract_number, notes
                               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               """, (
                                   arrival_data['name'], arrival_data['order_number'], arrival_data['description'],
                                   arrival_data['branch_id'], arrival_data['employee_id'], arrival_data['date'],
                                   arrival_data['doc_number'], arrival_data['supplier_name'], arrival_data['supplier_inn'],
                                   arrival_data['supplier_phone'], arrival_data['supplier_email'],
                                   arrival_data['total_amount'], arrival_data['waybill_number'],
                                   arrival_data['contract_number'], arrival_data['notes']
                               ))
            except Exception as e:
                print(f"   ⚠️ Ошибка добавления поступления: {e}")

        conn.commit()
        conn.close()

        print(f"   ✅ Добавлено поступлений: {arrivals_count}")

    def generate_users(self):
        """Генерирует пользователей"""
        print("\n👤 Генерация пользователей...")

        users = [
            ("admin", "admin", "admin"),
            ("user1", "123456", "user"),
            ("user2", "123456", "user"),
            ("manager", "manager123", "manager"),
            ("viewer", "viewer123", "viewer")
        ]

        conn = self.db.get_connection()
        cursor = conn.cursor()

        for username, password, role in users:
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (username, password, role))
                print(f"   ✅ Добавлен пользователь: {username} ({role})")
            except Exception as e:
                print(f"   ⚠️ Пользователь {username} уже существует или ошибка: {e}")

        conn.commit()
        conn.close()

    def print_statistics(self):
        """Выводит статистику заполнения базы данных"""
        print("\n" + "=" * 60)
        print("СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 60)

        conn = self.db.get_connection()
        cursor = conn.cursor()

        tables = [
            ('branches', 'филиалов'),
            ('employees', 'сотрудников'),
            ('room', 'комнат'),
            ('equipment', 'единиц оборудования'),
            ('arrivals', 'поступлений'),
            ('users', 'пользователей')
        ]

        for table, name in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   📊 {name.capitalize()}: {count}")

        # Дополнительная статистика по оборудованию
        cursor.execute("SELECT COUNT(*) FROM equipment WHERE room_id IS NULL OR room_id = 0")
        stock_count = cursor.fetchone()[0]
        print(f"   📦 Оборудование на складе: {stock_count}")

        cursor.execute("SELECT COUNT(*) FROM equipment WHERE room_id IS NOT NULL AND room_id != 0")
        room_count = cursor.fetchone()[0]
        print(f"   🚪 Оборудование в комнатах: {room_count}")

        # Статистика по категориям
        cursor.execute("""
                       SELECT category, COUNT(*) as count
                       FROM equipment
                       WHERE category IS NOT NULL AND category != ''
                       GROUP BY category
                       ORDER BY count DESC
                       """)
        categories = cursor.fetchall()
        print("\n   📂 Распределение по категориям:")
        for cat in categories[:5]:  # Показываем топ-5 категорий
            print(f"      - {cat['category']}: {cat['count']}")

        # Общая стоимость оборудования
        cursor.execute("SELECT SUM(price * quantity) FROM equipment")
        total_value = cursor.fetchone()[0]
        if total_value:
            print(f"\n   💰 Общая стоимость оборудования: {total_value:,.2f} руб.")

        conn.close()

    def run(self):
        """Запускает генерацию всех данных"""
        print("\n🚀 Начинаем генерацию тестовых данных...")

        # Очищаем существующие данные
        self.clear_all_data()

        # Генерируем данные
        branch_ids = self.generate_branches()
        employees = self.generate_employees(branch_ids)
        rooms = self.generate_rooms(branch_ids)
        equipment = self.generate_equipment(rooms, employees)
        self.generate_arrivals(employees, equipment)
        self.generate_users()

        # Выводим статистику
        self.print_statistics()

        print("\n" + "=" * 60)
        print("✅ ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        print("\n💡 Теперь можно запускать основное приложение: python report_window.py")


def main():
    generator = TestDataGenerator()
    generator.run()


if __name__ == "__main__":
    main()