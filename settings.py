import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate, QEvent
from PySide6.QtGui import QKeyEvent
import paths
from database_handler import DatabaseHandler
from ui.ui_view import Ui_MainWindow


class EmployeesDialog(QDialog):
    def __init__(self, db, branch_id, branch_name, parent=None):
        super().__init__(parent)
        self.db = db
        self.branch_id = branch_id
        self.branch_name = branch_name
        self.selected_employee_id = None
        self.setWindowTitle(f"Сотрудники филиала: {branch_name}")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Должность", "Отчетов", "Дата приема"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)

        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.job_edit = QLineEdit()
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("ФИО:", self.name_edit)
        form_layout.addRow("Должность:", self.job_edit)
        form_layout.addRow("Дата приема:", self.date_edit)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Добавить")
        self.add_btn.clicked.connect(self.add_employee)
        self.update_btn = QPushButton("✏️ Обновить")
        self.update_btn.clicked.connect(self.update_employee)
        self.update_btn.setEnabled(False)
        self.delete_btn = QPushButton("🗑️ Удалить")
        self.delete_btn.clicked.connect(self.delete_employee)
        self.delete_btn.setEnabled(False)
        close_btn = QPushButton("❌ Закрыть")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.load_employees()

    def load_employees(self):
        employees = self.db.get_employees(self.branch_id)
        self.table.setRowCount(len(employees))
        for i, emp in enumerate(employees):
            self.table.setItem(i, 0, QTableWidgetItem(str(emp[0])))
            self.table.setItem(i, 1, QTableWidgetItem(emp[1]))
            self.table.setItem(i, 2, QTableWidgetItem(emp[2]))
            self.table.setItem(i, 3, QTableWidgetItem(str(emp[3])))
            self.table.setItem(i, 4, QTableWidgetItem(emp[4]))

    def on_row_selected(self, row, column):
        id_item = self.table.item(row, 0)
        if id_item:
            self.selected_employee_id = int(id_item.text())
            self.name_edit.setText(self.table.item(row, 1).text())
            self.job_edit.setText(self.table.item(row, 2).text())
            date_str = self.table.item(row, 4).text()
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if date.isValid():
                self.date_edit.setDate(date)
            self.update_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.add_btn.setText("➕ Добавить (нового)")

    def add_employee(self):
        name = self.name_edit.text().strip()
        job = self.job_edit.text().strip()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        if not name or not job:
            QMessageBox.warning(self, "Ошибка", "Заполните ФИО и должность")
            return

        employee_id = self.db.add_employee(name, job, date, self.branch_id)
        QMessageBox.information(self, "Успех", f"Сотрудник добавлен с ID: {employee_id}")

        self.name_edit.clear()
        self.job_edit.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.selected_employee_id = None
        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.add_btn.setText("➕ Добавить")

        self.load_employees()
        QApplication.processEvents()

        if self.parent() and hasattr(self.parent(), 'refresh_all_rooms_dialogs'):
            self.parent().refresh_all_rooms_dialogs()

    def update_employee(self):
        if not self.selected_employee_id:
            return
        name = self.name_edit.text().strip()
        job = self.job_edit.text().strip()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        if not name or not job:
            QMessageBox.warning(self, "Ошибка", "Заполните ФИО и должность")
            return
        success = self.db.update_employee(self.selected_employee_id, name, job, date)
        if success:
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.selected_employee_id = None
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            self.add_btn.setText("➕ Добавить")
            self.name_edit.clear()
            self.job_edit.clear()
            self.date_edit.setDate(QDate.currentDate())
            self.load_employees()
            QApplication.processEvents()
            if self.parent() and hasattr(self.parent(), 'refresh_all_rooms_dialogs'):
                self.parent().refresh_all_rooms_dialogs()

    def delete_employee(self):
        if not self.selected_employee_id:
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить сотрудника?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            success = self.db.delete_employee(self.selected_employee_id)
            if success:
                QMessageBox.information(self, "Успех", "Сотрудник удален")
                self.selected_employee_id = None
                self.update_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
                self.add_btn.setText("➕ Добавить")
                self.name_edit.clear()
                self.job_edit.clear()
                self.date_edit.setDate(QDate.currentDate())
                self.load_employees()
                QApplication.processEvents()
                if self.parent() and hasattr(self.parent(), 'refresh_all_rooms_dialogs'):
                    self.parent().refresh_all_rooms_dialogs()


