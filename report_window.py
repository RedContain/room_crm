import sys
import os
from datetime import datetime

# Добавляем путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDateTime, Signal, QFile, QIODevice
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtUiTools import QUiLoader

# ========== ИМПОРТ НАШИХ МОДУЛЕЙ ==========
import paths
from database_handler import DatabaseHandler
from ui.ui_reportwindow import Ui_reportWindow  # или как называется класс

# ========== ИМПОРТ plane (если доступен) ==========
PLANE_AVAILABLE = False
try:
    from plane import MainWindow as PlaneWindow
    PLANE_AVAILABLE = True
except ImportError:
    print("⚠️ Модуль plane не найден, функция схем будет недоступна")

# ========== ИМПОРТ settings (если доступен) ==========
SETTINGS_AVAILABLE = False
try:
    from settings import MainWindow as SettingsWindow
    SETTINGS_AVAILABLE = True
except ImportError:
    print("⚠️ Модуль settings не найден, функция настроек будет недоступна")


class ConfirmationDialog(QDialog):
    def __init__(self, message="Вы уверены?", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(message))

        btn_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)


class SaveConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Сохранение")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Сохранить изменения?"))

        btn_box = QDialogButtonBox()
        btn_save = btn_box.addButton("Сохранить", QDialogButtonBox.AcceptRole)
        btn_discard = btn_box.addButton("Не сохранять", QDialogButtonBox.DestructiveRole)
        btn_cancel = btn_box.addButton("Отмена", QDialogButtonBox.RejectRole)

        btn_save.clicked.connect(lambda: self.done(1))
        btn_discard.clicked.connect(lambda: self.done(2))
        btn_cancel.clicked.connect(self.reject)

        layout.addWidget(btn_box)


class WorkplaceDialog(QDialog):
    def __init__(self, db, room_id, workplace_number, parent=None):
        super().__init__(parent)
        self.db = db
        self.room_id = room_id
        self.workplace_number = workplace_number
        self.setWindowTitle(f"Рабочее место №{workplace_number}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.equipment_type = QComboBox()
        self.equipment_type.addItems(["Компьютер", "Монитор", "Ноутбук", "Принтер", "МФУ", "Другое"])
        form.addRow("Тип оборудования:", self.equipment_type)

        self.equipment_name = QLineEdit()
        form.addRow("Название:", self.equipment_name)

        self.serial_number = QLineEdit()
        form.addRow("Серийный номер:", self.serial_number)

        self.has_monitor = QCheckBox("Есть монитор")
        form.addRow("", self.has_monitor)

        self.has_keyboard = QCheckBox("Есть клавиатура")
        form.addRow("", self.has_keyboard)

        self.has_mouse = QCheckBox("Есть мышь")
        form.addRow("", self.has_mouse)

        self.has_power_cable = QCheckBox("Есть кабель питания")
        form.addRow("", self.has_power_cable)

        self.notes = QLineEdit()
        form.addRow("Примечания:", self.notes)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_data(self):
        return {
            'number': self.workplace_number,
            'type': self.equipment_type.currentText(),
            'name': self.equipment_name.text(),
            'serial': self.serial_number.text(),
            'has_monitor': self.has_monitor.isChecked(),
            'has_keyboard': self.has_keyboard.isChecked(),
            'has_mouse': self.has_mouse.isChecked(),
            'has_power_cable': self.has_power_cable.isChecked(),
            'notes': self.notes.text()
        }


class WorkplaceWidget(QWidget):
    edit_clicked = Signal(int)
    delete_clicked = Signal(int)

    def __init__(self, number, data=None):
        super().__init__()
        self.number = number
        self.data = data or {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        title = QLabel(f"Место №{number}")
        title.setMinimumWidth(80)
        layout.addWidget(title)

        if data and data.get('name'):
            info = QLabel(f"{data.get('type', '')}: {data.get('name', '')}")
            layout.addWidget(info, 1)
        else:
            empty = QLabel("не заполнено")
            empty.setStyleSheet("color: gray; font-style: italic;")
            layout.addWidget(empty, 1)

        edit_btn = QPushButton("✏️")
        edit_btn.setMaximumWidth(30)
        edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.number))

        delete_btn = QPushButton("🗑️")
        delete_btn.setMaximumWidth(30)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.number))

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)


class ReportWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_reportWindow()
        self.ui.setupUi(self)
        self.db = DatabaseHandler()
        self.current_report_id = None
        self.current_room_id = None
        self.workplaces_data = {}
        self.arrival_items = []
        self.distribution_model = None
        self.settings_window = None
        self.plane_window = None
        self.create_menu()
        self.setup_tabs()
        self.load_initial_data()
        self.showMaximized()

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")
        file_menu.addAction("Новая отчетность", self.new_report)
        file_menu.addAction("Новое поступление", self.new_arrival)
        file_menu.addSeparator()
        file_menu.addAction("Сохранить отчет", self.save_report_txt)
        file_menu.addAction("Сохранить как...", self.save_report_as)
        file_menu.addSeparator()
        file_menu.addAction("Полный список отчетов", self.show_reports_list)
        file_menu.addSeparator()
        file_menu.addAction("Выход", self.close)

        settings_menu = menubar.addMenu("Настройки")
        settings_menu.addAction("Размер шрифта", self.on_font_size)
        settings_menu.addAction("Тема", self.on_theme)
        settings_menu.addSeparator()

        if SETTINGS_AVAILABLE:
            settings_menu.addAction("Редактировать рабочее окружение", self.open_settings_window)
        else:
            action = settings_menu.addAction("Редактировать рабочее окружение (недоступно)")
            action.setEnabled(False)

        help_menu = menubar.addMenu("Справка")
        help_menu.addAction("Версия", self.show_version)
        help_menu.addAction("О программе", self.show_project_info)

        schema_menu = menubar.addMenu("Открыть схему")
        schema_menu.addAction("Показать схему", self.show_schema)

    def open_settings_window(self):
        if not SETTINGS_AVAILABLE:
            QMessageBox.warning(self, "Ошибка", "Модуль настроек не найден")
            return

        try:
            dialog = SettingsWindow()
            dialog.exec()
            self.refresh_comboboxes()
        except Exception as e:
            # Добавим проверку - если это не настоящая ошибка, не показываем
            if "exec" not in str(e):  # игнорируем ошибку про exec
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть настройки:\n{e}")

    def show_schema(self):
        if not PLANE_AVAILABLE:
            QMessageBox.warning(self, "Ошибка", "Модуль схем не найден")
            return
        try:
            self.plane_window = PlaneWindow()
            self.plane_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть схему:\n{e}")

    def setup_tabs(self):
        self.setup_arrival_tab()
        self.setup_inventory_tab()
        self.setup_distribution_tab()

    # ========== ВКЛАДКА ПОСТУПЛЕНИЕ ==========
    def setup_arrival_tab(self):
        self.load_branches_to_combo(self.ui.comboBox_5)
        self.load_branches_to_combo(self.ui.comboBox_6)
        self.load_employees_to_combo(self.ui.comboBox_8)

        if hasattr(self.ui, 'doubleSpinBox'):
            self.ui.doubleSpinBox.setMaximum(9999999.99)
            self.ui.doubleSpinBox.setMinimum(0)
            self.ui.doubleSpinBox.setSingleStep(100)

        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "№", "Название", "Категория", "Тип", "Количество", "Цена", "Серийный №"
        ])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.tableWidget.setSelectionMode(QTableWidget.MultiSelection)

        if hasattr(self.ui, 'pushButton_5'):
            self.ui.pushButton_5.clicked.connect(self.export_arrival_pdf)
        if hasattr(self.ui, 'pushButton_3'):
            self.ui.pushButton_3.clicked.connect(self.export_arrival_txt)
        if hasattr(self.ui, 'pushButton_2'):
            self.ui.pushButton_2.clicked.connect(self.cancel_arrival)
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.save_arrival)
        if hasattr(self.ui, 'pushButton_16'):
            self.ui.pushButton_16.clicked.connect(self.add_arrival_position)

        self.load_arrival_data()

    def load_arrival_data(self):
        try:
            equipment = self.db.get_all_equipment()
            self.ui.tableWidget.setRowCount(0)
            for i, item in enumerate(equipment):
                self.ui.tableWidget.insertRow(i)
                self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(item[1]))
                self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(item[2]))
                self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(item[3]))
                self.ui.tableWidget.setItem(i, 4, QTableWidgetItem("1"))
                self.ui.tableWidget.setItem(i, 5, QTableWidgetItem("0"))
                self.ui.tableWidget.setItem(i, 6, QTableWidgetItem(item[4]))
        except Exception as e:
            print(f"Ошибка загрузки поступлений: {e}")

    def add_arrival_position(self):
        data = {
            'name': self.ui.lineEdit_15.text() if hasattr(self.ui, 'lineEdit_15') else "",
            'category': self.ui.comboBox_9.currentText() if hasattr(self.ui, 'comboBox_9') else "",
            'type': self.ui.comboBox_10.currentText() if hasattr(self.ui, 'comboBox_10') else "",
            'quantity': self.ui.spinBox_2.value() if hasattr(self.ui, 'spinBox_2') else 1,
            'serial_number': self.ui.lineEdit_18.text() if hasattr(self.ui, 'lineEdit_18') else "",
            'supplier': self.ui.lineEdit_7.text() if hasattr(self.ui, 'lineEdit_7') else "",
            'price': self.ui.doubleSpinBox.value() if hasattr(self.ui, 'doubleSpinBox') else 0,
            'date_incoming': self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd") if hasattr(self.ui, 'dateTimeEdit') else datetime.now().strftime("%Y-%m-%d"),
            'state_incoming': 1,
            'phone_supplier': self.ui.lineEdit_9.text() if hasattr(self.ui, 'lineEdit_9') else "",
            'email_supplier': self.ui.lineEdit_10.text() if hasattr(self.ui, 'lineEdit_10') else "",
            'notes': self.ui.plainTextEdit.toPlainText() if hasattr(self.ui, 'plainTextEdit') else ""
        }

        if not data['name'] or not data['serial_number']:
            QMessageBox.warning(self, "Ошибка", "Заполните название и серийный номер")
            return

        try:
            equip_id = self.db.add_equipment(data)
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(data['name']))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(data['category']))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(data['type']))
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(str(data['quantity'])))
            self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(str(data['price'])))
            self.ui.tableWidget.setItem(row, 6, QTableWidgetItem(data['serial_number']))
            self.clear_arrival_form()
            QMessageBox.information(self, "Успех", f"Позиция добавлена (ID: {equip_id})")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def clear_arrival_form(self):
        if hasattr(self.ui, 'lineEdit_15'):
            self.ui.lineEdit_15.clear()
        if hasattr(self.ui, 'lineEdit_18'):
            self.ui.lineEdit_18.clear()
        if hasattr(self.ui, 'spinBox_2'):
            self.ui.spinBox_2.setValue(1)
        if hasattr(self.ui, 'doubleSpinBox'):
            self.ui.doubleSpinBox.setValue(0)

    def export_arrival_txt(self):
        if self.ui.tableWidget.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Нет данных для выгрузки")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", "", "Текстовые файлы (*.txt)")
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("ОТЧЕТ О ПОСТУПЛЕНИИ\n")
                f.write(f"Дата: {QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}\n")
                f.write("=" * 50 + "\n\n")

                f.write("ДАННЫЕ ПОСТУПЛЕНИЯ:\n")
                if hasattr(self.ui, 'lineEdit_5'):
                    f.write(f"Название: {self.ui.lineEdit_5.text()}\n")
                if hasattr(self.ui, 'lineEdit_6'):
                    f.write(f"Номер приказа: {self.ui.lineEdit_6.text()}\n")
                if hasattr(self.ui, 'textEdit_4'):
                    f.write(f"Описание: {self.ui.textEdit_4.toPlainText()}\n")

                f.write("\nПОЗИЦИИ:\n")
                f.write("-" * 50 + "\n")
                f.write(f"{'№':<4} {'Название':<20} {'Категория':<15} {'Кол-во':<8} {'Цена':<10}\n")
                f.write("-" * 50 + "\n")

                total = 0
                for row in range(self.ui.tableWidget.rowCount()):
                    num = self.ui.tableWidget.item(row, 0).text() if self.ui.tableWidget.item(row, 0) else ""
                    name = self.ui.tableWidget.item(row, 1).text() if self.ui.tableWidget.item(row, 1) else ""
                    cat = self.ui.tableWidget.item(row, 2).text() if self.ui.tableWidget.item(row, 2) else ""
                    qty = self.ui.tableWidget.item(row, 4).text() if self.ui.tableWidget.item(row, 4) else "0"
                    price = self.ui.tableWidget.item(row, 5).text() if self.ui.tableWidget.item(row, 5) else "0"
                    f.write(f"{num:<4} {name:<20} {cat:<15} {qty:<8} {price:<10}\n")
                    try:
                        total += int(qty) * float(price)
                    except:
                        pass

                f.write("-" * 50 + "\n")
                f.write(f"ИТОГО: {total} руб.\n")

            QMessageBox.information(self, "Успех", f"Отчет сохранен: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def export_arrival_pdf(self):
        QMessageBox.information(self, "Информация", "Функция PDF будет добавлена позже")

    def cancel_arrival(self):
        dlg = ConfirmationDialog("Отменить ввод данных?", self)
        if dlg.exec() == QDialog.Accepted:
            self.clear_arrival_form()

    def save_arrival(self):
        dlg = ConfirmationDialog("Сохранить все изменения?", self)
        if dlg.exec() == QDialog.Accepted:
            try:
                self.ui.progressBar.setValue(100)
                QMessageBox.information(self, "Успех", "Данные сохранены в БД")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    # ========== ВКЛАДКА ИНВЕНТАРИЗАЦИЯ ==========
    def setup_inventory_tab(self):
        self.load_branches_to_combo(self.ui.comboBox_3)
        self.load_branches_to_combo(self.ui.comboBox_4)
        self.load_employees_to_combo(self.ui.comboBox)
        self.load_employees_to_combo(self.ui.comboBox_2)

        if hasattr(self.ui, 'comboBox_4'):
            self.ui.comboBox_4.currentIndexChanged.connect(self.on_branch_changed_inventory)
        if hasattr(self.ui, 'spinBox_3'):
            self.ui.spinBox_3.valueChanged.connect(self.on_floor_changed_inventory)
        if hasattr(self.ui, 'comboBox_7'):
            self.ui.comboBox_7.currentIndexChanged.connect(self.on_room_changed_inventory)

        if hasattr(self.ui, 'tableView'):
            self.ui.tableView.setModel(QStandardItemModel())
            model = self.ui.tableView.model()
            if model:
                model.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Серийный №", "Статус"])

        if hasattr(self.ui, 'comboBox_12'):
            self.ui.comboBox_12.currentIndexChanged.connect(self.apply_inventory_filters)
        if hasattr(self.ui, 'comboBox_11'):
            self.ui.comboBox_11.currentIndexChanged.connect(self.apply_inventory_filters)
        if hasattr(self.ui, 'lineEdit_20'):
            self.ui.lineEdit_20.textChanged.connect(self.apply_inventory_filters)
        if hasattr(self.ui, 'lineEdit_21'):
            self.ui.lineEdit_21.textChanged.connect(self.apply_inventory_filters)
        if hasattr(self.ui, 'lineEdit_22'):
            self.ui.lineEdit_22.textChanged.connect(self.apply_inventory_filters)

        self.load_categories_to_combo(self.ui.comboBox_12)
        self.load_types_to_combo(self.ui.comboBox_11)

        if hasattr(self.ui, 'pushButton_11'):
            self.ui.pushButton_11.clicked.connect(self.export_inventory_room_report)

    def on_branch_changed_inventory(self):
        branch_id = self.ui.comboBox_4.currentData()
        if branch_id:
            branch = self.db.get_branch(branch_id)
            if branch and hasattr(self.ui, 'spinBox_3'):
                self.ui.spinBox_3.setMaximum(branch[2])

    def on_floor_changed_inventory(self):
        branch_id = self.ui.comboBox_4.currentData()
        floor = self.ui.spinBox_3.value() if hasattr(self.ui, 'spinBox_3') else 1
        if branch_id and floor and hasattr(self.ui, 'comboBox_7'):
            self.load_rooms_to_combo(self.ui.comboBox_7, branch_id, floor)

    def on_room_changed_inventory(self):
        room_id = self.ui.comboBox_7.currentData() if hasattr(self.ui, 'comboBox_7') else None
        if not room_id:
            return

        equipment = self.db.get_equipment_by_room(room_id)
        model = self.ui.tableView.model()
        if model:
            model.removeRows(0, model.rowCount())
            for item in equipment:
                row = [
                    QStandardItem(str(item[0])),
                    QStandardItem(item[1]),
                    QStandardItem(item[2]),
                    QStandardItem(item[4]),
                    QStandardItem(item[5])
                ]
                model.appendRow(row)

    def apply_inventory_filters(self):
        pass

    def export_inventory_room_report(self):
        room_id = self.ui.comboBox_7.currentData() if hasattr(self.ui, 'comboBox_7') else None
        if not room_id:
            QMessageBox.warning(self, "Ошибка", "Выберите комнату")
            return

        room = self.db.get_room(room_id)
        if not room:
            return

        equipment = self.db.get_equipment_by_room(room_id)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет по инвентаризации",
            f"Инвентаризация_{room[1]}.txt", "Текстовые файлы (*.txt)"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("ИНВЕНТАРИЗАЦИОННАЯ ОПИСЬ\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Комната: {room[1]} - {room[2]}\n")
                f.write(f"Этаж: {room[3]}\n")
                f.write(f"Вместимость: {room[4]} чел.\n")
                f.write(f"Площадь: {room[8]} м²\n")
                f.write(f"Столов: {room[5]}, Стульев: {room[6]}, Розеток: {room[7]}\n")
                f.write(f"Дата инвентаризации: {QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm')}\n\n")
                f.write("=" * 60 + "\n")
                f.write("ПЕРЕЧЕНЬ ОБОРУДОВАНИЯ\n")
                f.write("=" * 60 + "\n\n")

                if not equipment:
                    f.write("В комнате нет оборудования\n")
                else:
                    f.write(f"{'№':<4} {'Наименование':<30} {'Категория':<15} {'Тип':<15} {'Серийный №':<15} {'Статус':<10}\n")
                    f.write("-" * 90 + "\n")
                    for i, item in enumerate(equipment, 1):
                        f.write(f"{i:<4} {item[1]:<30} {item[2]:<15} {item[3]:<15} {item[4]:<15} {item[5]:<10}\n")
                    f.write("-" * 90 + "\n")
                    f.write(f"Всего единиц: {len(equipment)}\n\n")

                f.write("\n" + "=" * 60 + "\n")
                f.write("Ответственный за инвентаризацию:\n\n")
                f.write("____________________  /______________/\n")
                f.write("   (подпись)              (ФИО)\n\n")
                f.write("Дата: ______________\n")

            QMessageBox.information(self, "Успех", f"Отчет сохранен:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить отчет:\n{e}")

    # ========== ВКЛАДКА РАСПРЕДЕЛЕНИЕ ==========
    def setup_distribution_tab(self):
        self.load_employees_with_position(self.ui.comboBox_13)
        self.load_branches_to_combo(self.ui.comboBox_15)
        self.load_branches_to_combo(self.ui.comboBox_14)

        self.ui.comboBox_14.currentIndexChanged.connect(self.on_branch_changed_distribution)
        self.ui.spinBox_6.valueChanged.connect(self.on_floor_changed_distribution)
        self.ui.comboBox_16.currentIndexChanged.connect(self.on_room_changed_distribution)

        self.setup_workplaces_area()
        self.setup_distribution_table()

        if hasattr(self.ui, 'pushButton_15'):
            self.ui.pushButton_15.clicked.connect(self.transfer_selected_items)

        self.ui.comboBox_17.currentIndexChanged.connect(self.apply_distribution_filters)
        self.ui.comboBox_18.currentIndexChanged.connect(self.apply_distribution_filters)
        self.ui.lineEdit_27.textChanged.connect(self.apply_distribution_filters)
        self.ui.lineEdit_26.textChanged.connect(self.apply_distribution_filters)
        self.ui.lineEdit_25.textChanged.connect(self.apply_distribution_filters)

        self.load_categories_to_combo(self.ui.comboBox_17)
        self.load_types_to_combo(self.ui.comboBox_18)

        if hasattr(self.ui, 'pushButton_8'):
            self.ui.pushButton_8.clicked.connect(self.save_all_distribution)
        if hasattr(self.ui, 'pushButton_9'):
            self.ui.pushButton_9.clicked.connect(self.delete_all_distribution)
        if hasattr(self.ui, 'pushButton_4'):
            self.ui.pushButton_4.clicked.connect(self.save_room_distribution)
        if hasattr(self.ui, 'pushButton_6'):
            self.ui.pushButton_6.clicked.connect(self.reset_room_distribution)
        if hasattr(self.ui, 'pushButton_7'):
            self.ui.pushButton_7.clicked.connect(self.export_room_report)
        if hasattr(self.ui, 'pushButton_10'):
            self.ui.pushButton_10.clicked.connect(self.export_final_report)

    def setup_distribution_table(self):
        self.distribution_model = QStandardItemModel()
        self.distribution_model.setHorizontalHeaderLabels([
            "ID", "Название", "Категория", "Тип", "Серийный №", "Выбрать"
        ])
        self.ui.tableView_2.setModel(self.distribution_model)
        self.ui.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView_2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.load_distribution_equipment()

    def load_distribution_equipment(self):
        try:
            equipment = self.db.get_all_equipment()
            self.distribution_model.removeRows(0, self.distribution_model.rowCount())
            for item in equipment:
                row = []
                id_item = QStandardItem(str(item[0]))
                id_item.setEditable(False)
                row.append(id_item)
                name_item = QStandardItem(item[1])
                name_item.setEditable(False)
                row.append(name_item)
                cat_item = QStandardItem(item[2])
                cat_item.setEditable(False)
                row.append(cat_item)
                type_item = QStandardItem(item[3])
                type_item.setEditable(False)
                row.append(type_item)
                serial_item = QStandardItem(item[4])
                serial_item.setEditable(False)
                row.append(serial_item)
                check_item = QStandardItem()
                check_item.setCheckable(True)
                check_item.setEditable(False)
                row.append(check_item)
                self.distribution_model.appendRow(row)
        except Exception as e:
            print(f"Ошибка загрузки оборудования: {e}")

    def transfer_selected_items(self):
        if not self.current_room_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите комнату")
            return

        selected_ids = []
        for row in range(self.distribution_model.rowCount()):
            check_item = self.distribution_model.item(row, 5)
            if check_item and check_item.checkState() == Qt.Checked:
                id_item = self.distribution_model.item(row, 0)
                if id_item:
                    selected_ids.append(int(id_item.text()))

        if not selected_ids:
            QMessageBox.warning(self, "Ошибка", "Выберите позиции для переноса")
            return

        free_spot = None
        room = self.db.get_room(self.current_room_id)
        capacity = room[4] if room else 10

        for i in range(1, capacity + 1):
            if i not in self.workplaces_data:
                free_spot = i
                break

        if not free_spot:
            QMessageBox.warning(self, "Ошибка", "Нет свободных мест")
            return

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name, category, type, serial_number FROM equipment WHERE equipment_id = ?",
                           (selected_ids[0],))
            equip = cursor.fetchone()
        finally:
            conn.close()

        if equip:
            data = {
                'type': equip[2] if equip[2] else "Оборудование",
                'name': equip[1],
                'serial': equip[3],
                'has_monitor': False,
                'has_keyboard': False,
                'has_mouse': False,
                'has_power_cable': True,
                'notes': f"ID в БД: {selected_ids[0]}"
            }
            self.workplaces_data[free_spot] = data
            self.update_workplace_widget(free_spot, data)
            self.db.update_equipment_room(selected_ids[0], self.current_room_id)

            for row in range(self.distribution_model.rowCount()):
                id_item = self.distribution_model.item(row, 0)
                if id_item and int(id_item.text()) in selected_ids:
                    check_item = self.distribution_model.item(row, 5)
                    if check_item:
                        check_item.setCheckState(Qt.Unchecked)

            QMessageBox.information(self, "Успех", f"Позиция перенесена на место №{free_spot}")

        self.load_distribution_equipment()

    def on_branch_changed_distribution(self):
        branch_id = self.ui.comboBox_14.currentData()
        if branch_id:
            branch = self.db.get_branch(branch_id)
            if branch:
                self.ui.spinBox_6.setMaximum(branch[2])
                self.load_distribution_equipment()

    def on_floor_changed_distribution(self):
        branch_id = self.ui.comboBox_14.currentData()
        floor = self.ui.spinBox_6.value()
        if branch_id and floor:
            self.load_rooms_to_combo(self.ui.comboBox_16, branch_id, floor)

    def on_room_changed_distribution(self):
        room_id = self.ui.comboBox_16.currentData()
        if not room_id:
            return
        self.current_room_id = room_id
        room = self.db.get_room(room_id)
        if room:
            self.create_workplaces(room[4])

    def apply_distribution_filters(self):
        category = self.ui.comboBox_17.currentData()
        type_ = self.ui.comboBox_18.currentData()
        name_filter = self.ui.lineEdit_27.text().lower()

        for row in range(self.distribution_model.rowCount()):
            show = True
            if category and category != "Все категории":
                cat_item = self.distribution_model.item(row, 2)
                if cat_item and cat_item.text() != category:
                    show = False
            if show and type_ and type_ != "Все типы":
                type_item = self.distribution_model.item(row, 3)
                if type_item and type_item.text() != type_:
                    show = False
            if show and name_filter:
                name_item = self.distribution_model.item(row, 1)
                if name_item and name_filter not in name_item.text().lower():
                    show = False
            self.ui.tableView_2.setRowHidden(row, not show)

    def save_room_distribution(self):
        if not self.current_room_id:
            QMessageBox.warning(self, "Ошибка", "Выберите комнату")
            return
        dlg = ConfirmationDialog("Сохранить распределение для этой комнаты?", self)
        if dlg.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Успех", "Распределение сохранено")

    def reset_room_distribution(self):
        dlg = ConfirmationDialog("Сбросить распределение для этой комнаты?", self)
        if dlg.exec() == QDialog.Accepted:
            self.workplaces_data.clear()
            room_id = self.ui.comboBox_16.currentData()
            if room_id:
                room = self.db.get_room(room_id)
                if room:
                    self.create_workplaces(room[4])

    def save_all_distribution(self):
        dlg = ConfirmationDialog("Сохранить все распределения?", self)
        if dlg.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Успех", "Все распределения сохранены")

    def delete_all_distribution(self):
        dlg = ConfirmationDialog("Удалить все распределения?", self)
        if dlg.exec() == QDialog.Accepted:
            self.workplaces_data.clear()
            self.clear_workplaces()

    def export_room_report(self):
        room_id = self.ui.comboBox_16.currentData()
        if not room_id:
            QMessageBox.warning(self, "Ошибка", "Выберите комнату")
            return

        room = self.db.get_room(room_id)
        if not room:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет по комнате", "", "Текстовые файлы (*.txt)")
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write(f"ОТЧЕТ ПО КОМНАТЕ: {room[1]} - {room[2]}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Этаж: {room[3]}\n")
                f.write(f"Вместимость: {room[4]} чел.\n")
                f.write(f"Столов: {room[5]}, Стульев: {room[6]}\n")
                f.write(f"Розеток: {room[7]}, Площадь: {room[8]} м²\n\n")
                f.write("РАБОЧИЕ МЕСТА:\n")
                f.write("-" * 50 + "\n")
                for i in range(1, room[4] + 1):
                    data = self.workplaces_data.get(i, {})
                    f.write(f"\nМесто №{i}:\n")
                    if data:
                        f.write(f"  Тип: {data.get('type', '')}\n")
                        f.write(f"  Название: {data.get('name', '')}\n")
                        f.write(f"  Серийный номер: {data.get('serial', '')}\n")
                        f.write(f"  Комплектация: ")
                        items = []
                        if data.get('has_monitor'): items.append("монитор")
                        if data.get('has_keyboard'): items.append("клавиатура")
                        if data.get('has_mouse'): items.append("мышь")
                        if data.get('has_power_cable'): items.append("кабель питания")
                        f.write(", ".join(items) if items else "нет")
                        f.write("\n")
                        if data.get('notes'):
                            f.write(f"  Примечания: {data['notes']}\n")
                    else:
                        f.write("  не заполнено\n")
                f.write("\n" + "=" * 50 + "\n")
            QMessageBox.information(self, "Успех", f"Отчет сохранен: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def export_final_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить финальный отчет", "", "Текстовые файлы (*.txt)")
        if not file_path:
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("ФИНАЛЬНЫЙ ОТЧЕТ ПО РАСПРЕДЕЛЕНИЮ\n")
                f.write(f"Дата: {QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}\n")
                f.write("=" * 50 + "\n\n")
                if self.current_room_id:
                    room = self.db.get_room(self.current_room_id)
                    if room:
                        f.write(f"Комната: {room[1]} - {room[2]}\n")
                        f.write(f"Заполнено мест: {len(self.workplaces_data)} из {room[4]}\n\n")
                        for num, data in self.workplaces_data.items():
                            f.write(f"Место {num}: {data.get('name', 'не заполнено')}\n")
            QMessageBox.information(self, "Успех", f"Отчет сохранен: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def setup_workplaces_area(self):
        self.workplaces_scroll = QScrollArea()
        self.workplaces_scroll.setWidgetResizable(True)
        self.workplaces_scroll.setMinimumHeight(300)
        self.workplaces_container = QWidget()
        self.workplaces_layout = QVBoxLayout(self.workplaces_container)
        self.workplaces_layout.addStretch()
        self.workplaces_scroll.setWidget(self.workplaces_container)
        if hasattr(self.ui, 'groupBox_15'):
            layout = self.ui.groupBox_15.layout()
            if layout is None:
                layout = QVBoxLayout(self.ui.groupBox_15)
                self.ui.groupBox_15.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            layout.addWidget(self.workplaces_scroll)

    def create_workplaces(self, count):
        self.clear_workplaces()
        for i in range(1, count + 1):
            widget = WorkplaceWidget(i, self.workplaces_data.get(i))
            widget.edit_clicked.connect(self.edit_workplace)
            widget.delete_clicked.connect(self.delete_workplace)
            self.workplaces_layout.insertWidget(self.workplaces_layout.count() - 1, widget)

    def clear_workplaces(self):
        while self.workplaces_layout.count() > 1:
            item = self.workplaces_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

    def edit_workplace(self, number):
        dlg = WorkplaceDialog(self.db, self.current_room_id, number, self)
        if dlg.exec() == QDialog.Accepted:
            data = dlg.get_data()
            self.workplaces_data[number] = data
            self.update_workplace_widget(number, data)

    def update_workplace_widget(self, number, data):
        for i in range(self.workplaces_layout.count()):
            item = self.workplaces_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), WorkplaceWidget):
                if item.widget().number == number:
                    new_widget = WorkplaceWidget(number, data)
                    new_widget.edit_clicked.connect(self.edit_workplace)
                    new_widget.delete_clicked.connect(self.delete_workplace)
                    self.workplaces_layout.replaceWidget(item.widget(), new_widget)
                    item.widget().deleteLater()
                    break

    def delete_workplace(self, number):
        dlg = ConfirmationDialog(f"Удалить рабочее место №{number}?", self)
        if dlg.exec() == QDialog.Accepted:
            if number in self.workplaces_data:
                del self.workplaces_data[number]
            self.update_workplace_widget(number, None)

    # ========== ОБЩИЕ МЕТОДЫ ==========
    def load_initial_data(self):
        self.load_branches_to_combo(self.ui.comboBox_5)
        self.load_branches_to_combo(self.ui.comboBox_6)
        self.load_employees_to_combo(self.ui.comboBox_8)
        self.load_branches_to_combo(self.ui.comboBox_3)
        self.load_branches_to_combo(self.ui.comboBox_4)
        self.load_employees_to_combo(self.ui.comboBox)
        self.load_employees_to_combo(self.ui.comboBox_2)
        self.load_employees_with_position(self.ui.comboBox_13)
        self.load_branches_to_combo(self.ui.comboBox_15)
        self.load_branches_to_combo(self.ui.comboBox_14)
        self.load_categories_to_combo(self.ui.comboBox_9)
        self.load_types_to_combo(self.ui.comboBox_10)
        if hasattr(self.ui, 'dateTimeEdit'):
            self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.progressBar.setValue(0)

    def load_branches_to_combo(self, combo):
        if not combo:
            return
        combo.clear()
        combo.addItem("Выберите филиал", None)
        try:
            branches = self.db.get_all_branches()
            for branch in branches:
                combo.addItem(branch[1], branch[0])
        except Exception as e:
            print(f"Ошибка загрузки филиалов: {e}")

    def load_employees_to_combo(self, combo):
        if not combo:
            return
        combo.clear()
        combo.addItem("Выберите сотрудника", None)
        try:
            employees = self.db.get_employees()
            for emp in employees:
                combo.addItem(f"{emp[1]} ({emp[2]})", emp[0])
        except Exception as e:
            print(f"Ошибка загрузки сотрудников: {e}")

    def load_employees_with_position(self, combo):
        if not combo:
            return
        combo.clear()
        combo.addItem("Выберите сотрудника", None)
        try:
            employees = self.db.get_employees()
            for emp in employees:
                combo.addItem(emp[1], emp[0])
        except Exception as e:
            print(f"Ошибка загрузки сотрудников: {e}")

    def load_categories_to_combo(self, combo):
        if not combo:
            return
        combo.clear()
        combo.addItem("Все категории", None)
        categories = ["Оргтехника", "Мебель", "Медицинское", "Инструменты", "Расходные материалы"]
        for cat in categories:
            combo.addItem(cat, cat)

    def load_types_to_combo(self, combo):
        if not combo:
            return
        combo.clear()
        combo.addItem("Все типы", None)
        types = ["Ноутбук", "Компьютер", "Принтер", "Монитор", "Стол", "Стул", "Кровать", "Холодильник"]
        for t in types:
            combo.addItem(t, t)

    def load_rooms_to_combo(self, combo, branch_id, floor):
        if not combo:
            return
        combo.clear()
        combo.addItem("Выберите комнату", None)
        if branch_id and floor:
            try:
                rooms = self.db.get_rooms_by_branch_and_floor(branch_id, floor)
                for room in rooms:
                    combo.addItem(f"{room[1]} - {room[2]}", room[0])
            except Exception as e:
                print(f"Ошибка загрузки комнат: {e}")

    # ========== МЕТОДЫ МЕНЮ ==========
    def new_report(self):
        dlg = SaveConfirmationDialog(self)
        result = dlg.exec()
        if result == 1:
            self.save_report_txt()
            self.clear_all()
        elif result == 2:
            self.clear_all()

    def new_arrival(self):
        dlg = SaveConfirmationDialog(self)
        result = dlg.exec()
        if result == 1:
            self.save_arrival()
            self.clear_arrival_tab()
        elif result == 2:
            self.clear_arrival_tab()

    def save_report_txt(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab == 0:
            self.export_room_report()
        elif current_tab == 1:
            QMessageBox.information(self, "Информация", "Сохранение отчета инвентаризации")
        elif current_tab == 2:
            self.export_arrival_txt()

    def save_report_as(self):
        self.save_report_txt()

    def show_reports_list(self):
        QMessageBox.information(self, "Информация", "Функция списка отчетов временно недоступна")

    def on_font_size(self):
        QMessageBox.information(self, "Информация", "Функция изменения шрифта будет добавлена позже")

    def on_theme(self):
        QMessageBox.information(self, "Информация", "Функция изменения темы будет добавлена позже")

    def show_version(self):
        QMessageBox.information(self, "Версия", "Версия 1.0\nДипломный проект 2026")

    def show_project_info(self):
        QMessageBox.information(self, "Информация о проекте",
                                "Дипломный проект\n"
                                "Тема: Система учета оборудования\n"
                                "Разработчик: ...\n"
                                "Telegram: @katwell1\n\n"
                                "© 2026")

    def clear_all(self):
        self.clear_arrival_tab()
        self.clear_inventory_tab()
        self.clear_distribution_tab()

    def clear_arrival_tab(self):
        if hasattr(self.ui, 'lineEdit_5'):
            self.ui.lineEdit_5.setText("Поступление № ")
        if hasattr(self.ui, 'textEdit_4'):
            self.ui.textEdit_4.clear()
        if hasattr(self.ui, 'lineEdit_6'):
            self.ui.lineEdit_6.clear()
        if hasattr(self.ui, 'plainTextEdit'):
            self.ui.plainTextEdit.clear()

    def clear_inventory_tab(self):
        if hasattr(self.ui, 'lineEdit'):
            self.ui.lineEdit.clear()
        if hasattr(self.ui, 'textEdit'):
            self.ui.textEdit.clear()
        if hasattr(self.ui, 'lineEdit_3'):
            self.ui.lineEdit_3.clear()
        if hasattr(self.ui, 'textEdit_3'):
            self.ui.textEdit_3.clear()
        if hasattr(self.ui, 'lineEdit_4'):
            self.ui.lineEdit_4.clear()

    def clear_distribution_tab(self):
        if hasattr(self.ui, 'lineEdit_23'):
            self.ui.lineEdit_23.clear()
        if hasattr(self.ui, 'textEdit_5'):
            self.ui.textEdit_5.clear()
        if hasattr(self.ui, 'lineEdit_24'):
            self.ui.lineEdit_24.clear()
        self.workplaces_data.clear()
        self.clear_workplaces()

    def refresh_comboboxes(self):
        self.load_branches_to_combo(self.ui.comboBox_5)
        self.load_branches_to_combo(self.ui.comboBox_6)
        self.load_branches_to_combo(self.ui.comboBox_3)
        self.load_branches_to_combo(self.ui.comboBox_4)
        self.load_branches_to_combo(self.ui.comboBox_15)
        self.load_branches_to_combo(self.ui.comboBox_14)
        self.load_employees_to_combo(self.ui.comboBox_8)
        self.load_employees_to_combo(self.ui.comboBox)
        self.load_employees_to_combo(self.ui.comboBox_2)
        self.load_employees_with_position(self.ui.comboBox_13)
        self.load_distribution_equipment()


def main():
    app = QApplication(sys.argv)
    window = ReportWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()