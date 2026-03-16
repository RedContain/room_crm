import sys
import os
import shutil
from datetime import datetime

# Добавляем путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QFile, QIODevice, QDateTime, QPointF
from PySide6.QtGui import QPixmap, QPen, QBrush, QColor, QFont, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMessageBox, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QVBoxLayout, QLabel, QTableView, QHeaderView, QAbstractScrollArea, QGraphicsTextItem
from PySide6.QtUiTools import QUiLoader

# ========== ИМПОРТ НАШИХ МОДУЛЕЙ ==========
import paths
from database_handler import DatabaseHandler
from ui.ui_plane import Ui_MainWindow

# ========== ИМПОРТЫ ДЛЯ PDF ==========
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import platform
    import subprocess

    # Функция для поиска шрифта с кириллицей
    def find_cyrillic_font():
        """Ищет системный шрифт с поддержкой кириллицы"""
        system = platform.system()

        # Список возможных путей к шрифтам в разных ОС
        font_paths = []

        if system == "Windows":
            # Windows
            windows_dir = os.environ.get('WINDIR', 'C:\\Windows')
            font_paths = [
                os.path.join(windows_dir, 'Fonts', 'arial.ttf'),
                os.path.join(windows_dir, 'Fonts', 'times.ttf'),
                os.path.join(windows_dir, 'Fonts', 'cour.ttf'),
                os.path.join(windows_dir, 'Fonts', 'verdana.ttf'),
                os.path.join(windows_dir, 'Fonts', 'tahoma.ttf'),
            ]
        elif system == "Darwin":  # macOS
            font_paths = [
                '/Library/Fonts/Arial.ttf',
                '/Library/Fonts/Times New Roman.ttf',
                '/Library/Fonts/Courier New.ttf',
                '/Library/Fonts/Verdana.ttf',
                '/System/Library/Fonts/Helvetica.ttc',
            ]
        else:  # Linux
            # Поиск шрифтов через fc-list если доступно
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

            # Стандартные пути Linux
            font_paths.extend([
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
                '/usr/share/fonts/truetype/arial/arial.ttf',
            ])

        # Проверяем существование файлов
        for path in font_paths:
            if os.path.exists(path):
                return path

        return None

    # Регистрируем шрифт при импорте
    FONT_PATH = find_cyrillic_font()
    FONT_REGISTERED = False

    if FONT_PATH:
        try:
            pdfmetrics.registerFont(TTFont('CyrillicFont', FONT_PATH))
            # Также регистрируем жирную версию если есть
            bold_path = FONT_PATH.replace('.ttf', 'b.ttf').replace('.ttc', 'b.ttc')
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont('CyrillicFont-Bold', bold_path))
            else:
                # Используем тот же шрифт для жирного
                pdfmetrics.registerFont(TTFont('CyrillicFont-Bold', FONT_PATH))
            FONT_REGISTERED = True
            print(f"✅ Зарегистрирован шрифт: {FONT_PATH}")
        except Exception as e:
            print(f"⚠️ Не удалось зарегистрировать шрифт {FONT_PATH}: {e}")

    REPORTLAB_AVAILABLE = True