class RoomsDialog(QDialog):
    def __init__(self, db, branch_id, branch_name, parent=None):
        super().__init__(parent)
        self.db = db
        self.branch_id = branch_id
        self.branch_name = branch_name
        self.selected_room_id = None
        self.setWindowTitle(f"Комнаты филиала: {branch_name}")
        self.setMinimumSize(1100, 700)

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Номер", "Название", "Этаж", "Вместимость",
            "Столов", "Стульев", "Розеток", "Площадь", "Ответственный"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)

        form_group = QGroupBox("Характеристики комнаты")
        form_layout = QGridLayout(form_group)

        form_layout.addWidget(QLabel("Номер комнаты:"), 0, 0)
        self.number_edit = QLineEdit()
        form_layout.addWidget(self.number_edit, 0, 1)

        form_layout.addWidget(QLabel("Название:"), 1, 0)
        self.name_edit = QLineEdit()
        form_layout.addWidget(self.name_edit, 1, 1)

        form_layout.addWidget(QLabel("Этаж:"), 2, 0)
        self.floor_spin = QSpinBox()
        self.floor_spin.setRange(1, 50)
        form_layout.addWidget(self.floor_spin, 2, 1)

        form_layout.addWidget(QLabel("Вместимость (чел):"), 3, 0)
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(0, 200)
        self.capacity_spin.setSuffix(" чел")
        form_layout.addWidget(self.capacity_spin, 3, 1)

        form_layout.addWidget(QLabel("Количество столов:"), 0, 2)
        self.desks_spin = QSpinBox()
        self.desks_spin.setRange(0, 100)
        self.desks_spin.setSuffix(" шт")
        form_layout.addWidget(self.desks_spin, 0, 3)

        form_layout.addWidget(QLabel("Количество стульев:"), 1, 2)
        self.chairs_spin = QSpinBox()
        self.chairs_spin.setRange(0, 200)
        self.chairs_spin.setSuffix(" шт")
        form_layout.addWidget(self.chairs_spin, 1, 3)

        form_layout.addWidget(QLabel("Количество розеток:"), 2, 2)
        self.sockets_spin = QSpinBox()
        self.sockets_spin.setRange(0, 50)
        self.sockets_spin.setSuffix(" шт")
        form_layout.addWidget(self.sockets_spin, 2, 3)

        form_layout.addWidget(QLabel("Площадь (м²):"), 3, 2)
        self.area_spin = QDoubleSpinBox()
        self.area_spin.setRange(0, 1000)
        self.area_spin.setSuffix(" м²")
        self.area_spin.setSingleStep(0.5)
        form_layout.addWidget(self.area_spin, 3, 3)

        form_layout.addWidget(QLabel("Ответственный сотрудник:"), 4, 0)
        self.responsible_combo = QComboBox()
        form_layout.addWidget(self.responsible_combo, 4, 1, 1, 3)

        form_layout.addWidget(QLabel("Примечания:"), 5, 0)
        self.notes_edit = QLineEdit()
        self.notes_edit.setPlaceholderText("Дополнительная информация о комнате...")
        form_layout.addWidget(self.notes_edit, 5, 1, 1, 3)

        layout.addWidget(form_group)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Добавить")
        self.add_btn.clicked.connect(self.add_room)
        self.update_btn = QPushButton("✏️ Обновить")
        self.update_btn.clicked.connect(self.update_room)
        self.update_btn.setEnabled(False)
        self.delete_btn = QPushButton("🗑️ Удалить")
        self.delete_btn.clicked.connect(self.delete_room)
        self.delete_btn.setEnabled(False)
        close_btn = QPushButton("❌ Закрыть")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.load_responsible_employees()
        self.load_rooms()

        if self.parent() and hasattr(self.parent(), 'register_rooms_dialog'):
            self.parent().register_rooms_dialog(self)

    def closeEvent(self, event):
        if self.parent() and hasattr(self.parent(), 'unregister_rooms_dialog'):
            self.parent().unregister_rooms_dialog(self)
        super().closeEvent(event)

    def load_responsible_employees(self):
        try:
            current_data = self.responsible_combo.currentData()
            self.responsible_combo.blockSignals(True)
            self.responsible_combo.clear()
            self.responsible_combo.addItem("Не назначен", None)

            employees = self.db.get_employees(self.branch_id)
            for emp in employees:
                self.responsible_combo.addItem(f"{emp[1]} ({emp[2]})", emp[0])

            if current_data:
                index = self.responsible_combo.findData(current_data)
                if index >= 0:
                    self.responsible_combo.setCurrentIndex(index)

            self.responsible_combo.blockSignals(False)
        except Exception as e:
            print(f"[RoomsDialog] Ошибка загрузки сотрудников: {e}")

    def load_rooms(self):
        rooms = self.db.get_rooms_by_branch(self.branch_id)
        self.table.setRowCount(len(rooms))
        for i, room in enumerate(rooms):
            self.table.setItem(i, 0, QTableWidgetItem(str(room[0])))
            self.table.setItem(i, 1, QTableWidgetItem(room[1] or ""))
            self.table.setItem(i, 2, QTableWidgetItem(room[2] or ""))
            self.table.setItem(i, 3, QTableWidgetItem(str(room[3] or "1")))
            self.table.setItem(i, 4, QTableWidgetItem(str(room[4] or "0")))
            self.table.setItem(i, 5, QTableWidgetItem(str(room[5] or "0")))
            self.table.setItem(i, 6, QTableWidgetItem(str(room[6] or "0")))
            self.table.setItem(i, 7, QTableWidgetItem(str(room[7] or "0")))
            self.table.setItem(i, 8, QTableWidgetItem(str(room[8] or "0.0")))

            responsible_name = "Не назначен"
            if len(room) > 9 and room[9]:
                responsible = self.db.get_employee_by_id(room[9])
                if responsible:
                    responsible_name = responsible[1]
            self.table.setItem(i, 9, QTableWidgetItem(responsible_name))

    def on_row_selected(self, row, column):
        id_item = self.table.item(row, 0)
        if id_item:
            self.selected_room_id = int(id_item.text())
            self.number_edit.setText(self.table.item(row, 1).text() or "")
            self.name_edit.setText(self.table.item(row, 2).text() or "")
            self.floor_spin.setValue(int(self.table.item(row, 3).text() or "1"))
            self.capacity_spin.setValue(int(self.table.item(row, 4).text() or "0"))
            self.desks_spin.setValue(int(self.table.item(row, 5).text() or "0"))
            self.chairs_spin.setValue(int(self.table.item(row, 6).text() or "0"))
            self.sockets_spin.setValue(int(self.table.item(row, 7).text() or "0"))
            self.area_spin.setValue(float(self.table.item(row, 8).text() or "0.0"))
            responsible_text = self.table.item(row, 9).text()
            found = False
            for idx in range(self.responsible_combo.count()):
                if self.responsible_combo.itemText(idx) == responsible_text:
                    self.responsible_combo.setCurrentIndex(idx)
                    found = True
                    break
            if not found:
                self.responsible_combo.setCurrentIndex(0)
            self.update_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.add_btn.setText("➕ Добавить (новую)")

    def get_form_data(self):
        return {
            'room_number': self.number_edit.text().strip(),
            'room_name': self.name_edit.text().strip(),
            'floor': self.floor_spin.value(),
            'capacity': self.capacity_spin.value(),
            'desks_count': self.desks_spin.value(),
            'chairs_count': self.chairs_spin.value(),
            'sockets_count': self.sockets_spin.value(),
            'area': self.area_spin.value(),
            'responsible_id': self.responsible_combo.currentData(),
            'notes': self.notes_edit.text().strip()
        }

    def add_room(self):
        data = self.get_form_data()
        if not data['room_number'] or not data['room_name']:
            QMessageBox.warning(self, "Ошибка", "Заполните номер и название комнаты")
            return
        try:
            room_id = self.db.add_room(
                room_number=data['room_number'],
                room_name=data['room_name'],
                branch_id=self.branch_id,
                floor=data['floor'],
                capacity=data['capacity'],
                desks_count=data['desks_count'],
                chairs_count=data['chairs_count'],
                sockets_count=data['sockets_count'],
                area=data['area'],
                responsible_id=data['responsible_id'],
                notes=data['notes']
            )
            QMessageBox.information(self, "Успех", f"Комната добавлена с ID: {room_id}")
            self.clear_form()
            self.load_rooms()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить комнату: {e}")

    def update_room(self):
        if not self.selected_room_id:
            return
        data = self.get_form_data()
        if not data['room_number'] or not data['room_name']:
            QMessageBox.warning(self, "Ошибка", "Заполните номер и название комнаты")
            return
        try:
            success = self.db.update_room(
                room_id=self.selected_room_id,
                room_number=data['room_number'],
                room_name=data['room_name'],
                floor=data['floor'],
                capacity=data['capacity'],
                desks_count=data['desks_count'],
                chairs_count=data['chairs_count'],
                sockets_count=data['sockets_count'],
                area=data['area'],
                responsible_id=data['responsible_id'],
                notes=data['notes']
            )
            if success:
                QMessageBox.information(self, "Успех", "Комната обновлена")
                self.selected_room_id = None
                self.update_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
                self.add_btn.setText("➕ Добавить")
                self.clear_form()
                self.load_rooms()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить комнату")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить комнату: {e}")

    def delete_room(self):
        if not self.selected_room_id:
            return
        reply = QMessageBox.question(self, "Подтверждение",
                                     "Удалить комнату? Все связанные данные будут потеряны.",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                success = self.db.delete_room(self.selected_room_id)
                if success:
                    QMessageBox.information(self, "Успех", "Комната удалена")
                    self.selected_room_id = None
                    self.update_btn.setEnabled(False)
                    self.delete_btn.setEnabled(False)
                    self.add_btn.setText("➕ Добавить")
                    self.clear_form()
                    self.load_rooms()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить комнату")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить комнату: {e}")

    def clear_form(self):
        self.number_edit.clear()
        self.name_edit.clear()
        self.floor_spin.setValue(1)
        self.capacity_spin.setValue(0)
        self.desks_spin.setValue(0)
        self.chairs_spin.setValue(0)
        self.sockets_spin.setValue(0)
        self.area_spin.setValue(0.0)
        self.responsible_combo.setCurrentIndex(0)
        self.notes_edit.clear()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = DatabaseHandler()
        self.current_branch_id = None
        self.original_company_name = ""
        self.changes_made = False

        self.open_rooms_dialogs = []

        self.company_name_edit = self.ui.lineEdit
        self.branches_spin = self.ui.spinBox
        self.branches_list = self.ui.listWidget
        self.branch_group = getattr(self.ui, 'groupBox_3', None)
        self.branch_name_edit = self.ui.lineEdit_2
        self.branch_address_edit = self.ui.lineEdit_5
        self.employees_spin = self.ui.spinBox_3
        # В обновленной форме этажи и комнаты поменяли местами.
        self.floors_spin = self.ui.spinBox_2
        self.rooms_spin = self.ui.spinBox_4
        self.save_branch_count_btn = getattr(self.ui, 'pushButton_6', None)
        self.delete_branch_btn = self.ui.pushButton_3
        self.save_branch_btn = getattr(self.ui, 'pushButton_2', None)
        self.save_all_btn = self.ui.pushButton_4
        self.reset_all_btn = self.ui.pushButton_5
        self.employees_btn = self.ui.toolButton_2
        self.rooms_btn = self.ui.toolButton_4

        self.branch_editor_widgets = [
            self.branch_name_edit, self.branch_address_edit, self.employees_spin,
            self.floors_spin, self.rooms_spin, self.employees_btn, self.rooms_btn
        ]
        self.set_branch_editor_enabled(False)

        self.setup_connections()
        self.load_initial_data()
        self.showMaximized()

        self.branches_list.setFocusPolicy(Qt.StrongFocus)
        self.branches_list.installEventFilter(self)

    def setup_connections(self):
        self.company_name_edit.textChanged.connect(self.on_change)
        self.branches_spin.valueChanged.connect(self.on_change)
        self.branch_name_edit.textChanged.connect(self.on_change)
        self.branch_address_edit.textChanged.connect(self.on_change)
        self.floors_spin.valueChanged.connect(self.on_change)

        if self.save_branch_count_btn is not None:
            self.save_branch_count_btn.clicked.connect(self.save_branches_count)
        self.branches_list.itemClicked.connect(self.on_branch_selected)
        if self.save_branch_btn is not None:
            self.save_branch_btn.clicked.connect(self.save_branch)
        self.delete_branch_btn.clicked.connect(self.delete_branch)
        self.employees_btn.clicked.connect(self.open_employees_dialog)
        self.rooms_btn.clicked.connect(self.open_rooms_dialog)
        self.save_all_btn.clicked.connect(self.save_all_changes)
        self.reset_all_btn.clicked.connect(self.hard_reset_database)

        self.reset_all_btn.setShortcut(Qt.Key_F5)
        self.reset_all_btn.setToolTip("Полный сброс базы данных (F5)")

    def set_branch_editor_enabled(self, enabled):
        if self.branch_group is not None:
            self.branch_group.setEnabled(enabled)
            return
        for widget in self.branch_editor_widgets:
            widget.setEnabled(enabled)

    def eventFilter(self, obj, event):
        if obj == self.branches_list and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.delete_branch()
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.hard_reset_database()
            event.accept()
        elif event.key() == Qt.Key_Delete and self.branches_list.hasFocus():
            self.delete_branch()
            event.accept()
        else:
            super().keyPressEvent(event)

    def register_rooms_dialog(self, dialog):
        if dialog not in self.open_rooms_dialogs:
            self.open_rooms_dialogs.append(dialog)

    def unregister_rooms_dialog(self, dialog):
        if dialog in self.open_rooms_dialogs:
            self.open_rooms_dialogs.remove(dialog)

    def refresh_all_rooms_dialogs(self):
        for dialog in self.open_rooms_dialogs:
            dialog.load_responsible_employees()
        QApplication.processEvents()

    def on_change(self):
        self.changes_made = True

    def load_initial_data(self):
        company_name = self.db.get_company_name()
        self.company_name_edit.setText(company_name)
        self.original_company_name = company_name
        self.load_branches()

    def load_branches(self):
        self.branches_list.clear()
        branches = self.db.get_all_branches()
        for branch in branches:
            item = QListWidgetItem(branch[1])
            item.setData(Qt.UserRole, branch[0])
            self.branches_list.addItem(item)
        self.branches_spin.setValue(len(branches))

    def refresh_current_branch_data(self):
        if self.current_branch_id:
            branch = self.db.get_branch(self.current_branch_id)
            if branch:
                self.branch_name_edit.setText(branch[1])
                self.floors_spin.setValue(branch[2])
                self.branch_address_edit.setText(branch[3] or "")

                employees = self.db.get_employees(self.current_branch_id)
                rooms = self.db.get_rooms_by_branch(self.current_branch_id)
                self.employees_spin.setValue(len(employees))
                self.rooms_spin.setValue(len(rooms))

    def save_branches_count(self):
        current = self.branches_list.count()
        target = self.branches_spin.value()
        if target > current:
            for i in range(current + 1, target + 1):
                self.db.add_branch(f"Филиал №{i}")
            self.load_branches()
            self.changes_made = False
            QMessageBox.information(self, "Успех", f"Добавлено {target - current} филиалов")
        elif target < current:
            QMessageBox.warning(self, "Внимание",
                                "Для уменьшения количества филиалов удалите лишние вручную (выберите филиал и нажмите Delete или кнопку Удалить)")
            return False
        return True

    def on_branch_selected(self, item):
        self.current_branch_id = item.data(Qt.UserRole)
        self.refresh_current_branch_data()
        self.set_branch_editor_enabled(True)

    def save_branch(self):
        if not self.current_branch_id:
            return
        name = self.branch_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название филиала")
            return

        self.db.update_branch(self.current_branch_id, name,
                              self.floors_spin.value(),
                              self.branch_address_edit.text().strip())

        for i in range(self.branches_list.count()):
            item = self.branches_list.item(i)
            if item.data(Qt.UserRole) == self.current_branch_id:
                item.setText(name)
                break

        QMessageBox.information(self, "Успех", f"Филиал сохранен (этажей: {self.floors_spin.value()})")

    def delete_branch(self):
        if not self.current_branch_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите филиал для удаления")
            return

        reply = QMessageBox.question(self, "Подтверждение",
                                     "Удалить филиал? Все связанные данные (сотрудники, комнаты, оборудование) будут потеряны.",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_branch(self.current_branch_id)
            self.load_branches()
            self.set_branch_editor_enabled(False)
            self.current_branch_id = None
            self.branch_name_edit.clear()
            self.branch_address_edit.clear()
            self.floors_spin.setValue(1)
            self.employees_spin.setValue(0)
            self.rooms_spin.setValue(0)
            self.changes_made = True
            QMessageBox.information(self, "Успех", "Филиал удален")

    def open_employees_dialog(self):
        if self.current_branch_id:
            dialog = EmployeesDialog(self.db, self.current_branch_id,
                                     self.branch_name_edit.text(), self)
            dialog.finished.connect(lambda: self.on_employees_dialog_closed())
            dialog.exec()

    def on_employees_dialog_closed(self):
        if self.current_branch_id:
            employees = self.db.get_employees(self.current_branch_id)
            self.employees_spin.setValue(len(employees))

    def open_rooms_dialog(self):
        if self.current_branch_id:
            dialog = RoomsDialog(self.db, self.current_branch_id,
                                 self.branch_name_edit.text(), self)
            dialog.finished.connect(lambda: self.on_rooms_dialog_closed())
            dialog.exec()

    def on_rooms_dialog_closed(self):
        if self.current_branch_id:
            rooms = self.db.get_rooms_by_branch(self.current_branch_id)
            self.rooms_spin.setValue(len(rooms))

    def save_all_changes(self):
        try:
            if not self.save_branches_count():
                return
            company_name = self.company_name_edit.text().strip()
            if company_name:
                self.db.save_company_name(company_name)
            if self.current_branch_id:
                self.save_branch()
            self.changes_made = False
            QMessageBox.information(self, "Успех", "Все изменения сохранены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {str(e)}")

    def hard_reset_database(self):
        """Полный сброс базы данных"""
        reply = QMessageBox.question(self, "Полный сброс",
                                     "⚠️ ВНИМАНИЕ! Это действие полностью очистит базу данных!\n\n"
                                     "Будут удалены:\n"
                                     "- Все филиалы\n"
                                     "- Все сотрудники\n"
                                     "- Все комнаты\n"
                                     "- Все оборудование\n"
                                     "- Все отчеты\n\n"
                                     "Будут добавлены тестовые данные.\n\n"
                                     "Вы уверены?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            reply2 = QMessageBox.question(self, "Подтверждение",
                                          "Последнее предупреждение!\n"
                                          "Все данные будут безвозвратно удалены!\n\n"
                                          "Продолжить?",
                                          QMessageBox.Yes | QMessageBox.No)
            if reply2 == QMessageBox.Yes:
                # Закрываем все открытые диалоги комнат
                for dialog in self.open_rooms_dialogs[:]:  # Используем срез для копии списка
                    try:
                        dialog.close()
                    except:
                        pass
                self.open_rooms_dialogs.clear()

                # Закрываем все другие открытые диалоги
                for widget in QApplication.topLevelWidgets():
                    if isinstance(widget, QDialog) and widget != self and widget.isVisible():
                        try:
                            widget.close()
                        except:
                            pass

                # Выполняем сброс базы данных
                success = self.db.hard_reset_database()

                if success:
                    # Полностью перезагружаем интерфейс
                    self.load_initial_data()
                    self.current_branch_id = None
                    self.set_branch_editor_enabled(False)
                    self.branch_name_edit.clear()
                    self.branch_address_edit.clear()
                    self.floors_spin.setValue(1)
                    self.employees_spin.setValue(0)
                    self.rooms_spin.setValue(0)
                    self.changes_made = False

                    QMessageBox.information(self, "Успех", "База данных полностью сброшена!\nДобавлены тестовые данные.")
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось выполнить сброс базы данных!")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Настройки")
    app.setOrganizationName("Diplom")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
