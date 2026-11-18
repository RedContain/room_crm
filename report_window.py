import sys
import os
from datetime import datetime, timedelta
import uuid

# Добавляем путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDateTime, Signal, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem, QShortcut, QKeySequence, QIcon

# ========== ИМПОРТ НАШИХ МОДУЛЕЙ ==========
import paths
from database_handler import DatabaseHandler
from ui.ui_reportwindow import Ui_reportWindow

# ========== ДЛЯ PDF ==========
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import platform
    import subprocess

    def find_cyrillic_font():
        system = platform.system()
        font_paths = []

        if system == "Windows":
            windows_dir = os.environ.get('WINDIR', 'C:\\Windows')
            font_paths = [
                os.path.join(windows_dir, 'Fonts', 'arial.ttf'),
                os.path.join(windows_dir, 'Fonts', 'times.ttf'),
                os.path.join(windows_dir, 'Fonts', 'cour.ttf'),
                os.path.join(windows_dir, 'Fonts', 'verdana.ttf'),
                os.path.join(windows_dir, 'Fonts', 'tahoma.ttf'),
            ]
        elif system == "Darwin":
            font_paths = [
                '/Library/Fonts/Arial.ttf',
                '/Library/Fonts/Times New Roman.ttf',
                '/Library/Fonts/Courier New.ttf',
                '/Library/Fonts/Verdana.ttf',
                '/System/Library/Fonts/Helvetica.ttc',
            ]
        else:
            try:
                result = subprocess.run(['fc-list', ':family', 'file'],
                                        capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line and ('.ttf' in line or '.ttc' in line):
                            font_file = line.split(':')[0].strip()
                            if any(name in font_file.lower() for name in ['arial', 'dejavu', 'liberation', 'free']):
                                font_paths.append(font_file)
            except:
                pass

            font_paths.extend([
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
                '/usr/share/fonts/truetype/arial/arial.ttf',
            ])

        for path in font_paths:
            if os.path.exists(path):
                return path
        return None

    FONT_PATH = find_cyrillic_font()
    FONT_REGISTERED = False
    FONT_NAME = "Helvetica"

    if FONT_PATH:
        try:
            pdfmetrics.registerFont(TTFont('CyrillicFont', FONT_PATH))
            bold_path = FONT_PATH.replace('.ttf', 'b.ttf').replace('.ttc', 'b.ttc')
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont('CyrillicFont-Bold', bold_path))
            else:
                pdfmetrics.registerFont(TTFont('CyrillicFont-Bold', FONT_PATH))
            FONT_REGISTERED = True
            FONT_NAME = "CyrillicFont"
            print(f"✅ Зарегистрирован шрифт: {FONT_PATH}")
        except Exception as e:
            print(f"⚠️ Не удалось зарегистрировать шрифт {FONT_PATH}: {e}")

    PDF_AVAILABLE = True
except ImportError as e:
    PDF_AVAILABLE = False
    FONT_REGISTERED = False
    FONT_NAME = "Helvetica"
    print(f"⚠️ ReportLab не установлен. Функция PDF будет недоступна. Ошибка: {e}")

# ========== ИМПОРТ ДОПОЛНИТЕЛЬНЫХ МОДУЛЕЙ ==========
PLANE_AVAILABLE = False
try:
    from plane import MainWindow as PlaneWindow
    PLANE_AVAILABLE = True
except ImportError:
    print("⚠️ Модуль plane не найден, функция схем будет недоступна")

SETTINGS_AVAILABLE = False
SettingsWindowClass = None
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    import settings
    SettingsWindowClass = settings.MainWindow
    SETTINGS_AVAILABLE = True
    print(f"✅ Модуль settings загружен, путь: {settings.__file__}")
except Exception as e:
    print(f"⚠️ Ошибка при импорте settings: {e}")
    import traceback
    traceback.print_exc()


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


class ArrivalInfoDialog(QDialog):
    def __init__(self, arrival_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Информация о поступлении")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout(self)

        title = QLabel(f"Поступление: {arrival_data.get('name', '')}")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Поле", "Значение"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.setAlternatingRowColors(True)

        fields = [
            ("Название", arrival_data.get('name', '')),
            ("Номер приказа", arrival_data.get('order_number', '')),
            ("Описание", arrival_data.get('description', '')),
            ("Дата", arrival_data.get('date', '')),
            ("Филиал", arrival_data.get('branch_name', '')),
            ("Сотрудник", arrival_data.get('employee_name', '')),
            ("Номер докладной", arrival_data.get('doc_number', '')),
            ("Поставщик", arrival_data.get('supplier_name', '')),
            ("ИНН поставщика", arrival_data.get('supplier_inn', '')),
            ("Телефон поставщика", arrival_data.get('supplier_phone', '')),
            ("Email поставщика", arrival_data.get('supplier_email', '')),
            ("Общая сумма", f"{arrival_data.get('total_amount', 0):.2f} руб."),
            ("Номер накладной", arrival_data.get('waybill_number', '')),
            ("Номер договора", arrival_data.get('contract_number', '')),
            ("Примечания", arrival_data.get('notes', '')),
        ]

        table.setRowCount(len(fields))
        for i, (field, value) in enumerate(fields):
            table.setItem(i, 0, QTableWidgetItem(field))
            table.setItem(i, 1, QTableWidgetItem(str(value)))
            table.item(i, 0).setFlags(Qt.ItemIsEnabled)
            table.item(i, 1).setFlags(Qt.ItemIsEnabled)

        layout.addWidget(table)

        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)


class ReportsListDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Полный список отчетов")
        self.setMinimumSize(800, 400)

        layout = QVBoxLayout(self)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "ID", "Название", "Дата", "Сотрудник", "Филиал", "Номер приказа"
        ])
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

        self.load_data()

    def load_data(self):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT a.arrival_id, a.name, a.date, e.name_id, b.name, a.order_number
                           FROM arrivals a
                                    LEFT JOIN employees e ON a.employee_id = e.worker_id
                                    LEFT JOIN branches b ON a.branch_id = b.branch_id
                           ORDER BY a.date DESC
                           """)
            rows = cursor.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список отчетов: {e}")
            rows = []
        finally:
            conn.close()

        self.model.removeRows(0, self.model.rowCount())
        for row in rows:
            items = [QStandardItem(str(row[0])),
                     QStandardItem(row[1] or ""),
                     QStandardItem(row[2] or ""),
                     QStandardItem(row[3] or ""),
                     QStandardItem(row[4] or ""),
                     QStandardItem(row[5] or "")]
            self.model.appendRow(items)


class ReportWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_reportWindow()
        self.ui.setupUi(self)
        self.db = DatabaseHandler()
        self.current_report_id = None
        self.current_room_id = None
        self.distribution_model = None
        self.room_equipment_model = None
        self.settings_window = None
        self.plane_window = None
        self._settings_window = None

        self._ensure_extra_columns()
        self._ensure_arrivals_table()

        self.create_menu()
        self.setup_tabs()
        self.load_initial_data()
        self.setup_shortcuts()
        self.setup_notification_area()
        self.showMaximized()

    def _ensure_extra_columns(self):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(equipment)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'inventory_number' not in columns:
                cursor.execute("ALTER TABLE equipment ADD COLUMN inventory_number TEXT DEFAULT ''")
                print("✅ Добавлена колонка inventory_number в equipment")
            if 'workplace_number' not in columns:
                cursor.execute("ALTER TABLE equipment ADD COLUMN workplace_number INTEGER DEFAULT NULL")
                print("✅ Добавлена колонка workplace_number в equipment")
            if 'model' not in columns:
                cursor.execute("ALTER TABLE equipment ADD COLUMN model TEXT DEFAULT ''")
                print("✅ Добавлена колонка model в equipment")
            if 'manufacturer' not in columns:
                cursor.execute("ALTER TABLE equipment ADD COLUMN manufacturer TEXT DEFAULT ''")
                print("✅ Добавлена колонка manufacturer в equipment")
            conn.commit()
        except Exception as e:
            print(f"⚠️ Ошибка при добавлении колонок: {e}")
        finally:
            conn.close()

    def _ensure_arrivals_table(self):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
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
            conn.commit()
            print("✅ Таблица arrivals создана/проверена")
        except Exception as e:
            print(f"⚠️ Ошибка при создании arrivals: {e}")
        finally:
            conn.close()

    def setup_notification_area(self):
        self.notification_label = QLabel(self.ui.centralwidget)
        self.notification_label.setAlignment(Qt.AlignCenter)
        self.notification_label.setFixedSize(189, 113)
        self.notification_label.setWordWrap(True)
        self.notification_label.setStyleSheet("""
            QLabel {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        self.notification_label.hide()

        if hasattr(self, 'notification_timer') and self.notification_timer is not None:
            try:
                self.notification_timer.stop()
                self.notification_timer.deleteLater()
            except:
                pass
        self.notification_timer = QTimer(self)
        self.notification_timer.setSingleShot(True)
        self.notification_timer.timeout.connect(self.notification_label.hide)

        self.update_notification_position()

    def update_notification_position(self):
        if hasattr(self, 'notification_label'):
            central = self.ui.centralwidget
            x = central.width() - self.notification_label.width() - 10
            y = 10
            self.notification_label.move(x, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_notification_position()

    def show_notification(self, message, error=False):
        if not self.isVisible():
            return

        if not hasattr(self, 'notification_timer') or self.notification_timer is None:
            self.setup_notification_area()
        else:
            try:
                self.notification_timer.isActive()
            except RuntimeError:
                self.setup_notification_area()

        if error:
            self.notification_label.setStyleSheet("""
                QLabel {
                    background-color: #f44336;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)
        else:
            self.notification_label.setStyleSheet("""
                QLabel {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)
        self.notification_label.setText(message)
        self.notification_label.show()
        self.update_notification_position()
        self.notification_timer.start(5000)

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, self.new_report)
        QShortcut(QKeySequence("Ctrl+Shift+N"), self, self.new_arrival)
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_current)
        QShortcut(QKeySequence("Ctrl+P"), self, self.export_current_pdf)
        QShortcut(QKeySequence("Delete"), self, self.delete_selected_in_current_tab)
        QShortcut(QKeySequence("F5"), self, self.refresh_current_tab)
        QShortcut(QKeySequence("Ctrl+F"), self, self.focus_on_filter)

    def current_tab_kind(self):
        current_index = self.ui.tabWidget.currentIndex()
        for widget_name, tab_kind in (
                ('tab_2', 'arrival'),
                ('tab_5', 'distribution'),
                ('tab', 'inventory')):
            widget = getattr(self.ui, widget_name, None)
            if widget is not None and self.ui.tabWidget.indexOf(widget) == current_index:
                return tab_kind
        return None

    def save_current(self):
        current_tab = self.current_tab_kind()
        if current_tab == 'arrival':
            self.save_arrival()
        elif current_tab == 'distribution':
            self.export_room_report()
        elif current_tab == 'inventory':
            self.export_inventory_room_report()

    def export_current_pdf(self):
        current_tab = self.current_tab_kind()
        if current_tab == 'arrival':
            self.export_arrival_pdf()
        elif current_tab == 'inventory':
            self.export_inventory_room_report_pdf()
        else:
            self.show_notification("PDF доступен для вкладок 'Поступление' и 'Инвентаризация'", error=True)

    def delete_selected_in_current_tab(self):
        current_tab = self.current_tab_kind()
        if current_tab == 'arrival':
            self.delete_selected_arrival()

    def refresh_current_tab(self):
        current_tab = self.current_tab_kind()
        if current_tab == 'arrival':
            self.load_arrival_data()
            self.show_notification("Данные поступления обновлены")
        elif current_tab == 'inventory':
            self.on_room_changed_inventory()
            self.show_notification("Данные инвентаризации обновлены")
        elif current_tab == 'distribution':
            self.load_distribution_equipment(silent=True)
            if self.current_room_id:
                self.load_room_equipment(self.current_room_id)
            self.show_notification("Данные распределения обновлены")

    def focus_on_filter(self):
        current_tab = self.current_tab_kind()
        if current_tab == 'arrival':
            if hasattr(self.ui, 'textEdit') and self.ui.textEdit.isVisible():
                self.ui.textEdit.setFocus()
        elif current_tab == 'inventory':
            if hasattr(self.ui, 'lineEdit_20'):
                self.ui.lineEdit_20.setFocus()
            elif hasattr(self.ui, 'textEdit_3'):
                self.ui.textEdit_3.setFocus()
        elif current_tab == 'distribution':
            if hasattr(self.ui, 'textEdit_2'):
                self.ui.textEdit_2.setFocus()

    def validate_required_fields(self, fields_dict):
        first_empty = None
        for widget, field_name in fields_dict.items():
            if isinstance(widget, QLineEdit):
                text = widget.text().strip()
            elif isinstance(widget, QComboBox):
                text = widget.currentText().strip()
            elif isinstance(widget, QTextEdit):
                text = widget.toPlainText().strip()
            else:
                continue

            if not text:
                widget.setStyleSheet("border: 2px solid red;")
                if first_empty is None:
                    first_empty = widget
            else:
                widget.setStyleSheet("")
        return first_empty

    def clear_validation(self, widget):
        widget.setStyleSheet("")

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")

        new_report_action = file_menu.addAction("Создать отчетность")
        new_report_action.setShortcut("Ctrl+N")
        new_report_action.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        new_report_action.triggered.connect(self.new_report)

        new_arrival_action = file_menu.addAction("Новое поступление")
        new_arrival_action.setShortcut("Ctrl+Shift+N")
        new_arrival_action.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        new_arrival_action.triggered.connect(self.new_arrival)

        file_menu.addSeparator()

        save_action = file_menu.addAction("Сохранить")
        save_action.setShortcut("Ctrl+S")
        save_action.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        save_action.triggered.connect(self.save_current)

        file_menu.addSeparator()

        reports_list_action = file_menu.addAction("Полный список отчетов")
        reports_list_action.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        reports_list_action.triggered.connect(self.show_reports_list)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("Выход")
        exit_action.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        exit_action.triggered.connect(self.close)

        settings_menu = menubar.addMenu("Настройки")

        if SETTINGS_AVAILABLE:
            env_action = settings_menu.addAction("Редактировать рабочее окружение")
            env_action.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
            env_action.triggered.connect(self.open_settings_window)
        else:
            env_action = settings_menu.addAction("Редактировать рабочее окружение (недоступно)")
            env_action.setEnabled(False)

        help_menu = menubar.addMenu("Справка")

        version_action = help_menu.addAction("Версия")
        version_action.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        version_action.triggered.connect(self.show_version)

        info_action = help_menu.addAction("О программе")
        info_action.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        info_action.triggered.connect(self.show_project_info)

        schema_menu = menubar.addMenu("Открыть схему")
        schema_action = schema_menu.addAction("Показать схему")
        schema_action.setIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        schema_action.triggered.connect(self.show_schema)

    def open_settings_window(self):
        if not SETTINGS_AVAILABLE or SettingsWindowClass is None:
            self.show_notification("Модуль настроек не найден", error=True)
            return

        try:
            if hasattr(self, '_settings_window') and self._settings_window is not None:
                try:
                    if self._settings_window.isVisible():
                        self._settings_window.raise_()
                        self._settings_window.activateWindow()
                        return
                except RuntimeError:
                    self._settings_window = None

            print("🔵 Создаем новое окно настроек...")

            self._settings_window = SettingsWindowClass()
            self._settings_window.setParent(None)

            main_geo = self.geometry()
            dialog_geo = self._settings_window.geometry()
            x = main_geo.x() + (main_geo.width() - dialog_geo.width()) // 2
            y = main_geo.y() + (main_geo.height() - dialog_geo.height()) // 2
            self._settings_window.move(x, y)

            self._settings_window.destroyed.connect(self.refresh_all_data)

            print("🟢 Показываем окно...")
            self._settings_window.show()

        except Exception as e:
            print(f"🔴 ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.show_notification(f"Ошибка: {e}", error=True)

    def refresh_all_data(self):
        """Полная перезагрузка данных после закрытия окна настроек"""
        print("🔄 Полная перезагрузка данных...")

        branches = self.db.get_all_branches()
        print(f"   Загружено филиалов: {len(branches)}")

        branch_combos = [
            self.ui.comboBox_5,
            self.ui.comboBox_19,
            self.ui.comboBox_14
        ]

        for combo in branch_combos:
            if combo:
                current_data = combo.currentData()
                combo.clear()
                combo.addItem("Выберите филиал", None)
                for branch in branches:
                    combo.addItem(branch[1], branch[0])
                if current_data:
                    index = combo.findData(current_data)
                    if index >= 0:
                        combo.setCurrentIndex(index)

        employees = self.db.get_employees()
        print(f"   Загружено сотрудников: {len(employees)}")

        employee_combos_full = [
            self.ui.comboBox_8,
        ]

        if hasattr(self.ui, 'comboBox'):
            employee_combos_full.append(self.ui.comboBox)
        if hasattr(self.ui, 'comboBox_2'):
            employee_combos_full.append(self.ui.comboBox_2)

        for combo in employee_combos_full:
            if combo:
                current_data = combo.currentData()
                combo.clear()
                combo.addItem("Выберите сотрудника", None)
                for emp in employees:
                    combo.addItem(f"{emp[1]} ({emp[2]})", emp[0])
                if current_data:
                    index = combo.findData(current_data)
                    if index >= 0:
                        combo.setCurrentIndex(index)
                combo.update()
                combo.repaint()

        if hasattr(self.ui, 'comboBox_13'):
            combo = self.ui.comboBox_13
            current_data = combo.currentData()
            combo.clear()
            combo.addItem("Выберите сотрудника", None)
            for emp in employees:
                combo.addItem(emp[1], emp[0])
            if current_data:
                index = combo.findData(current_data)
                if index >= 0:
                    combo.setCurrentIndex(index)
            combo.update()
            combo.repaint()

        self.load_arrival_data()
        # Загружаем оборудование для распределения в тихом режиме (без диалога)
        self.load_distribution_equipment(silent=True)

        if self.current_room_id:
            self.load_room_equipment(self.current_room_id)

        QApplication.processEvents()

        print("✅ Данные обновлены")
        self.show_notification("Данные обновлены")

        self._settings_window = None

    def show_schema(self):
        if not PLANE_AVAILABLE:
            self.show_notification("Модуль схем не найден", error=True)
            return
        try:
            if hasattr(self, 'plane_window') and self.plane_window is not None:
                if self.plane_window.isVisible():
                    self.plane_window.raise_()
                    self.plane_window.activateWindow()
                    return
                else:
                    self.plane_window = None

            self.plane_window = PlaneWindow()
            self.plane_window.setParent(self, Qt.Window)
            self.plane_window.show()
        except Exception as e:
            self.show_notification(f"Ошибка открытия схемы: {e}", error=True)

    def show_reports_list(self):
        dlg = ReportsListDialog(self.db, self)
        dlg.exec()

    def setup_tabs(self):
        self.setup_arrival_tab()
        self.setup_inventory_tab()
        self.setup_distribution_tab()

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
        categories = [
            "Электроника", "Комплектующие", "Сетевое оборудование", "Расходные материалы",
            "Инструменты", "Мебель", "Медицинское оборудование", "Оргтехника", "Прочее"
        ]
        for cat in categories:
            combo.addItem(cat, cat)

    def load_types_to_combo(self, combo):
        if not combo:
            return
        combo.clear()
        combo.addItem("Все типы", None)
        types = [
            "Телевизор", "SSD", "Процессор", "Материнская плата", "Оперативная память",
            "Блок питания", "Корпус", "Кулер", "Жёсткий диск", "Видеокарта",
            "Звуковая карта", "Сетевая карта", "Кабель HDMI", "Кабель VGA", "Кабель USB",
            "Витая пара", "Хомут", "Болт", "Гайка", "Шуруп",
            "Дюбель", "Отвёртка", "Пассатижи", "Мультиметр", "Принтер",
            "Сканер", "Копир", "Факс", "МФУ", "ИБП",
            "Сервер", "Коммутатор", "Маршрутизатор", "Патч-панель", "Розетка",
            "Сетевой фильтр", "Удлинитель", "Батарейка", "Аккумулятор", "Зарядное устройство",
            "Мышь", "Клавиатура", "Наушники", "Микрофон", "Веб-камера",
            "Колонки", "Монитор", "Ноутбук", "Планшет", "Смартфон",
            "Часы", "Флешка", "Внешний диск", "Оптический привод", "Картридер",
            "Тонер-картридж", "Бумага А4", "Ручка", "Карандаш", "Степлер",
            "Дырокол", "Папка", "Скоросшиватель", "Файл", "Лоток для бумаг",
            "Кресло", "Стол", "Шкаф", "Тумба", "Вешалка",
            "Кулер для воды", "Микроволновка", "Чайник", "Холодильник", "Кондиционер",
            "Обогреватель", "Вентилятор", "Лампа", "Светильник", "Датчик движения",
            "Датчик дыма", "Огнетушитель", "Аптечка", "Табличка", "Указатель",
            "Стенд", "Доска", "Маркер", "Мел", "Губка",
            "Тряпка", "Ведро", "Швабра", "Совок", "Пакет",
            "Перчатки", "Маска", "Халат", "Бахилы", "Шапочка",
            "Очки защитные", "Наушники защитные", "Респиратор", "Фартук", "Нарукавники",
            "Футболка", "Кепка", "Бейдж", "Брелок", "Значок",
            "Медаль", "Грамота", "Диплом", "Сертификат", "Благодарность",
            "Письмо", "Конверт", "Открытка", "Календарь", "Ежедневник",
            "Блокнот", "Записная книжка", "Папка-регистратор", "Разделитель", "Вкладка",
            "Стикер", "Закладка", "Скрепка", "Кнопка", "Булавка",
            "Резинка", "Ластик", "Точилка", "Линейка", "Транспортир",
            "Циркуль", "Лекало", "Трафарет", "Штамп", "Печать",
            "Штемпельная подушка", "Краска", "Тонер", "Чернила", "Плёнка",
            "Бумага для этикеток", "Термоэтикетки", "Термолента", "Чековая лента", "Диск CD",
            "Диск DVD", "Диск Blu-ray", "Дискета", "Кассета", "Карта памяти",
            "USB-модем", "Wi-Fi адаптер", "Bluetooth-адаптер", "GSM-антенна", "Спутниковая антенна",
            "Коаксиальный кабель", "Оптоволокно", "Коннектор", "Клемма", "Клеммник"
        ]
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

    def load_initial_data(self):
        self.load_branches_to_combo(self.ui.comboBox_5)
        self.load_employees_to_combo(self.ui.comboBox_8)

        if hasattr(self.ui, 'comboBox_19'):
            self.load_branches_to_combo(self.ui.comboBox_19)
        if hasattr(self.ui, 'comboBox'):
            self.load_employees_to_combo(self.ui.comboBox)
        if hasattr(self.ui, 'comboBox_2'):
            self.load_employees_to_combo(self.ui.comboBox_2)

        self.load_employees_with_position(self.ui.comboBox_13)
        self.load_branches_to_combo(self.ui.comboBox_14)

        self.load_categories_to_combo(self.ui.comboBox_9)
        self.load_types_to_combo(self.ui.comboBox_10)

        if hasattr(self.ui, 'dateTimeEdit'):
            self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        if hasattr(self.ui, 'textEdit'):
            self.ui.textEdit.setPlaceholderText("🔍 Поиск по названию, категории, типу, серийному номеру...")
            self.ui.textEdit.clear()
            self.ui.textEdit.textChanged.connect(self.filter_arrival_table)

    def setup_arrival_tab(self):
        self.load_branches_to_combo(self.ui.comboBox_5)
        self.load_employees_to_combo(self.ui.comboBox_8)

        self.ui.tableWidget.setColumnCount(14)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "ID", "Название", "Категория", "Тип", "Модель", "Производитель",
            "Серийный №", "Инв. №", "Кол-во", "Цена", "Дата пост.", "Статус", "Инфо", "Действия"
        ])

        self.ui.tableWidget.setColumnHidden(0, True)

        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(False)

        self.ui.tableWidget.setColumnWidth(1, 180)
        self.ui.tableWidget.setColumnWidth(2, 120)
        self.ui.tableWidget.setColumnWidth(3, 120)
        self.ui.tableWidget.setColumnWidth(4, 120)
        self.ui.tableWidget.setColumnWidth(5, 150)
        self.ui.tableWidget.setColumnWidth(6, 130)
        self.ui.tableWidget.setColumnWidth(7, 100)
        self.ui.tableWidget.setColumnWidth(8, 70)
        self.ui.tableWidget.setColumnWidth(9, 100)
        self.ui.tableWidget.setColumnWidth(10, 100)
        self.ui.tableWidget.setColumnWidth(11, 100)
        self.ui.tableWidget.setColumnWidth(12, 60)
        self.ui.tableWidget.setColumnWidth(13, 100)

        self.ui.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.tableWidget.setSelectionMode(QTableWidget.MultiSelection)

        if hasattr(self.ui, 'pushButton_5'):
            self.ui.pushButton_5.clicked.connect(self.export_arrival_pdf)
        if hasattr(self.ui, 'pushButton_2'):
            self.ui.pushButton_2.clicked.connect(self.cancel_arrival)
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.save_arrival)
        if hasattr(self.ui, 'pushButton_16'):
            self.ui.pushButton_16.clicked.connect(self.add_arrival_position)
        if hasattr(self.ui, 'pushButton_7'):
            self.ui.pushButton_7.clicked.connect(self.save_arrival)
        if hasattr(self.ui, 'pushButton_9'):
            self.ui.pushButton_9.clicked.connect(self.delete_selected_arrival)

        if hasattr(self.ui, 'lineEdit_15'):
            self.ui.lineEdit_15.setToolTip("Введите название оборудования")
        if hasattr(self.ui, 'lineEdit_18'):
            self.ui.lineEdit_18.setToolTip("Введите серийный номер")
        if hasattr(self.ui, 'lineEdit_19'):
            self.ui.lineEdit_19.setToolTip("Введите инвентарный номер (если есть)")

        for widget in [self.ui.lineEdit_15, self.ui.lineEdit_18, self.ui.lineEdit_19,
                       self.ui.lineEdit_5, self.ui.lineEdit_6]:
            if widget:
                widget.focusInEvent = lambda event, w=widget: self.clear_validation(w) or QLineEdit.focusInEvent(w, event)

        self.load_arrival_data()

    def load_arrival_data(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT
                               equipment_id, name, category, type,
                               COALESCE(model, '') as model,
                               COALESCE(manufacturer, '') as manufacturer,
                               serial_number,
                               COALESCE(inventory_number, '') as inventory_number,
                               quantity, price, date_incoming,
                               COALESCE(status, 'in_use') as status
                           FROM equipment
                           ORDER BY equipment_id DESC
                           """)
            rows = cursor.fetchall()
            conn.close()

            self.all_arrival_data = rows
            self.display_arrival_data(rows)

        except Exception as e:
            print(f"Ошибка загрузки поступлений: {e}")
            self.all_arrival_data = []

    def display_arrival_data(self, rows):
        self.ui.tableWidget.setRowCount(0)
        for i, row in enumerate(rows):
            self.ui.tableWidget.insertRow(i)

            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(row[1] or ""))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(row[2] or ""))
            self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(row[3] or ""))
            self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(row[4] or ""))
            self.ui.tableWidget.setItem(i, 5, QTableWidgetItem(row[5] or ""))
            self.ui.tableWidget.setItem(i, 6, QTableWidgetItem(row[6] or ""))
            self.ui.tableWidget.setItem(i, 7, QTableWidgetItem(row[7] or ""))
            self.ui.tableWidget.setItem(i, 8, QTableWidgetItem(str(row[8])))
            self.ui.tableWidget.setItem(i, 9, QTableWidgetItem(str(row[9])))
            self.ui.tableWidget.setItem(i, 10, QTableWidgetItem(row[10] or ""))

            status_text = "В наличии" if row[11] == 'in_use' else "Списано" if row[11] == 'written_off' else row[11]
            self.ui.tableWidget.setItem(i, 11, QTableWidgetItem(status_text))

            btn_info = QPushButton("📄")
            btn_info.setToolTip("Информация о поступлении")
            btn_info.setMaximumWidth(40)
            btn_info.clicked.connect(lambda checked, r=i: self.show_arrival_info(r))
            self.ui.tableWidget.setCellWidget(i, 12, btn_info)

            btn_delete = QPushButton("Удалить")
            btn_delete.setToolTip("Удалить позицию")
            btn_delete.clicked.connect(lambda checked, r=i: self.delete_single_arrival_row(r))
            self.ui.tableWidget.setCellWidget(i, 13, btn_delete)

    def filter_arrival_table(self):
        if not hasattr(self, 'all_arrival_data'):
            return

        search_text = self.ui.textEdit.toPlainText().lower().strip()

        if not search_text:
            self.display_arrival_data(self.all_arrival_data)
            return

        filtered_rows = []
        for row in self.all_arrival_data:
            searchable = ' '.join([
                str(row[1] or ''),
                str(row[2] or ''),
                str(row[3] or ''),
                str(row[4] or ''),
                str(row[5] or ''),
                str(row[6] or ''),
                str(row[7] or ''),
                str(row[8] or ''),
                str(row[9] or ''),
                str(row[10] or ''),
                str(row[11] or ''),
            ]).lower()

            if search_text in searchable:
                filtered_rows.append(row)

        self.display_arrival_data(filtered_rows)
        self.show_notification(f"Найдено записей: {len(filtered_rows)}")

    def show_arrival_info(self, row):
        item_id = self.ui.tableWidget.item(row, 0)
        if not item_id:
            return

        equip_id = int(item_id.text())

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT name, category, type, model, manufacturer, serial_number,
                                  inventory_number, quantity, price, date_incoming, supplier,
                                  phone_supplier, email_supplier, notes
                           FROM equipment
                           WHERE equipment_id = ?
                           """, (equip_id,))
            equip = cursor.fetchone()
        finally:
            conn.close()

        if not equip:
            return

        arrival_data = {
            'name': equip[0] if equip[0] else "",
            'order_number': "",
            'description': equip[13] if equip[13] else "",
            'date': equip[9] if equip[9] else "",
            'branch_name': "",
            'employee_name': "",
            'doc_number': "",
            'supplier_name': equip[10] if equip[10] else "",
            'supplier_inn': "",
            'supplier_phone': equip[11] if equip[11] else "",
            'supplier_email': equip[12] if equip[12] else "",
            'total_amount': float(equip[8] or 0) * float(equip[7] or 1),
            'waybill_number': "",
            'contract_number': "",
            'notes': equip[13] if equip[13] else "",
        }

        dlg = ArrivalInfoDialog(arrival_data, self)
        dlg.exec()

    def delete_single_arrival_row(self, row):
        item_id = self.ui.tableWidget.item(row, 0)
        if not item_id:
            return
        equip_id = int(item_id.text())
        dlg = ConfirmationDialog("Удалить эту позицию из базы данных?", self)
        if dlg.exec() == QDialog.Accepted:
            self.delete_equipment_by_id(equip_id)
            self.ui.tableWidget.removeRow(row)
            self.load_arrival_data()
            self.show_notification("Позиция удалена")

    def delete_equipment_by_id(self, equip_id):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM equipment WHERE equipment_id = ?", (equip_id,))
            conn.commit()
        except Exception as e:
            self.show_notification(f"Не удалось удалить из БД: {e}", error=True)
        finally:
            conn.close()

    def add_arrival_position(self):
        fields_to_check = {}
        if hasattr(self.ui, 'lineEdit_15'):
            fields_to_check[self.ui.lineEdit_15] = "Название"
        if hasattr(self.ui, 'lineEdit_18'):
            fields_to_check[self.ui.lineEdit_18] = "Серийный номер"

        first_empty = self.validate_required_fields(fields_to_check)
        if first_empty:
            self.show_notification("Заполните обязательные поля (название и серийный номер)", error=True)
            first_empty.setFocus()
            return

        data = {
            'name': self.ui.lineEdit_15.text() if hasattr(self.ui, 'lineEdit_15') else "",
            'category': self.ui.comboBox_9.currentText() if hasattr(self.ui, 'comboBox_9') else "",
            'type': self.ui.comboBox_10.currentText() if hasattr(self.ui, 'comboBox_10') else "",
            'model': self.ui.lineEdit_16.text() if hasattr(self.ui, 'lineEdit_16') else "",
            'manufacturer': self.ui.lineEdit_17.text() if hasattr(self.ui, 'lineEdit_17') else "",
            'quantity': self.ui.spinBox_2.value() if hasattr(self.ui, 'spinBox_2') else 1,
            'serial_number': self.ui.lineEdit_18.text() if hasattr(self.ui, 'lineEdit_18') else "",
            'inventory_number': self.ui.lineEdit_19.text() if hasattr(self.ui, 'lineEdit_19') else "",
            'supplier': self.ui.lineEdit_7.text() if hasattr(self.ui, 'lineEdit_7') else "",
            'price': self.ui.doubleSpinBox.value() if hasattr(self.ui, 'doubleSpinBox') else 0,
            'date_incoming': self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd") if hasattr(self.ui, 'dateTimeEdit') else datetime.now().strftime("%Y-%m-%d"),
            'phone_supplier': self.ui.lineEdit_9.text() if hasattr(self.ui, 'lineEdit_9') else "",
            'email_supplier': self.ui.lineEdit_10.text() if hasattr(self.ui, 'lineEdit_10') else "",
            'notes': self.ui.plainTextEdit.toPlainText() if hasattr(self.ui, 'plainTextEdit') else ""
        }

        try:
            equip_id = self.db.add_equipment(data)
            self.load_arrival_data()
            self.load_distribution_equipment(silent=True)
            self.clear_arrival_form()
            self.show_notification(f"Позиция добавлена (ID: {equip_id})")
            QMessageBox.information(self, "Успех", f"Позиция добавлена (ID: {equip_id})")
        except Exception as e:
            self.show_notification(f"Не удалось сохранить: {e}", error=True)

    def clear_arrival_form(self):
        if hasattr(self.ui, 'lineEdit_15'):
            self.ui.lineEdit_15.clear()
        if hasattr(self.ui, 'lineEdit_16'):
            self.ui.lineEdit_16.clear()
        if hasattr(self.ui, 'lineEdit_17'):
            self.ui.lineEdit_17.clear()
        if hasattr(self.ui, 'lineEdit_18'):
            self.ui.lineEdit_18.clear()
        if hasattr(self.ui, 'lineEdit_19'):
            self.ui.lineEdit_19.clear()
        if hasattr(self.ui, 'spinBox_2'):
            self.ui.spinBox_2.setValue(1)
        if hasattr(self.ui, 'doubleSpinBox'):
            self.ui.doubleSpinBox.setValue(0)

    def delete_selected_arrival(self):
        selected_rows = set()
        for item in self.ui.tableWidget.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            self.show_notification("Выберите позиции для удаления", error=True)
            return

        dlg = ConfirmationDialog(f"Удалить {len(selected_rows)} позиций из базы данных?", self)
        if dlg.exec() == QDialog.Accepted:
            for row in sorted(selected_rows, reverse=True):
                item_id = self.ui.tableWidget.item(row, 0)
                if item_id:
                    self.delete_equipment_by_id(int(item_id.text()))
                self.ui.tableWidget.removeRow(row)
            self.load_arrival_data()
            self.load_distribution_equipment(silent=True)
            self.show_notification(f"Удалено {len(selected_rows)} позиций")

    def export_arrival_pdf(self):
        if not PDF_AVAILABLE:
            self.show_notification("Библиотека ReportLab не установлена. Установите: pip install reportlab", error=True)
            return

        if self.ui.tableWidget.rowCount() == 0:
            self.show_notification("Нет данных для выгрузки", error=True)
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить PDF отчет", "", "PDF файлы (*.pdf)")
        if not file_path:
            return

        try:
            c = canvas.Canvas(file_path, pagesize=landscape(A4))
            width, height = landscape(A4)

            global FONT_NAME, FONT_REGISTERED

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 14)
            else:
                c.setFont("Helvetica", 14)

            c.drawString(30, height - 30, "ВЫГРУЗКА ИЗ БАЗЫ ДАННЫХ")

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 10)
            else:
                c.setFont("Helvetica", 10)
            c.drawString(30, height - 50, f"Дата: {QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm')}")

            y = height - 80

            if FONT_REGISTERED:
                c.setFont(f"{FONT_NAME}-Bold", 9)
            else:
                c.setFont("Helvetica-Bold", 9)

            headers = ["№", "Название", "Категория", "Тип", "Модель", "Производитель", "Кол-во", "Цена", "Сумма"]
            x_positions = [30, 50, 180, 280, 380, 480, 580, 640, 700]

            for i, header in enumerate(headers):
                c.drawString(x_positions[i], y, header)
            y -= 15

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 8)
            else:
                c.setFont("Helvetica", 8)

            total_sum = 0
            for row in range(self.ui.tableWidget.rowCount()):
                if y < 50:
                    c.showPage()
                    y = height - 50
                    if FONT_REGISTERED:
                        c.setFont(FONT_NAME, 8)
                    else:
                        c.setFont("Helvetica", 8)

                num = str(row+1)
                name = self.ui.tableWidget.item(row, 1).text() if self.ui.tableWidget.item(row, 1) else ""
                cat = self.ui.tableWidget.item(row, 2).text() if self.ui.tableWidget.item(row, 2) else ""
                type_name = self.ui.tableWidget.item(row, 3).text() if self.ui.tableWidget.item(row, 3) else ""
                model = self.ui.tableWidget.item(row, 4).text() if self.ui.tableWidget.item(row, 4) else ""
                manufacturer = self.ui.tableWidget.item(row, 5).text() if self.ui.tableWidget.item(row, 5) else ""
                qty = self.ui.tableWidget.item(row, 8).text() if self.ui.tableWidget.item(row, 8) else "0"
                price = self.ui.tableWidget.item(row, 9).text() if self.ui.tableWidget.item(row, 9) else "0"

                try:
                    qty_val = int(qty)
                    price_val = float(price)
                    sum_val = qty_val * price_val
                    total_sum += sum_val
                except:
                    sum_val = 0

                c.drawString(x_positions[0], y, num)
                c.drawString(x_positions[1], y, name[:25])
                c.drawString(x_positions[2], y, cat[:15])
                c.drawString(x_positions[3], y, type_name[:15])
                c.drawString(x_positions[4], y, model[:15])
                c.drawString(x_positions[5], y, manufacturer[:15])
                c.drawString(x_positions[6], y, qty)
                c.drawString(x_positions[7], y, f"{price_val:.2f}" if 'price_val' in locals() else price)
                c.drawString(x_positions[8], y, f"{sum_val:.2f}")
                y -= 12

            y -= 10
            if FONT_REGISTERED:
                c.setFont(f"{FONT_NAME}-Bold", 10)
            else:
                c.setFont("Helvetica-Bold", 10)
            c.drawString(x_positions[6], y, f"ИТОГО: {total_sum:.2f} руб.")

            c.save()
            self.show_notification(f"PDF отчет сохранен: {file_path}")
            QMessageBox.information(self, "Успех", f"PDF отчет сохранен:\n{file_path}")

        except Exception as e:
            self.show_notification(f"Не удалось создать PDF: {e}", error=True)
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать PDF:\n{str(e)}")

    def cancel_arrival(self):
        dlg = ConfirmationDialog("Отменить ввод данных?", self)
        if dlg.exec() == QDialog.Accepted:
            self.clear_arrival_form()
            self.show_notification("Ввод отменен")

    def save_arrival(self):
        name = self.ui.lineEdit_5.text() if hasattr(self.ui, 'lineEdit_5') else ""
        order_number = self.ui.lineEdit_6.text() if hasattr(self.ui, 'lineEdit_6') else ""
        description = self.ui.textEdit_4.toPlainText() if hasattr(self.ui, 'textEdit_4') else ""
        branch_id = self.ui.comboBox_5.currentData() if hasattr(self.ui, 'comboBox_5') else None
        employee_id = self.ui.comboBox_8.currentData() if hasattr(self.ui, 'comboBox_8') else None
        date = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        doc_number = self.ui.lineEdit_2.text() if hasattr(self.ui, 'lineEdit_2') else ""
        supplier_name = self.ui.lineEdit_7.text() if hasattr(self.ui, 'lineEdit_7') else ""
        supplier_inn = self.ui.lineEdit_8.text() if hasattr(self.ui, 'lineEdit_8') else ""
        supplier_phone = self.ui.lineEdit_9.text() if hasattr(self.ui, 'lineEdit_9') else ""
        supplier_email = self.ui.lineEdit_10.text() if hasattr(self.ui, 'lineEdit_10') else ""

        try:
            total_amount = float(self.ui.lineEdit_11.text() or 0) if hasattr(self.ui, 'lineEdit_11') else 0
        except:
            total_amount = 0

        waybill_number = self.ui.lineEdit_12.text() if hasattr(self.ui, 'lineEdit_12') else ""
        contract_number = self.ui.lineEdit_13.text() if hasattr(self.ui, 'lineEdit_13') else ""
        notes = self.ui.plainTextEdit.toPlainText() if hasattr(self.ui, 'plainTextEdit') else ""

        if not name.strip() and not order_number.strip() and not description.strip() and not supplier_name.strip():
            self.show_notification("Нет данных для сохранения. Заполните хотя бы название поступления", error=True)
            self.ui.lineEdit_5.setStyleSheet("border: 2px solid red;")
            self.ui.lineEdit_5.setFocus()
            return

        if not name.strip():
            self.ui.lineEdit_5.setStyleSheet("border: 2px solid red;")
            self.ui.lineEdit_5.setFocus()
            self.show_notification("Введите название поступления", error=True)
            return
        else:
            self.ui.lineEdit_5.setStyleSheet("")

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO arrivals (
                               name, order_number, description, branch_id, employee_id, date,
                               doc_number, supplier_name, supplier_inn, supplier_phone, supplier_email,
                               total_amount, waybill_number, contract_number, notes
                           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           """, (name, order_number, description, branch_id, employee_id, date,
                                 doc_number, supplier_name, supplier_inn, supplier_phone, supplier_email,
                                 total_amount, waybill_number, contract_number, notes))
            conn.commit()
            arrival_id = cursor.lastrowid
            self.show_notification(f"Поступление сохранено (ID: {arrival_id})")
            QMessageBox.information(self, "Успех", f"Поступление сохранено (ID: {arrival_id})")
        except Exception as e:
            self.show_notification(f"Не удалось сохранить поступление: {e}", error=True)
        finally:
            conn.close()

    def setup_inventory_tab(self):
        if hasattr(self.ui, 'comboBox_19'):
            self.load_branches_to_combo(self.ui.comboBox_19)

        if hasattr(self.ui, 'comboBox'):
            self.load_employees_to_combo(self.ui.comboBox)
        if hasattr(self.ui, 'comboBox_2'):
            self.load_employees_to_combo(self.ui.comboBox_2)

        if hasattr(self.ui, 'comboBox_19'):
            self.ui.comboBox_19.currentIndexChanged.connect(self.on_branch_changed_inventory)
        if hasattr(self.ui, 'comboBox_7'):
            self.ui.comboBox_7.currentIndexChanged.connect(self.on_room_changed_inventory)
        if hasattr(self.ui, 'spinBox_3'):
            self.ui.spinBox_3.valueChanged.connect(self.on_floor_changed_inventory)

        if hasattr(self.ui, 'tableView'):
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels([
                "ID", "Название", "Категория", "Тип", "Модель", "Производитель", "Кол-во", "Цена",
                "Серийный №", "Инв. №", "Дата поступления", "Поставщик", "Статус"
            ])
            self.ui.tableView.setModel(model)
            self.ui.tableView.setColumnHidden(0, True)

            header = self.ui.tableView.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Interactive)
            header.setStretchLastSection(False)
            self.ui.tableView.setColumnWidth(1, 200)
            self.ui.tableView.setColumnWidth(2, 120)
            self.ui.tableView.setColumnWidth(3, 120)
            self.ui.tableView.setColumnWidth(4, 120)
            self.ui.tableView.setColumnWidth(5, 150)
            self.ui.tableView.setColumnWidth(6, 70)
            self.ui.tableView.setColumnWidth(7, 100)
            self.ui.tableView.setColumnWidth(8, 130)
            self.ui.tableView.setColumnWidth(9, 100)
            self.ui.tableView.setColumnWidth(10, 120)
            self.ui.tableView.setColumnWidth(11, 150)
            self.ui.tableView.setColumnWidth(12, 100)

        if hasattr(self.ui, 'comboBox_12'):
            self.ui.comboBox_12.currentIndexChanged.connect(self.apply_inventory_filters)
        if hasattr(self.ui, 'comboBox_11'):
            self.ui.comboBox_11.currentIndexChanged.connect(self.apply_inventory_filters)
        if hasattr(self.ui, 'lineEdit_20'):
            self.ui.lineEdit_20.textChanged.connect(self.apply_inventory_filters)
        if hasattr(self.ui, 'textEdit_3'):
            self.ui.textEdit_3.setPlaceholderText("Поиск по названию, модели, типу...")
            self.ui.textEdit_3.clear()
            self.ui.textEdit_3.textChanged.connect(self.apply_inventory_filters)

        self.load_categories_to_combo(self.ui.comboBox_12)
        self.load_types_to_combo(self.ui.comboBox_11)

        if hasattr(self.ui, 'pushButton_11'):
            self.ui.pushButton_11.clicked.connect(self.export_inventory_room_report_pdf)
        if hasattr(self.ui, 'pushButton_14'):
            self.ui.pushButton_14.clicked.connect(self.export_inventory_full_report_pdf)

    def on_branch_changed_inventory(self):
        branch_id = self.ui.comboBox_19.currentData() if hasattr(self.ui, 'comboBox_19') else None
        if branch_id:
            branch = self.db.get_branch(branch_id)
            if branch and hasattr(self.ui, 'spinBox_3'):
                self.ui.spinBox_3.setMaximum(branch[2])

    def on_floor_changed_inventory(self):
        branch_id = self.ui.comboBox_19.currentData() if hasattr(self.ui, 'comboBox_19') else None
        floor = self.ui.spinBox_3.value() if hasattr(self.ui, 'spinBox_3') else 1
        if branch_id and floor and hasattr(self.ui, 'comboBox_7'):
            self.load_rooms_to_combo(self.ui.comboBox_7, branch_id, floor)

    def on_room_changed_inventory(self):
        room_id = self.ui.comboBox_7.currentData() if hasattr(self.ui, 'comboBox_7') else None
        if not room_id:
            return

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT equipment_id, name, category, type, model, manufacturer,
                                  quantity, price, serial_number, inventory_number, date_incoming,
                                  supplier, status
                           FROM equipment
                           WHERE room_id = ?
                           ORDER BY name
                           """, (room_id,))
            rows = cursor.fetchall()
        finally:
            conn.close()

        model = self.ui.tableView.model()
        if model:
            model.removeRows(0, model.rowCount())
            for row in rows:
                items = [
                    QStandardItem(str(row[0])),
                    QStandardItem(row[1]),
                    QStandardItem(row[2] if row[2] else ""),
                    QStandardItem(row[3] if row[3] else ""),
                    QStandardItem(row[4] if row[4] else ""),
                    QStandardItem(row[5] if row[5] else ""),
                    QStandardItem(str(row[6])),
                    QStandardItem(str(row[7])),
                    QStandardItem(row[8] if row[8] else ""),
                    QStandardItem(row[9] if row[9] else ""),
                    QStandardItem(row[10] if row[10] else ""),
                    QStandardItem(row[11] if row[11] else ""),
                    QStandardItem(row[12] if row[12] else "")
                ]
                model.appendRow(items)

    def apply_inventory_filters(self):
        category = self.ui.comboBox_12.currentData() if hasattr(self.ui, 'comboBox_12') else None
        type_ = self.ui.comboBox_11.currentData() if hasattr(self.ui, 'comboBox_11') else None
        if hasattr(self.ui, 'lineEdit_20'):
            name_filter = self.ui.lineEdit_20.text().lower().strip()
        elif hasattr(self.ui, 'textEdit_3'):
            name_filter = self.ui.textEdit_3.toPlainText().lower().strip()
        else:
            name_filter = ""

        model = self.ui.tableView.model()
        if not model:
            return

        for row in range(model.rowCount()):
            show = True
            if category and category != "Все категории":
                cat_item = model.item(row, 2)
                if cat_item and cat_item.text() != category:
                    show = False
            if show and type_ and type_ != "Все типы":
                type_item = model.item(row, 3)
                if type_item and type_item.text() != type_:
                    show = False
            if show and name_filter:
                name_item = model.item(row, 1)
                if name_item and name_filter not in name_item.text().lower():
                    show = False
            self.ui.tableView.setRowHidden(row, not show)

    def export_inventory_room_report_pdf(self):
        if not PDF_AVAILABLE:
            self.show_notification("Библиотека ReportLab не установлена", error=True)
            return

        room_id = self.ui.comboBox_7.currentData() if hasattr(self.ui, 'comboBox_7') else None
        if not room_id:
            self.show_notification("Выберите комнату", error=True)
            return

        room = self.db.get_room(room_id)
        if not room:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет по инвентаризации",
            f"Инвентаризация_{room[1]}.pdf", "PDF файлы (*.pdf)"
        )
        if not file_path:
            return

        try:
            c = canvas.Canvas(file_path, pagesize=landscape(A4))
            width, height = landscape(A4)

            global FONT_NAME, FONT_REGISTERED

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 14)
            else:
                c.setFont("Helvetica", 14)

            c.drawString(30, height - 30, f"ИНВЕНТАРИЗАЦИЯ КОМНАТЫ: {room[1]}")

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 10)
            else:
                c.setFont("Helvetica", 10)

            y = height - 60
            c.drawString(30, y, f"Название: {room[2]}")
            y -= 15
            c.drawString(30, y, f"Этаж: {room[3]}")
            y -= 15
            c.drawString(30, y, f"Вместимость: {room[4]} чел.")
            y -= 15
            c.drawString(30, y, f"Площадь: {room[8]} м²")
            y -= 15
            c.drawString(30, y, f"Столов: {room[5]}, Стульев: {room[6]}, Розеток: {room[7]}")
            y -= 15
            c.drawString(30, y, f"Дата: {QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm')}")
            y -= 25

            if FONT_REGISTERED:
                c.setFont(f"{FONT_NAME}-Bold", 9)
            else:
                c.setFont("Helvetica-Bold", 9)

            headers = ["№", "Наименование", "Модель", "Производитель", "Поставщик", "Кол-во", "Цена", "Сумма"]
            x_pos = [30, 50, 200, 300, 400, 500, 560, 620]

            for i, header in enumerate(headers):
                c.drawString(x_pos[i], y, header)
            y -= 15

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 8)
            else:
                c.setFont("Helvetica", 8)

            model = self.ui.tableView.model()
            total_sum = 0
            visible_rows = 0

            if model:
                for row in range(model.rowCount()):
                    if not self.ui.tableView.isRowHidden(row):
                        visible_rows += 1
                        if y < 50:
                            c.showPage()
                            y = height - 50
                            if FONT_REGISTERED:
                                c.setFont(FONT_NAME, 8)
                            else:
                                c.setFont("Helvetica", 8)

                        name = model.item(row, 1).text() if model.item(row, 1) else ""
                        model_name = model.item(row, 4).text() if model.item(row, 4) else ""
                        manufacturer = model.item(row, 5).text() if model.item(row, 5) else ""
                        supplier = model.item(row, 11).text() if model.item(row, 11) else ""
                        qty = model.item(row, 6).text() if model.item(row, 6) else "0"
                        price = model.item(row, 7).text() if model.item(row, 7) else "0"

                        try:
                            qty_val = int(qty)
                            price_val = float(price)
                            sum_val = qty_val * price_val
                            total_sum += sum_val
                        except:
                            sum_val = 0

                        c.drawString(x_pos[0], y, str(visible_rows))
                        c.drawString(x_pos[1], y, name[:20])
                        c.drawString(x_pos[2], y, model_name[:15])
                        c.drawString(x_pos[3], y, manufacturer[:15])
                        c.drawString(x_pos[4], y, supplier[:15])
                        c.drawString(x_pos[5], y, qty)
                        c.drawString(x_pos[6], y, f"{price_val:.2f}" if 'price_val' in locals() else price)
                        c.drawString(x_pos[7], y, f"{sum_val:.2f}")
                        y -= 12

            y -= 10
            if FONT_REGISTERED:
                c.setFont(f"{FONT_NAME}-Bold", 10)
            else:
                c.setFont("Helvetica-Bold", 10)
            c.drawString(x_pos[5], y, f"ИТОГО: {total_sum:.2f} руб.")

            c.save()
            self.show_notification(f"PDF отчет сохранен: {file_path}")
            QMessageBox.information(self, "Успех", f"PDF отчет сохранен:\n{file_path}")

        except Exception as e:
            self.show_notification(f"Ошибка создания PDF: {e}", error=True)
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать PDF:\n{str(e)}")

    def export_inventory_full_report_pdf(self):
        if not PDF_AVAILABLE:
            self.show_notification("Библиотека ReportLab не установлена", error=True)
            return

        branch_id = self.ui.comboBox_19.currentData() if hasattr(self.ui, 'comboBox_19') else None
        if not branch_id:
            self.show_notification("Выберите филиал", error=True)
            return

        branch = self.db.get_branch(branch_id)
        if not branch:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить полный отчет",
            f"Инвентаризация_{branch['name']}.pdf", "PDF файлы (*.pdf)"
        )
        if not file_path:
            return

        try:
            c = canvas.Canvas(file_path, pagesize=landscape(A4))
            width, height = landscape(A4)

            page_height = height

            global FONT_NAME, FONT_REGISTERED

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 14)
            else:
                c.setFont("Helvetica", 14)

            c.drawString(30, page_height - 30, f"ПОЛНЫЙ ОТЧЕТ ПО ФИЛИАЛУ: {branch['name']}")

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 10)
            else:
                c.setFont("Helvetica", 10)

            c.drawString(30, page_height - 50, f"Адрес: {branch['address']}")
            c.drawString(30, page_height - 65, f"Дата: {QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm')}")

            y_position = page_height - 100
            total_equipment = 0
            total_value = 0

            for floor in range(1, branch['floors_count'] + 1):
                if y_position < 100:
                    c.showPage()
                    y_position = page_height - 50
                    if FONT_REGISTERED:
                        c.setFont(FONT_NAME, 10)
                    else:
                        c.setFont("Helvetica", 10)

                if FONT_REGISTERED:
                    c.setFont(f"{FONT_NAME}-Bold", 12)
                else:
                    c.setFont("Helvetica-Bold", 12)
                c.drawString(30, y_position, f"Этаж {floor}")
                y_position -= 20

                rooms = self.db.get_rooms_by_branch_and_floor(branch_id, floor)

                if not rooms:
                    if FONT_REGISTERED:
                        c.setFont(FONT_NAME, 9)
                    else:
                        c.setFont("Helvetica", 9)
                    c.drawString(30, y_position, "На этаже нет комнат")
                    y_position -= 20
                    continue

                for room in rooms:
                    if y_position < 80:
                        c.showPage()
                        y_position = page_height - 50
                        if FONT_REGISTERED:
                            c.setFont(FONT_NAME, 10)
                        else:
                            c.setFont("Helvetica", 10)

                    if FONT_REGISTERED:
                        c.setFont(f"{FONT_NAME}-Bold", 10)
                    else:
                        c.setFont("Helvetica-Bold", 10)
                    c.drawString(30, y_position, f"Комната {room[1]} - {room[2]}")
                    y_position -= 15

                    conn = self.db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                                   SELECT name, category, type, model, manufacturer, quantity, price, supplier
                                   FROM equipment
                                   WHERE room_id = ?
                                   ORDER BY name
                                   """, (room[0],))
                    equipment = cursor.fetchall()
                    conn.close()

                    if equipment:
                        if FONT_REGISTERED:
                            c.setFont(FONT_NAME, 8)
                        else:
                            c.setFont("Helvetica", 8)

                        headers = ["Название", "Модель", "Производитель", "Кол-во", "Цена", "Поставщик"]
                        x_pos = [40, 160, 260, 360, 420, 480]

                        y_temp = y_position - 3
                        for i, header in enumerate(headers):
                            c.drawString(x_pos[i], y_temp, header)
                        y_position -= 15

                        for eq in equipment:
                            if y_position < 40:
                                c.showPage()
                                y_position = page_height - 50
                                if FONT_REGISTERED:
                                    c.setFont(FONT_NAME, 8)
                                else:
                                    c.setFont("Helvetica", 8)

                            name = eq[0][:18] if len(eq[0]) > 18 else eq[0]
                            model = eq[3][:15] if eq[3] and len(eq[3]) > 15 else (eq[3] or "")
                            manufacturer = eq[4][:15] if eq[4] and len(eq[4]) > 15 else (eq[4] or "")
                            supplier = eq[7][:15] if eq[7] and len(eq[7]) > 15 else (eq[7] or "")

                            c.drawString(x_pos[0], y_position, name)
                            c.drawString(x_pos[1], y_position, model)
                            c.drawString(x_pos[2], y_position, manufacturer)
                            c.drawString(x_pos[3], y_position, str(eq[5]))
                            c.drawString(x_pos[4], y_position, f"{eq[6]:.2f}")
                            c.drawString(x_pos[5], y_position, supplier)
                            y_position -= 12

                            total_equipment += 1
                            try:
                                total_value += int(eq[5]) * float(eq[6])
                            except:
                                pass
                    else:
                        if FONT_REGISTERED:
                            c.setFont(FONT_NAME, 8)
                        else:
                            c.setFont("Helvetica", 8)
                        c.drawString(40, y_position, "  Нет оборудования")
                        y_position -= 12

                    y_position -= 5

                y_position -= 10

            c.showPage()
            if FONT_REGISTERED:
                c.setFont(f"{FONT_NAME}-Bold", 12)
            else:
                c.setFont("Helvetica-Bold", 12)
            c.drawString(30, page_height - 50, "ИТОГ ПО ФИЛИАЛУ:")

            if FONT_REGISTERED:
                c.setFont(FONT_NAME, 10)
            else:
                c.setFont("Helvetica", 10)
            c.drawString(30, page_height - 70, f"Всего единиц оборудования: {total_equipment}")
            c.drawString(30, page_height - 85, f"Общая стоимость: {total_value:.2f} руб.")

            c.save()
            self.show_notification(f"Полный отчет сохранен: {file_path}")
            QMessageBox.information(self, "Успех", f"Полный отчет сохранен:\n{file_path}")

        except Exception as e:
            self.show_notification(f"Ошибка создания PDF: {e}", error=True)
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать PDF:\n{str(e)}")

    def setup_distribution_tab(self):
        self.load_employees_with_position(self.ui.comboBox_13)
        self.load_branches_to_combo(self.ui.comboBox_14)

        if hasattr(self.ui, 'comboBox_14'):
            self.ui.comboBox_14.currentIndexChanged.connect(self.on_branch_changed_distribution)
        if hasattr(self.ui, 'spinBox_6'):
            self.ui.spinBox_6.valueChanged.connect(self.on_floor_changed_distribution)
        if hasattr(self.ui, 'comboBox_16'):
            self.ui.comboBox_16.currentIndexChanged.connect(self.on_room_changed_distribution)

        self.setup_right_panel()
        self.setup_distribution_table()

        if hasattr(self.ui, 'comboBox_17'):
            self.ui.comboBox_17.currentIndexChanged.connect(self.apply_distribution_filters)
        if hasattr(self.ui, 'comboBox_18'):
            self.ui.comboBox_18.currentIndexChanged.connect(self.apply_distribution_filters)
        if hasattr(self.ui, 'textEdit_2'):
            self.ui.textEdit_2.setPlaceholderText("Поиск по названию, модели, типу...")
            self.ui.textEdit_2.clear()
            self.ui.textEdit_2.textChanged.connect(self.apply_distribution_filters)

        self.load_categories_to_combo(self.ui.comboBox_17)
        self.load_types_to_combo(self.ui.comboBox_18)

        if hasattr(self.ui, 'pushButton_15'):
            self.ui.pushButton_15.clicked.connect(self.transfer_selected_items)
        if hasattr(self.ui, 'pushButton_17'):
            self.ui.pushButton_17.clicked.connect(self.remove_selected_room_equipment)
        if hasattr(self.ui, 'pushButton_8'):
            self.ui.pushButton_8.clicked.connect(self.save_all_distribution)
        if hasattr(self.ui, 'pushButton_9'):
            self.ui.pushButton_9.clicked.connect(self.delete_all_distribution)
        if hasattr(self.ui, 'pushButton_4'):
            self.ui.pushButton_4.clicked.connect(self.save_room_distribution)
        if hasattr(self.ui, 'pushButton_6'):
            self.ui.pushButton_6.clicked.connect(self.reset_room_distribution)
        if hasattr(self.ui, 'pushButton_10'):
            self.ui.pushButton_10.clicked.connect(self.export_final_report)

    def setup_distribution_table(self):
        self.distribution_model = QStandardItemModel()
        self.distribution_model.setHorizontalHeaderLabels([
            "Выбрать", "ID", "Доступно", "Перенести", "Название", "Категория", "Тип",
            "Модель", "Производитель", "Серийный №", "Инвентарный №", "Цена", "Дата поступления"
        ])
        self.ui.tableView_2.setModel(self.distribution_model)

        header = self.ui.tableView_2.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)

        self.ui.tableView_2.setColumnWidth(0, 60)
        self.ui.tableView_2.setColumnWidth(1, 0)
        self.ui.tableView_2.setColumnWidth(2, 80)
        self.ui.tableView_2.setColumnWidth(3, 100)
        self.ui.tableView_2.setColumnWidth(4, 180)
        self.ui.tableView_2.setColumnWidth(5, 100)
        self.ui.tableView_2.setColumnWidth(6, 100)
        self.ui.tableView_2.setColumnWidth(7, 120)
        self.ui.tableView_2.setColumnWidth(8, 120)
        self.ui.tableView_2.setColumnWidth(9, 130)
        self.ui.tableView_2.setColumnWidth(10, 100)
        self.ui.tableView_2.setColumnWidth(11, 100)
        self.ui.tableView_2.setColumnWidth(12, 120)

        self.ui.tableView_2.setColumnHidden(1, True)
        self.ui.tableView_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView_2.setSelectionMode(QAbstractItemView.MultiSelection)

    def load_distribution_equipment(self, silent=False):
        """Загружает оборудование для распределения"""
        try:
            rows = self.db.get_equipment_for_distribution()
            print(f"[DEBUG] Найдено оборудования для распределения: {len(rows)}")
            self.distribution_model.removeRows(0, self.distribution_model.rowCount())

            if len(rows) == 0 and not silent:
                # Показываем диалог только если не в тихом режиме
                reply = QMessageBox.question(self, "Нет оборудования",
                                             "На складе нет оборудования для распределения.\n\nХотите сбросить всё оборудование на склад?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    count = self.db.reset_equipment_to_stock()
                    if count > 0:
                        rows = self.db.get_equipment_for_distribution()
                        QMessageBox.information(self, "Успех", f"Сброшено {count} единиц оборудования")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось сбросить оборудование")
                        return
                else:
                    return

            for row in rows:
                items = []
                check_item = QStandardItem()
                check_item.setCheckable(True)
                check_item.setCheckState(Qt.Unchecked)
                check_item.setEditable(False)
                items.append(check_item)

                id_item = QStandardItem(str(row['equipment_id']))
                id_item.setEditable(False)
                items.append(id_item)

                qty_available = QStandardItem(str(row['quantity']))
                qty_available.setEditable(False)
                qty_available.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                items.append(qty_available)

                qty_to_move = QStandardItem("1")
                qty_to_move.setEditable(True)
                qty_to_move.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                items.append(qty_to_move)

                name_item = QStandardItem(row['name'] if row['name'] else "")
                name_item.setEditable(False)
                items.append(name_item)

                cat_item = QStandardItem(row['category'] if row['category'] else "")
                cat_item.setEditable(False)
                items.append(cat_item)

                type_item = QStandardItem(row['type'] if row['type'] else "")
                type_item.setEditable(False)
                items.append(type_item)

                model_item = QStandardItem(row['model'] if row['model'] else "")
                model_item.setEditable(False)
                items.append(model_item)

                manufacturer_item = QStandardItem(row['manufacturer'] if row['manufacturer'] else "")
                manufacturer_item.setEditable(False)
                items.append(manufacturer_item)

                serial_item = QStandardItem(row['serial_number'] if row['serial_number'] else "")
                serial_item.setEditable(False)
                items.append(serial_item)

                inv_item = QStandardItem(row['inventory_number'] if row['inventory_number'] else "")
                inv_item.setEditable(False)
                items.append(inv_item)

                price_item = QStandardItem(f"{row['price']:.2f}" if row['price'] else "0.00")
                price_item.setEditable(False)
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                items.append(price_item)

                date_item = QStandardItem(row['date_incoming'] if row['date_incoming'] else "")
                date_item.setEditable(False)
                items.append(date_item)

                self.distribution_model.appendRow(items)

            if len(rows) > 0:
                self.show_notification(f"Загружено {len(rows)} позиций для распределения")

        except Exception as e:
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось загрузить данные:\n\n{str(e)}")

    def setup_right_panel(self):
        room_container = getattr(self.ui, 'groupBox', None)
        if room_container is not None:
            layout = room_container.layout()
            if layout is None:
                layout = QVBoxLayout(room_container)
                room_container.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()

            title = QLabel("Оборудование в выбранной комнате")
            title.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout.addWidget(title)

            self.room_equipment_table = QTableView()
            layout.addWidget(self.room_equipment_table)
            self.remove_room_equip_btn = QPushButton("Удалить выделенное оборудование из комнаты")
            self.remove_room_equip_btn.clicked.connect(self.remove_selected_room_equipment)
            layout.addWidget(self.remove_room_equip_btn)
        elif hasattr(self.ui, 'tableView_3'):
            self.room_equipment_table = self.ui.tableView_3
        else:
            return

        self.room_equipment_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.room_equipment_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.room_equipment_model = QStandardItemModel()
        self.room_equipment_model.setHorizontalHeaderLabels([
            "ID", "Название", "Категория", "Тип", "Модель", "Производитель",
            "Серийный №", "Инвентарный №", "Кол-во", "Цена", "Дата поступления", "Поставщик"
        ])
        self.room_equipment_table.setModel(self.room_equipment_model)
        self.room_equipment_table.setColumnHidden(0, True)

        header = self.room_equipment_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(False)
        self.room_equipment_table.setColumnWidth(1, 180)
        self.room_equipment_table.setColumnWidth(2, 100)
        self.room_equipment_table.setColumnWidth(3, 100)
        self.room_equipment_table.setColumnWidth(4, 100)
        self.room_equipment_table.setColumnWidth(5, 120)
        self.room_equipment_table.setColumnWidth(6, 120)
        self.room_equipment_table.setColumnWidth(7, 100)
        self.room_equipment_table.setColumnWidth(8, 70)
        self.room_equipment_table.setColumnWidth(9, 100)
        self.room_equipment_table.setColumnWidth(10, 100)
        self.room_equipment_table.setColumnWidth(11, 150)

    def remove_selected_room_equipment(self):
        selection = self.room_equipment_table.selectionModel().selectedRows()
        if not selection:
            self.show_notification("Выберите оборудование для удаления из комнаты", error=True)
            return

        row = selection[0].row()
        equip_id_item = self.room_equipment_model.item(row, 0)
        if not equip_id_item:
            return
        equip_id = int(equip_id_item.text())

        dlg = ConfirmationDialog("Убрать это оборудование из комнаты?", self)
        if dlg.exec() == QDialog.Accepted:
            conn = self.db.get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE equipment SET room_id = NULL, workplace_number = NULL WHERE equipment_id = ?", (equip_id,))
                conn.commit()
            except Exception as e:
                self.show_notification(f"Не удалось обновить: {e}", error=True)
            finally:
                conn.close()
            self.load_room_equipment(self.current_room_id)
            self.load_distribution_equipment(silent=True)
            self.show_notification("Оборудование удалено из комнаты")

    def on_branch_changed_distribution(self):
        branch_id = self.ui.comboBox_14.currentData()
        if branch_id:
            branch = self.db.get_branch(branch_id)
            if branch:
                self.ui.spinBox_6.setMaximum(branch[2])

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
            self.load_room_equipment(room_id)

    def load_room_equipment(self, room_id):
        if not room_id:
            return

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT equipment_id, name, category, type, model, manufacturer,
                                  serial_number, inventory_number, quantity, price,
                                  date_incoming, supplier, status
                           FROM equipment
                           WHERE room_id = ?
                           ORDER BY name
                           """, (room_id,))
            rows = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка загрузки оборудования комнаты: {e}")
            rows = []
        finally:
            conn.close()

        if self.room_equipment_model:
            self.room_equipment_model.removeRows(0, self.room_equipment_model.rowCount())
            for row in rows:
                items = [
                    QStandardItem(str(row['equipment_id'])),
                    QStandardItem(row['name'] if row['name'] else ""),
                    QStandardItem(row['category'] if row['category'] else ""),
                    QStandardItem(row['type'] if row['type'] else ""),
                    QStandardItem(row['model'] if row['model'] else ""),
                    QStandardItem(row['manufacturer'] if row['manufacturer'] else ""),
                    QStandardItem(row['serial_number'] if row['serial_number'] else ""),
                    QStandardItem(row['inventory_number'] if row['inventory_number'] else ""),
                    QStandardItem(str(row['quantity'])),
                    QStandardItem(f"{row['price']:.2f}" if row['price'] else "0.00"),
                    QStandardItem(row['date_incoming'] if row['date_incoming'] else ""),
                    QStandardItem(row['supplier'] if row['supplier'] else "")
                ]
                for item in items:
                    item.setEditable(False)
                self.room_equipment_model.appendRow(items)

    def apply_distribution_filters(self):
        category = self.ui.comboBox_17.currentData()
        type_ = self.ui.comboBox_18.currentData()
        name_filter = self.ui.textEdit_2.toPlainText().lower() if hasattr(self.ui, 'textEdit_2') else ""

        for row in range(self.distribution_model.rowCount()):
            show = True
            if category and category != "Все категории":
                cat_item = self.distribution_model.item(row, 5)
                if cat_item and cat_item.text() != category:
                    show = False
            if show and type_ and type_ != "Все типы":
                type_item = self.distribution_model.item(row, 6)
                if type_item and type_item.text() != type_:
                    show = False
            if show and name_filter:
                name_item = self.distribution_model.item(row, 4)
                if name_item and name_filter not in name_item.text().lower():
                    show = False
            self.ui.tableView_2.setRowHidden(row, not show)

    def transfer_selected_items(self):
        if not self.current_room_id:
            self.show_notification("Сначала выберите комнату", error=True)
            return

        transfers = []
        errors = []

        for row in range(self.distribution_model.rowCount()):
            check_item = self.distribution_model.item(row, 0)
            if check_item and check_item.checkState() == Qt.Checked:
                equip_id_item = self.distribution_model.item(row, 1)
                qty_available_item = self.distribution_model.item(row, 2)
                qty_to_move_item = self.distribution_model.item(row, 3)
                name_item = self.distribution_model.item(row, 4)

                if equip_id_item and qty_to_move_item:
                    try:
                        equip_id = int(equip_id_item.text())
                        total_qty = int(qty_available_item.text())
                        move_qty_text = qty_to_move_item.text().strip()
                        move_qty = 1 if not move_qty_text else int(move_qty_text)

                        if move_qty <= 0:
                            errors.append(f"Для '{name_item.text()}' количество должно быть больше 0")
                            continue
                        if move_qty > total_qty:
                            errors.append(f"Для '{name_item.text()}' нельзя перенести больше {total_qty} шт. (доступно: {total_qty})")
                            continue
                        transfers.append((equip_id, move_qty, total_qty, name_item.text()))
                    except ValueError:
                        errors.append(f"Некорректное количество для '{name_item.text()}'")
                        continue

        if not transfers:
            if errors:
                self.show_notification("\n".join(errors[:3]), error=True)
            else:
                self.show_notification("Выберите позиции для переноса", error=True)
            return

        conn = self.db.get_connection()
        success_count = 0
        error_messages = []

        try:
            cursor = conn.cursor()
            for equip_id, move_qty, total_qty, item_name in transfers:
                try:
                    cursor.execute("SELECT name, category, type, model, manufacturer, serial_number, inventory_number, price, date_incoming, supplier, phone_supplier, email_supplier, status, notes FROM equipment WHERE equipment_id = ?", (equip_id,))
                    equip_data = cursor.fetchone()
                    if not equip_data:
                        error_messages.append(f"Оборудование '{item_name}' не найдено в БД")
                        continue

                    if move_qty == total_qty:
                        cursor.execute("UPDATE equipment SET room_id = ? WHERE equipment_id = ?", (self.current_room_id, equip_id))
                        success_count += 1
                    else:
                        cursor.execute("UPDATE equipment SET quantity = quantity - ? WHERE equipment_id = ?", (move_qty, equip_id))
                        old_serial = equip_data['serial_number'] if equip_data['serial_number'] else ""
                        new_serial = f"{old_serial}_copy_{uuid.uuid4().hex[:8]}" if old_serial else f"copy_{equip_id}_{uuid.uuid4().hex[:8]}"
                        cursor.execute("SELECT COUNT(*) FROM equipment WHERE serial_number = ?", (new_serial,))
                        if cursor.fetchone()[0] > 0:
                            new_serial = f"{new_serial}_{uuid.uuid4().hex[:4]}"
                        cursor.execute("""
                                       INSERT INTO equipment (name, category, type, model, manufacturer, quantity, serial_number, inventory_number, price, date_incoming, supplier, phone_supplier, email_supplier, status, notes, room_id)
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                       """, (equip_data['name'], equip_data['category'] or "", equip_data['type'] or "", equip_data['model'] or "", equip_data['manufacturer'] or "", move_qty, new_serial, equip_data['inventory_number'] or "", equip_data['price'] or 0, equip_data['date_incoming'] or datetime.now().strftime("%Y-%m-%d"), equip_data['supplier'] or "", equip_data['phone_supplier'] or "", equip_data['email_supplier'] or "", equip_data['status'] or "in_use", equip_data['notes'] or "", self.current_room_id))
                        success_count += 1
                except Exception as e:
                    error_messages.append(f"Ошибка при переносе '{item_name}': {str(e)}")
                    continue

            conn.commit()
            if error_messages:
                self.show_notification(f"Перенесено: {success_count} из {len(transfers)} позиций.\nОшибки:\n" + "\n".join(error_messages[:3]), error=True)
            else:
                self.show_notification(f"Успешно перенесено {success_count} позиций")
                QMessageBox.information(self, "Успех", f"Перенесено позиций: {success_count}")
        except Exception as e:
            conn.rollback()
            self.show_notification(f"Критическая ошибка при переносе: {e}", error=True)
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить перенос:\n{str(e)}")
        finally:
            conn.close()

        self.load_distribution_equipment(silent=True)
        if self.current_room_id:
            self.load_room_equipment(self.current_room_id)

    def save_room_distribution(self):
        if not self.current_room_id:
            self.show_notification("Выберите комнату", error=True)
            return
        dlg = ConfirmationDialog("Сохранить распределение для этой комнаты?", self)
        if dlg.exec() == QDialog.Accepted:
            self.show_notification("Распределение сохранено")

    def reset_room_distribution(self):
        if not self.current_room_id:
            self.show_notification("Выберите комнату", error=True)
            return
        dlg = ConfirmationDialog("Сбросить распределение для этой комнаты (все оборудования открепятся)?", self)
        if dlg.exec() == QDialog.Accepted:
            conn = self.db.get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE equipment SET room_id = NULL WHERE room_id = ?", (self.current_room_id,))
                conn.commit()
            except Exception as e:
                self.show_notification(f"Не удалось сбросить: {e}", error=True)
            finally:
                conn.close()
            self.load_room_equipment(self.current_room_id)
            self.load_distribution_equipment(silent=True)
            self.show_notification("Распределение сброшено")

    def save_all_distribution(self):
        dlg = ConfirmationDialog("Сохранить все распределения?", self)
        if dlg.exec() == QDialog.Accepted:
            self.show_notification("Все распределения сохранены")

    def delete_all_distribution(self):
        dlg = ConfirmationDialog("Удалить все распределения (отвязать всё оборудование от комнат)?", self)
        if dlg.exec() == QDialog.Accepted:
            conn = self.db.get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE equipment SET room_id = NULL")
                conn.commit()
            except Exception as e:
                self.show_notification(f"Не удалось удалить: {e}", error=True)
            finally:
                conn.close()
            self.load_distribution_equipment(silent=True)
            if self.current_room_id:
                self.load_room_equipment(self.current_room_id)
            self.show_notification("Все распределения удалены")

    def export_room_report(self):
        room_id = self.ui.comboBox_16.currentData()
        if not room_id:
            self.show_notification("Выберите комнату", error=True)
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

                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                               SELECT name, category, type, model, manufacturer, supplier,
                                      serial_number, inventory_number, quantity, price, date_incoming
                               FROM equipment
                               WHERE room_id = ?
                               ORDER BY name
                               """, (room_id,))
                equip_list = cursor.fetchall()
                conn.close()

                f.write("ОБОРУДОВАНИЕ В КОМНАТЕ:\n")
                f.write("-" * 120 + "\n")
                header = (f"{'№':<4} {'Наименование':<25} {'Категория':<15} {'Тип':<15} "
                          f"{'Модель':<15} {'Производитель':<15} {'Поставщик':<20} "
                          f"{'Кол-во':<8} {'Цена':<10}\n")
                f.write(header)
                f.write("-" * 120 + "\n")

                for i, eq in enumerate(equip_list, 1):
                    f.write(f"{i:<4} {eq[0]:<25} {eq[1]:<15} {eq[2]:<15} "
                            f"{eq[3]:<15} {eq[4]:<15} {eq[5]:<20} "
                            f"{eq[8]:<8} {eq[9]:<10}\n")

                f.write("-" * 120 + "\n")
                f.write(f"Всего единиц: {len(equip_list)}\n")
                f.write("\n" + "=" * 50 + "\n")
            self.show_notification(f"Отчет сохранен: {file_path}")
            QMessageBox.information(self, "Успех", f"Отчет сохранен: {file_path}")
        except Exception as e:
            self.show_notification(f"Не удалось сохранить: {e}", error=True)

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

                branches = self.db.get_all_branches()
                for branch in branches:
                    f.write(f"\nФИЛИАЛ: {branch[1]}\n")
                    rooms = self.db.get_rooms_by_branch(branch[0])
                    for room in rooms:
                        f.write(f"  Комната {room[1]}: {room[2]}\n")
                        conn = self.db.get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT name, quantity FROM equipment WHERE room_id = ?", (room[0],))
                        eqs = cursor.fetchall()
                        conn.close()
                        for name, qty in eqs:
                            f.write(f"    - {name} (x{qty})\n")
                f.write("\n" + "=" * 50 + "\n")
            self.show_notification(f"Финальный отчет сохранен: {file_path}")
            QMessageBox.information(self, "Успех", f"Отчет сохранен: {file_path}")
        except Exception as e:
            self.show_notification(f"Не удалось сохранить: {e}", error=True)

    def new_report(self):
        dlg = SaveConfirmationDialog(self)
        result = dlg.exec()
        if result == 1:
            self.save_current()
            self.clear_all()
        elif result == 2:
            self.clear_all()
        self.show_notification("Новый отчет создан")

    def new_arrival(self):
        dlg = SaveConfirmationDialog(self)
        result = dlg.exec()
        if result == 1:
            self.save_arrival()
            self.clear_arrival_tab()
        elif result == 2:
            self.clear_arrival_tab()
        self.show_notification("Новое поступление создано")

    def show_version(self):
        QMessageBox.information(self, "Версия", "Версия 1.0\nДипломный проект 2026")

    def show_project_info(self):
        QMessageBox.information(self, "Информация о проекте",
                                "Дипломный проект\nТема: Система учета оборудования\nРазработчик: ...\nTelegram: @katwell1\n\n© 2026")

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
        if hasattr(self, 'room_equipment_model'):
            self.room_equipment_model.removeRows(0, self.room_equipment_model.rowCount())
        self.load_distribution_equipment(silent=True)


def main():
    app = QApplication(sys.argv)
    window = ReportWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