except ImportError as e:
    REPORTLAB_AVAILABLE = False
    FONT_REGISTERED = False
    print(f"⚠️ reportlab не установлен, функции PDF будут недоступны. Ошибка: {e}")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = DatabaseHandler()
        self.current_map_id = None
        self.current_scene = None
        self.current_scene_display = None
        self.marker_items = []
        self.marker_items_display = []

        self.is_edit_mode = False
        self.pending_marker = None
        self.selected_room_id = None

        # ВЫЗЫВАЕМ ВСЕ МЕТОДЫ ИНИЦИАЛИЗАЦИИ
        self.setup_ui()
        self.connect_signals()
        self.load_branches_to_combobox()
        self.show_status("Готов к работе")

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создаем статус-бар, если его нет
        if not hasattr(self.ui, 'statusbar') or self.ui.statusbar is None:
            self.statusBar()

        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("QLabel { color: green; font-weight: bold; padding: 2px; }")

        # Добавляем в статус-бар
        if hasattr(self.ui, 'statusbar'):
            self.ui.statusbar.addPermanentWidget(self.status_label)
        else:
            self.statusBar().addPermanentWidget(self.status_label)

        if hasattr(self.ui, 'tableView'):
            self.ui.tableView.doubleClicked.connect(self.on_table_double_click)

        # Настраиваем правую таблицу для отображения оборудования
        self.setup_equipment_table()

    def setup_equipment_table(self):
        """Настраивает таблицу для отображения оборудования во вкладке просмотра"""
        if not hasattr(self.ui, 'tableView_2'):
            return

        # Создаем модель для таблицы оборудования
        self.equipment_model = QStandardItemModel()
        self.equipment_model.setHorizontalHeaderLabels([
            "Название", "Категория", "Тип", "Кол-во", "Цена",
            "Серийный №", "Инв. №", "Дата поступления", "Производитель", "Статус"
        ])
        self.ui.tableView_2.setModel(self.equipment_model)

        # Настройка горизонтальной прокрутки
        self.ui.tableView_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tableView_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Настройка колонок
        header = self.ui.tableView_2.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(False)

        # Задаём примерную ширину колонок
        self.ui.tableView_2.setColumnWidth(0, 200)  # Название
        self.ui.tableView_2.setColumnWidth(1, 150)  # Категория
        self.ui.tableView_2.setColumnWidth(2, 150)  # Тип
        self.ui.tableView_2.setColumnWidth(3, 80)   # Кол-во
        self.ui.tableView_2.setColumnWidth(4, 100)  # Цена
        self.ui.tableView_2.setColumnWidth(5, 150)  # Серийный №
        self.ui.tableView_2.setColumnWidth(6, 120)  # Инв. №
        self.ui.tableView_2.setColumnWidth(7, 150)  # Дата поступления
        self.ui.tableView_2.setColumnWidth(8, 200)  # Производитель
        self.ui.tableView_2.setColumnWidth(9, 100)  # Статус

        self.ui.tableView_2.setSelectionBehavior(QTableView.SelectRows)

    def show_status(self, message, is_error=False):
        """Показывает сообщение в статус-баре"""
        if hasattr(self, 'status_label'):
            self.status_label.setText(f"  {message}  ")
            if is_error:
                self.status_label.setStyleSheet("QLabel { color: red; font-weight: bold; padding: 2px; }")
            else:
                self.status_label.setStyleSheet("QLabel { color: green; font-weight: bold; padding: 2px; }")

    def connect_signals(self):
        """Подключение сигналов к слотам"""
        # Вкладка настроек (редактирование)
        if hasattr(self.ui, 'comboBox'):
            self.ui.comboBox.currentIndexChanged.connect(self.on_branch_changed_settings)
        if hasattr(self.ui, 'spinBox'):
            self.ui.spinBox.valueChanged.connect(self.on_floor_changed_settings)
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.on_load_map_clicked)
        if hasattr(self.ui, 'pushButton_2'):
            self.ui.pushButton_2.clicked.connect(self.on_edit_map_clicked)
        if hasattr(self.ui, 'pushButton_3'):
            self.ui.pushButton_3.clicked.connect(self.on_delete_map_clicked)
        if hasattr(self.ui, 'pushButton_8'):
            self.ui.pushButton_8.clicked.connect(self.on_save_map_clicked)

        # Вкладка просмотра
        if hasattr(self.ui, 'comboBox_2'):
            self.ui.comboBox_2.currentIndexChanged.connect(self.on_branch_changed_display)
        if hasattr(self.ui, 'spinBox_2'):
            self.ui.spinBox_2.valueChanged.connect(self.on_floor_changed_display)
        if hasattr(self.ui, 'pushButton_6'):
            self.ui.pushButton_6.clicked.connect(self.on_export_all_pdf)
        if hasattr(self.ui, 'pushButton_7'):
            self.ui.pushButton_7.clicked.connect(self.on_export_floor_pdf)

    def load_branches_to_combobox(self):
        """Загрузка филиалов в комбобоксы"""
        branches = self.db.get_all_branches()

        # Заполняем первый комбобокс (настройки)
        if hasattr(self.ui, 'comboBox'):
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("Выберите филиал", None)
            for branch in branches:
                self.ui.comboBox.addItem(branch['name'], branch['branch_id'])

        # Заполняем второй комбобокс (просмотр)
        if hasattr(self.ui, 'comboBox_2'):
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItem("Выберите филиал", None)
            for branch in branches:
                self.ui.comboBox_2.addItem(branch['name'], branch['branch_id'])

        self.show_status(f"Загружено {len(branches)} филиалов")

    def clear_graphics_view(self, graphics_view):
        """Очищает graphics view"""
        if graphics_view:
            scene = graphics_view.scene()
            if scene:
                scene.clear()
            graphics_view.setScene(None)

    def on_branch_changed_settings(self, index):
        """Обработчик смены филиала во вкладке настроек"""
        self.clear_graphics_view(getattr(self.ui, 'graphicsView', None))
        self.current_scene = None
        self.marker_items = []
        self.current_map_id = None
        if hasattr(self.ui, 'spinBox'):
            self.ui.spinBox.setValue(1)
        self.load_rooms_to_table()

    def on_floor_changed_settings(self, floor):
        """Обработчик смены этажа во вкладке настроек"""
        self.load_rooms_to_table()
        branch_id = None
        if hasattr(self.ui, 'comboBox'):
            branch_id = self.ui.comboBox.currentData()
        if branch_id:
            self.display_map_settings(branch_id, floor)

    def load_rooms_to_table(self):
        """Загрузка комнат в таблицу (настройки)"""
        if not hasattr(self.ui, 'tableView'):
            return

        branch_id = None
        if hasattr(self.ui, 'comboBox'):
            branch_id = self.ui.comboBox.currentData()

        floor = 1
        if hasattr(self.ui, 'spinBox'):
            floor = self.ui.spinBox.value()

        if not branch_id:
            return

        rooms = self.db.get_rooms_by_branch_and_floor(branch_id, floor)

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Номер', 'Название', 'Вместимость'])

        for room in rooms:
            id_item = QtGui.QStandardItem(str(room['room_id']))
            num_item = QtGui.QStandardItem(room['room_number'])
            name_item = QtGui.QStandardItem(room['room_name'])
            capacity_item = QtGui.QStandardItem(str(room['capacity']))

            id_item.setEditable(False)
            num_item.setEditable(False)
            name_item.setEditable(False)
            capacity_item.setEditable(False)

            model.appendRow([id_item, num_item, name_item, capacity_item])

        self.ui.tableView.setModel(model)
        self.ui.tableView.setColumnHidden(0, True)
        self.show_status(f"Загружено {len(rooms)} комнат")

    def on_table_double_click(self, index):
        """Обработчик двойного клика по таблице комнат (привязка точки)"""
        if not self.pending_marker:
            self.show_status("Сначала поставьте точку на схеме!", True)
            return

        if not hasattr(self.ui, 'tableView') or not self.ui.tableView.model():
            return

        model = self.ui.tableView.model()
        row = index.row()
        room_id = model.data(model.index(row, 0))
        room_number = model.data(model.index(row, 1))
        room_name = model.data(model.index(row, 2))

        if self.pending_marker:
            self.pending_marker.setBrush(QBrush(QColor(0, 255, 0, 180)))
            self.pending_marker.setData(0, room_id)
            self.pending_marker.setData(1, room_number)
            self.pending_marker.setData(2, room_name)
            self.pending_marker.setToolTip(f"{room_number} - {room_name}")

            if self.current_scene:
                font = QFont("Arial", 8)
                text = self.current_scene.addText(f"{room_number}", font)
                text.setPos(self.pending_marker.rect().center().x() + 20,
                            self.pending_marker.rect().center().y() - 10)
                text.setData(0, room_id)
                text.setToolTip(f"{room_number} - {room_name}")

                self.marker_items.append(self.pending_marker)
                self.marker_items.append(text)

            self.pending_marker = None
            self.show_status(f"Точка привязана к комнате {room_number} - {room_name}")

    def on_load_map_clicked(self):
        """Загрузка схемы этажа"""
        branch_id = None
        if hasattr(self.ui, 'comboBox'):
            branch_id = self.ui.comboBox.currentData()

        floor = 1
        if hasattr(self.ui, 'spinBox'):
            floor = self.ui.spinBox.value()

        if not branch_id:
            self.show_status("Сначала выберите филиал!", True)
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите схему этажа", "", "Images (*.png *.jpg *.jpeg)")
        if not file_path:
            return

        maps_dir = paths.get_maps_dir()
        file_ext = os.path.splitext(file_path)[1]
        new_file_name = f"branch_{branch_id}_floor_{floor}{file_ext}"
        new_file_path = os.path.join(maps_dir, new_file_name)

        try:
            shutil.copy2(file_path, new_file_path)
            self.db.save_floor_map(branch_id, floor, new_file_path)
            self.display_map_settings(branch_id, floor)
            self.show_status("Схема загружена и сохранена!")
        except Exception as e:
            self.show_status(f"Ошибка загрузки: {str(e)}", True)

    def on_edit_map_clicked(self):
        """Включение/выключение режима редактирования"""
        if not self.current_map_id:
            self.show_status("Сначала загрузите схему для этого этажа!", True)
            return

        self.is_edit_mode = not self.is_edit_mode

        if self.is_edit_mode:
            if hasattr(self.ui, 'pushButton_2'):
                self.ui.pushButton_2.setText("Выключить редактирование")
            if hasattr(self.ui, 'graphicsView'):
                self.ui.graphicsView.setCursor(Qt.CrossCursor)
            self.show_status("Режим: кликните на схеме чтобы поставить точку, затем выберите комнату в таблице")
        else:
            if hasattr(self.ui, 'pushButton_2'):
                self.ui.pushButton_2.setText("Редактировать схему")
            if hasattr(self.ui, 'graphicsView'):
                self.ui.graphicsView.setCursor(Qt.ArrowCursor)
            self.pending_marker = None
            self.show_status("Режим редактирования выключен")

    def on_delete_map_clicked(self):
        """Удаление схемы или точек"""
        if not self.current_map_id:
            self.show_status("Нет загруженной схемы для удаления!", True)
            return

        dialog = QMessageBox(self)
        dialog.setWindowTitle("Удаление")
        dialog.setText("Что вы хотите удалить?")
        delete_all_btn = dialog.addButton("Всю схему с точками", QMessageBox.YesRole)
        delete_markers_btn = dialog.addButton("Только точки", QMessageBox.NoRole)
        cancel_btn = dialog.addButton("Отмена", QMessageBox.RejectRole)

        dialog.exec()

        if dialog.clickedButton() == delete_all_btn:
            # Получаем путь к файлу перед удалением из БД
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT image_path FROM floor_maps WHERE map_id = ?", (self.current_map_id,))
            map_data = cursor.fetchone()
            conn.close()

            if map_data and os.path.exists(map_data['image_path']):
                try:
                    os.remove(map_data['image_path'])
                except:
                    pass

            self.db.delete_full_map(self.current_map_id)
            self.clear_graphics_view(getattr(self.ui, 'graphicsView', None))
            self.current_map_id = None
            self.current_scene = None
            self.marker_items = []
            self.show_status("Схема и точки удалены")

        elif dialog.clickedButton() == delete_markers_btn:
            self.db.delete_markers_by_map(self.current_map_id)
            branch_id = None
            if hasattr(self.ui, 'comboBox'):
                branch_id = self.ui.comboBox.currentData()
            floor = 1
            if hasattr(self.ui, 'spinBox'):
                floor = self.ui.spinBox.value()
            self.display_map_settings(branch_id, floor)
            self.show_status("Все точки удалены")

    def on_save_map_clicked(self):
        """Сохранение точек на карте"""
        if not self.current_map_id or not self.current_scene:
            return

        saved_count = 0
        for item in self.marker_items:
            if isinstance(item, QGraphicsEllipseItem):
                room_id = item.data(0)
                if room_id:
                    rect = item.rect()
                    center = item.mapToScene(rect.center())
                    x, y = center.x(), center.y()

                    self.db.add_marker(self.current_map_id, room_id, x, y)
                    saved_count += 1

        if saved_count > 0:
            self.show_status(f"Сохранено {saved_count} точек")
        else:
            self.show_status("Нет точек для сохранения", True)

    def mousePressEvent(self, event):
        """Обработка нажатия мыши для создания маркеров"""
        super().mousePressEvent(event)

        if not self.is_edit_mode or event.button() != Qt.LeftButton:
            return

        if not self.current_scene or not hasattr(self.ui, 'graphicsView'):
            self.show_status("Сначала загрузите схему!", True)
            return

        view_pos = self.ui.graphicsView.mapFromGlobal(event.globalPosition().toPoint())
        scene_pos = self.ui.graphicsView.mapToScene(view_pos)

        if not self.ui.graphicsView.sceneRect().contains(scene_pos):
            return

        self.create_temp_marker(scene_pos.x(), scene_pos.y())

    def create_temp_marker(self, x, y):
        """Создание временного маркера"""
        if not self.current_scene:
            return

        if self.pending_marker and self.current_scene:
            self.current_scene.removeItem(self.pending_marker)

        pen = QPen(Qt.blue)
        pen.setWidth(3)
        brush = QBrush(QColor(0, 0, 255, 180))

        # Увеличиваем размер точек (было 16, стало 24)
        ellipse = QGraphicsEllipseItem(x - 12, y - 12, 24, 24)
        ellipse.setPen(pen)
        ellipse.setBrush(brush)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        ellipse.setData(0, None)
        ellipse.setToolTip("Новая точка - выберите комнату в таблице")

        self.current_scene.addItem(ellipse)
        self.pending_marker = ellipse

        self.show_status("Точка поставлена, выберите комнату в таблице двойным кликом")

    def display_map_settings(self, branch_id, floor):
        """Отображение схемы во вкладке настроек"""
        if not hasattr(self.ui, 'graphicsView'):
            return

        self.clear_graphics_view(self.ui.graphicsView)

        map_info, markers = self.db.get_map_data(branch_id, floor)
        if not map_info:
            return

        self.current_map_id = map_info['map_id']
        scene = QGraphicsScene()
        self.current_scene = scene

        # Проверяем существование файла
        if not os.path.exists(map_info['image_path']):
            self.show_status("Файл изображения не найден", True)
            return

        pixmap = QPixmap(map_info['image_path'])
        if pixmap.isNull():
            self.show_status("Не удалось загрузить изображение схемы", True)
            return

        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        self.marker_items = []
        for marker in markers:
            x, y, room_id, room_name, room_number = marker

            pen = QPen(Qt.green)
            pen.setWidth(3)
            brush = QBrush(QColor(0, 255, 0, 180))

            # Увеличиваем размер точек (было 16, стало 24)
            ellipse = QGraphicsEllipseItem(x - 12, y - 12, 24, 24)
            ellipse.setPen(pen)
            ellipse.setBrush(brush)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
            ellipse.setData(0, room_id)
            ellipse.setData(1, room_number)
            ellipse.setData(2, room_name)
            ellipse.setToolTip(f"{room_number} - {room_name}")
            scene.addItem(ellipse)
            self.marker_items.append(ellipse)

            font = QFont("Arial", 9)
            text = scene.addText(f"{room_number}", font)
            text.setPos(x + 18, y - 10)
            text.setData(0, room_id)
            text.setToolTip(f"{room_number} - {room_name}")
            self.marker_items.append(text)

        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(pixmap_item, Qt.KeepAspectRatio)
        self.show_status(f"Загружено {len(markers)} точек")

    def on_branch_changed_display(self, index):
        """Обработчик смены филиала во вкладке просмотра"""
        branch_id = None
        if hasattr(self.ui, 'comboBox_2'):
            branch_id = self.ui.comboBox_2.currentData()

        if branch_id and hasattr(self.ui, 'spinBox_2'):
            self.ui.spinBox_2.setValue(1)
            self.display_map_display(branch_id, 1)

    def on_floor_changed_display(self, floor):
        """Обработчик смены этажа во вкладке просмотра"""
        branch_id = None
        if hasattr(self.ui, 'comboBox_2'):
            branch_id = self.ui.comboBox_2.currentData()

        if branch_id:
            self.display_map_display(branch_id, floor)

    def display_map_display(self, branch_id, floor):
        """Отображение схемы во вкладке просмотра"""
        if not hasattr(self.ui, 'graphicsView_2'):
            return

        self.clear_graphics_view(self.ui.graphicsView_2)

        map_info, markers = self.db.get_map_data(branch_id, floor)
        if not map_info:
            self.show_status(f"Нет схемы для этажа {floor}", True)
            # Очищаем информацию о комнате
            self.equipment_model.removeRows(0, self.equipment_model.rowCount())
            return

        # Проверяем существование файла
        if not os.path.exists(map_info['image_path']):
            self.show_status("Файл изображения не найден", True)
            return

        scene = QGraphicsScene()
        self.current_scene_display = scene

        pixmap = QPixmap(map_info['image_path'])
        if pixmap.isNull():
            self.show_status("Не удалось загрузить изображение", True)
            return

        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        self.marker_items_display = []
        for marker in markers:
            x, y, room_id, room_name, room_number = marker

            pen = QPen(Qt.blue)
            pen.setWidth(3)
            brush = QBrush(QColor(0, 0, 255, 150))

            # Увеличиваем размер точек (было 16, стало 24)
            ellipse = QGraphicsEllipseItem(x - 12, y - 12, 24, 24)
            ellipse.setPen(pen)
            ellipse.setBrush(brush)
            ellipse.setData(0, room_id)
            ellipse.setData(1, room_number)
            ellipse.setData(2, room_name)
            ellipse.setToolTip(f"{room_number} - {room_name}")
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, False)

            # Устанавливаем обработчик клика
            ellipse.mousePressEvent = lambda event, e=ellipse: self.on_marker_clicked(event, e)

            scene.addItem(ellipse)
            self.marker_items_display.append(ellipse)

            font = QFont("Arial", 8)
            text = scene.addText(room_number, font)
            text.setPos(x + 12, y - 8)
            text.setFlag(QGraphicsEllipseItem.ItemIsSelectable, False)
            text.setToolTip(f"{room_number} - {room_name}")
            self.marker_items_display.append(text)

        self.ui.graphicsView_2.setScene(scene)
        self.ui.graphicsView_2.fitInView(pixmap_item, Qt.KeepAspectRatio)

        # Очищаем информацию о комнате
        self.equipment_model.removeRows(0, self.equipment_model.rowCount())
        self.show_status(f"Показан этаж {floor}, {len(markers)} помещений")

    def on_marker_clicked(self, event, marker):
        """Обработчик клика по маркеру на схеме просмотра"""
        room_id = marker.data(0)
        room_number = marker.data(1)
        room_name = marker.data(2)

        if room_id:
            # Загружаем оборудование и показываем название комнаты
            self.load_room_equipment(room_id, f"Кабинет {room_number} - {room_name}")

        # Передаём событие дальше
        if hasattr(QGraphicsEllipseItem, 'mousePressEvent'):
            QGraphicsEllipseItem.mousePressEvent(marker, event)

    def load_room_equipment(self, room_id, room_title):
        """Загружает оборудование для выбранной комнаты и отображает в таблице"""
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT name, category, type, quantity, price,
                                  serial_number, inventory_number, date_incoming, supplier, status
                           FROM equipment
                           WHERE room_id = ?
                           ORDER BY name
                           """, (room_id,))
            rows = cursor.fetchall()
        except Exception as e:
            self.show_status(f"Ошибка загрузки оборудования: {e}", True)
            rows = []
        finally:
            conn.close()

        # Очищаем таблицу
        self.equipment_model.removeRows(0, self.equipment_model.rowCount())

        # Добавляем строку с названием комнаты (жирным шрифтом)
        room_item = QStandardItem(room_title)
        room_item.setEditable(False)
        # Делаем жирным
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        room_item.setFont(font)
        room_item.setTextAlignment(Qt.AlignCenter)
        # Объединяем все колонки в одну строку
        empty_items = [QStandardItem("") for _ in range(9)]
        self.equipment_model.appendRow([room_item] + empty_items)

        if not rows:
            # Нет оборудования
            no_equip_item = QStandardItem("Нет оборудования в этом кабинете")
            no_equip_item.setTextAlignment(Qt.AlignCenter)
            no_equip_item.setEditable(False)
            empty_items2 = [QStandardItem("") for _ in range(9)]
            self.equipment_model.appendRow([no_equip_item] + empty_items2)
        else:
            # Добавляем оборудование
            for row in rows:
                items = [
                    QStandardItem(row[0] or ""),
                    QStandardItem(row[1] or ""),
                    QStandardItem(row[2] or ""),
                    QStandardItem(str(row[3])),
                    QStandardItem(str(row[4])),
                    QStandardItem(row[5] or ""),
                    QStandardItem(row[6] or ""),
                    QStandardItem(row[7] or ""),
                    QStandardItem(row[8] or ""),
                    QStandardItem(row[9] or "")
                ]
                for item in items:
                    item.setEditable(False)
                    item.setTextAlignment(Qt.AlignCenter)
                self.equipment_model.appendRow(items)

        self.show_status(f"Загружено {len(rows)} единиц оборудования")

    def get_equipment_for_room(self, room_id):
        """Получает оборудование для комнаты"""
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT name, category, type, quantity, price,
                                  serial_number, inventory_number, date_incoming, supplier, status
                           FROM equipment
                           WHERE room_id = ?
                           ORDER BY name
                           """, (room_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка загрузки оборудования: {e}")
            return []
        finally:
            conn.close()

    def on_export_all_pdf(self):
        """Экспорт всех этажей в PDF с полной информацией об оборудовании"""
        if not REPORTLAB_AVAILABLE:
            QMessageBox.warning(self, "Ошибка", "Библиотека reportlab не установлена. Установите: pip install reportlab")
            return

        branch_id = None
        if hasattr(self.ui, 'comboBox_2'):
            branch_id = self.ui.comboBox_2.currentData()

        if not branch_id:
            self.show_status("Выберите филиал!", True)
            return

        branch = self.db.get_branch(branch_id)
        if not branch:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет", f"инвентаризация_{branch['name']}.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        try:
            self.show_status("Генерация PDF...")

            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
            story = []
            styles = getSampleStyleSheet()

            # Создаем стили с русским шрифтом
            if FONT_REGISTERED:
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Title'],
                    fontName='CyrillicFont-Bold',
                    fontSize=18,
                    alignment=1,
                    spaceAfter=20
                )
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontName='CyrillicFont-Bold',
                    fontSize=14,
                    spaceAfter=10
                )
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontName='CyrillicFont',
                    fontSize=10
                )
                table_header_style = ParagraphStyle(
                    'TableHeader',
                    parent=styles['Normal'],
                    fontName='CyrillicFont-Bold',
                    fontSize=9,
                    alignment=1
                )
                table_cell_style = ParagraphStyle(
                    'TableCell',
                    parent=styles['Normal'],
                    fontName='CyrillicFont',
                    fontSize=8,
                    alignment=1
                )
            else:
                title_style = styles['Title']
                heading_style = styles['Heading2']
                normal_style = styles['Normal']
                table_header_style = styles['Normal']
                table_cell_style = styles['Normal']

            # Заголовок документа
            story.append(Paragraph(f"ИНВЕНТАРИЗАЦИОННАЯ ОПИСЬ", title_style))
            story.append(Paragraph(f"Филиал: {branch['name']}", heading_style))
            story.append(Paragraph(f"Адрес: {branch['address']}", normal_style))
            story.append(Paragraph(f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style))
            story.append(Spacer(1, 10*mm))

            total_equipment_all = 0
            total_value_all = 0

            # Проходим по этажам
            for floor in range(1, branch['floors_count'] + 1):
                story.append(Paragraph(f"ЭТАЖ {floor}", heading_style))
                story.append(Spacer(1, 5*mm))

                # Получаем схему этажа
                map_info, markers = self.db.get_map_data(branch_id, floor)

                if map_info and os.path.exists(map_info['image_path']):
                    try:
                        img = Image(map_info['image_path'])
                        img.drawHeight = 60*mm
                        img.drawWidth = 90*mm
                        story.append(img)
                        story.append(Spacer(1, 5*mm))
                    except Exception as e:
                        print(f"Ошибка загрузки изображения: {e}")

                if markers:
                    floor_total_equipment = 0
                    floor_total_value = 0

                    for marker in markers:
                        room_id = marker[2]
                        room_number = marker[4]
                        room_name = marker[3]

                        # Получаем оборудование для комнаты
                        equipment = self.get_equipment_for_room(room_id)

                        if equipment:
                            story.append(Paragraph(f"Кабинет {room_number} - {room_name}", normal_style))

                            # Таблица с оборудованием
                            data = [['№', 'Наименование', 'Категория', 'Тип', 'Кол-во', 'Цена', 'Сумма',
                                     'Серийный №', 'Инв. №', 'Производитель', 'Статус']]

                            room_total = 0
                            for i, eq in enumerate(equipment, 1):
                                name = eq[0] or ''
                                category = eq[1] or ''
                                eq_type = eq[2] or ''
                                quantity = str(eq[3])
                                price = f"{eq[4]:.2f}" if eq[4] else '0.00'
                                try:
                                    sum_val = float(eq[3]) * float(eq[4] if eq[4] else 0)
                                    room_total += sum_val
                                    sum_str = f"{sum_val:.2f}"
                                except:
                                    sum_str = '0.00'

                                serial = eq[5] or ''
                                inventory = eq[6] or ''
                                supplier = eq[8] or ''
                                status = eq[9] or ''

                                data.append([
                                    str(i),
                                    name[:30] + '...' if len(name) > 30 else name,
                                    category[:15] + '...' if len(category) > 15 else category,
                                    eq_type[:15] + '...' if len(eq_type) > 15 else eq_type,
                                    quantity,
                                    price,
                                    sum_str,
                                    serial[:15] + '...' if len(serial) > 15 else serial,
                                    inventory[:10] + '...' if len(inventory) > 10 else inventory,
                                    supplier[:15] + '...' if len(supplier) > 15 else supplier,
                                    status[:10] + '...' if len(status) > 10 else status
                                ])

                            # Добавляем итог по комнате
                            data.append(['', '', '', '', '', '', f'Итого: {room_total:.2f}', '', '', '', ''])

                            table = Table(data, colWidths=[10*mm, 30*mm, 20*mm, 20*mm, 12*mm, 15*mm, 20*mm, 20*mm, 15*mm, 20*mm, 15*mm])

                            table_style = [
                                ('GRID', (0,0), (-1,-2), 0.5, colors.grey),
                                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                                ('SPAN', (0,-1), (5,-1)),  # Объединяем ячейки для итога
                                ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                                ('FONTSIZE', (0,0), (-1,-1), 7),
                            ]

                            if FONT_REGISTERED:
                                table_style.extend([
                                    ('FONTNAME', (0,0), (-1,0), 'CyrillicFont-Bold'),
                                    ('FONTNAME', (0,1), (-1,-1), 'CyrillicFont'),
                                ])

                            table.setStyle(TableStyle(table_style))
                            story.append(table)
                            story.append(Spacer(1, 5*mm))

                            floor_total_equipment += len(equipment)
                            floor_total_value += room_total

                    # Итог по этажу
                    story.append(Paragraph(f"Итого по этажу {floor}: {floor_total_equipment} ед. на сумму {floor_total_value:.2f} руб.",
                                           normal_style))
                    story.append(Spacer(1, 10*mm))

                    total_equipment_all += floor_total_equipment
                    total_value_all += floor_total_value
                else:
                    story.append(Paragraph("Нет помещений на этаже", normal_style))
                    story.append(Spacer(1, 10*mm))

                story.append(PageBreak())

            # Итог по всему филиалу
            story.append(Paragraph("ИТОГО ПО ФИЛИАЛУ:", heading_style))
            story.append(Paragraph(f"Всего единиц оборудования: {total_equipment_all}", normal_style))
            story.append(Paragraph(f"Общая стоимость: {total_value_all:.2f} руб.", normal_style))

            doc.build(story)
            self.show_status(f"Отчет сохранен: {os.path.basename(file_path)}")

        except Exception as e:
            self.show_status(f"Ошибка создания PDF: {str(e)}", True)
            import traceback
            traceback.print_exc()

    def on_export_floor_pdf(self):
        """Экспорт одного этажа в PDF с полной информацией об оборудовании"""
        if not REPORTLAB_AVAILABLE:
            QMessageBox.warning(self, "Ошибка", "Библиотека reportlab не установлена. Установите: pip install reportlab")
            return

        branch_id = None
        if hasattr(self.ui, 'comboBox_2'):
            branch_id = self.ui.comboBox_2.currentData()

        floor = 1
        if hasattr(self.ui, 'spinBox_2'):
            floor = self.ui.spinBox_2.value()

        if not branch_id:
            self.show_status("Выберите филиал!", True)
            return

        branch = self.db.get_branch(branch_id)
        if not branch:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет", f"инвентаризация_{branch['name']}_этаж_{floor}.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        try:
            self.show_status("Генерация PDF...")

            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
            story = []
            styles = getSampleStyleSheet()

            # Создаем стили с русским шрифтом
            if FONT_REGISTERED:
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Title'],
                    fontName='CyrillicFont-Bold',
                    fontSize=18,
                    alignment=1,
                    spaceAfter=20
                )
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontName='CyrillicFont-Bold',
                    fontSize=14,
                    spaceAfter=10
                )
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontName='CyrillicFont',
                    fontSize=10
                )
                table_header_style = ParagraphStyle(
                    'TableHeader',
                    parent=styles['Normal'],
                    fontName='CyrillicFont-Bold',
                    fontSize=9,
                    alignment=1
                )
                table_cell_style = ParagraphStyle(
                    'TableCell',
                    parent=styles['Normal'],
                    fontName='CyrillicFont',
                    fontSize=8,
                    alignment=1
                )
            else:
                title_style = styles['Title']
                heading_style = styles['Heading2']
                normal_style = styles['Normal']
                table_header_style = styles['Normal']
                table_cell_style = styles['Normal']

            # Заголовок документа
            story.append(Paragraph(f"ИНВЕНТАРИЗАЦИОННАЯ ОПИСЬ", title_style))
            story.append(Paragraph(f"Филиал: {branch['name']}", heading_style))
            story.append(Paragraph(f"Адрес: {branch['address']}", normal_style))
            story.append(Paragraph(f"Этаж: {floor}", heading_style))
            story.append(Paragraph(f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style))
            story.append(Spacer(1, 10*mm))

            # Получаем схему этажа
            map_info, markers = self.db.get_map_data(branch_id, floor)

            if map_info and os.path.exists(map_info['image_path']):
                try:
                    img = Image(map_info['image_path'])
                    img.drawHeight = 60*mm
                    img.drawWidth = 90*mm
                    story.append(img)
                    story.append(Spacer(1, 5*mm))
                except Exception as e:
                    print(f"Ошибка загрузки изображения: {e}")

            floor_total_equipment = 0
            floor_total_value = 0

            if markers:
                for marker in markers:
                    room_id = marker[2]
                    room_number = marker[4]
                    room_name = marker[3]

                    # Получаем оборудование для комнаты
                    equipment = self.get_equipment_for_room(room_id)

                    if equipment:
                        story.append(Paragraph(f"Кабинет {room_number} - {room_name}", normal_style))

                        # Таблица с оборудованием
                        data = [['№', 'Наименование', 'Категория', 'Тип', 'Кол-во', 'Цена', 'Сумма',
                                 'Серийный №', 'Инв. №', 'Производитель', 'Статус']]

                        room_total = 0
                        for i, eq in enumerate(equipment, 1):
                            name = eq[0] or ''
                            category = eq[1] or ''
                            eq_type = eq[2] or ''
                            quantity = str(eq[3])
                            price = f"{eq[4]:.2f}" if eq[4] else '0.00'
                            try:
                                sum_val = float(eq[3]) * float(eq[4] if eq[4] else 0)
                                room_total += sum_val
                                sum_str = f"{sum_val:.2f}"
                            except:
                                sum_str = '0.00'

                            serial = eq[5] or ''
                            inventory = eq[6] or ''
                            supplier = eq[8] or ''
                            status = eq[9] or ''

                            data.append([
                                str(i),
                                name[:30] + '...' if len(name) > 30 else name,
                                category[:15] + '...' if len(category) > 15 else category,
                                eq_type[:15] + '...' if len(eq_type) > 15 else eq_type,
                                quantity,
                                price,
                                sum_str,
                                serial[:15] + '...' if len(serial) > 15 else serial,
                                inventory[:10] + '...' if len(inventory) > 10 else inventory,
                                supplier[:15] + '...' if len(supplier) > 15 else supplier,
                                status[:10] + '...' if len(status) > 10 else status
                            ])

                        # Добавляем итог по комнате
                        data.append(['', '', '', '', '', '', f'Итого: {room_total:.2f}', '', '', '', ''])

                        table = Table(data, colWidths=[10*mm, 30*mm, 20*mm, 20*mm, 12*mm, 15*mm, 20*mm, 20*mm, 15*mm, 20*mm, 15*mm])

                        table_style = [
                            ('GRID', (0,0), (-1,-2), 0.5, colors.grey),
                            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                            ('SPAN', (0,-1), (5,-1)),  # Объединяем ячейки для итога
                            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                            ('FONTSIZE', (0,0), (-1,-1), 7),
                        ]

                        if FONT_REGISTERED:
                            table_style.extend([
                                ('FONTNAME', (0,0), (-1,0), 'CyrillicFont-Bold'),
                                ('FONTNAME', (0,1), (-1,-1), 'CyrillicFont'),
                            ])

                        table.setStyle(TableStyle(table_style))
                        story.append(table)
                        story.append(Spacer(1, 5*mm))

                        floor_total_equipment += len(equipment)
                        floor_total_value += room_total
            else:
                story.append(Paragraph("Нет помещений на этаже", normal_style))

            # Итог по этажу
            story.append(Spacer(1, 10*mm))
            story.append(Paragraph(f"ИТОГО ПО ЭТАЖУ {floor}:", heading_style))
            story.append(Paragraph(f"Всего единиц оборудования: {floor_total_equipment}", normal_style))
            story.append(Paragraph(f"Общая стоимость: {floor_total_value:.2f} руб.", normal_style))

            doc.build(story)
            self.show_status(f"Отчет сохранен: {os.path.basename(file_path)}")

        except Exception as e:
            self.show_status(f"Ошибка создания PDF: {str(e)}", True)
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())