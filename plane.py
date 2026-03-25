import sys
import os
import shutil
from datetime import datetime

# Добавляем путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QFile, QIODevice, QDateTime, QPointF, QRectF
from PySide6.QtGui import QPixmap, QPen, QBrush, QColor, QFont, QStandardItemModel, QStandardItem, QPainterPath
from PySide6.QtWidgets import QMessageBox, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QVBoxLayout, QLabel, QTableView, QHeaderView, QAbstractScrollArea, QGraphicsTextItem, QGraphicsItem
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

    if FONT_PATH:
        try:
            pdfmetrics.registerFont(TTFont('CyrillicFont', FONT_PATH))
            bold_path = FONT_PATH.replace('.ttf', 'b.ttf').replace('.ttc', 'b.ttc')
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont('CyrillicFont-Bold', bold_path))
            else:
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


class CustomEllipseItem(QGraphicsEllipseItem):
    """Кастомный эллипс с поддержкой тултипа"""
    def __init__(self, x, y, w, h, room_id, room_number, room_name):
        super().__init__(x, y, w, h)
        self.room_id = room_id
        self.room_number = room_number
        self.room_name = room_name
        self.setToolTip(f"{room_number} - {room_name}")
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor(255, 255, 0, 200)))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor(0, 255, 0, 180)))
        super().hoverLeaveEvent(event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = DatabaseHandler()
        self.current_map_id = None
        self.current_scene = None
        self.current_scene_display = None
        self.marker_items = []  # Список точек (эллипсы)
        self.marker_texts = []  # Список текстовых меток
        self.marker_items_display = []
        self.marker_texts_display = []

        self.is_edit_mode = False
        self.pending_marker = None
        self.selected_room_id = None

        # Константы для размера точек (фиксированный размер в пикселях)
        self.MARKER_SIZE = 20  # Размер точки
        self.MARKER_RADIUS = 10  # Радиус точки

        # ВЫЗЫВАЕМ ВСЕ МЕТОДЫ ИНИЦИАЛИЗАЦИИ
        self.setup_ui()
        self.connect_signals()
        self.load_branches_to_combobox()
        self.show_status("Готов к работе")

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Настраиваем спинбоксы для этажей (поддерживаем минусовые этажи)
        if hasattr(self.ui, 'spinBox'):
            self.ui.spinBox.setRange(-3, 50)
            self.ui.spinBox.setToolTip("Этаж: -3 (подвал) до 50")
        if hasattr(self.ui, 'spinBox_2'):
            self.ui.spinBox_2.setRange(-3, 50)
            self.ui.spinBox_2.setToolTip("Этаж: -3 (подвал) до 50")

        # Создаем статус-бар
        if not hasattr(self.ui, 'statusbar') or self.ui.statusbar is None:
            self.statusBar()

        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("QLabel { color: green; font-weight: bold; padding: 2px; }")

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

        self.equipment_model = QStandardItemModel()
        self.equipment_model.setHorizontalHeaderLabels([
            "Название", "Категория", "Тип", "Кол-во", "Цена",
            "Серийный №", "Инв. №", "Дата поступления", "Производитель", "Статус"
        ])
        self.ui.tableView_2.setModel(self.equipment_model)

        self.ui.tableView_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tableView_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        header = self.ui.tableView_2.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(False)

        self.ui.tableView_2.setColumnWidth(0, 200)
        self.ui.tableView_2.setColumnWidth(1, 150)
        self.ui.tableView_2.setColumnWidth(2, 150)
        self.ui.tableView_2.setColumnWidth(3, 80)
        self.ui.tableView_2.setColumnWidth(4, 100)
        self.ui.tableView_2.setColumnWidth(5, 150)
        self.ui.tableView_2.setColumnWidth(6, 120)
        self.ui.tableView_2.setColumnWidth(7, 150)
        self.ui.tableView_2.setColumnWidth(8, 200)
        self.ui.tableView_2.setColumnWidth(9, 100)

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

        if hasattr(self.ui, 'comboBox'):
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("Выберите филиал", None)
            for branch in branches:
                self.ui.comboBox.addItem(branch['name'], branch['branch_id'])

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
        self.marker_texts = []
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

    def get_floor_display_text(self, floor):
        """Возвращает текст для отображения этажа"""
        if floor < 0:
            return f"Подвал {abs(floor)}"
        elif floor == 0:
            return "Цокольный этаж"
        else:
            return f"Этаж {floor}"

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
        model.setHorizontalHeaderLabels(['ID', 'Номер', 'Название', 'Вместимость', 'Привязана'])

        # Получаем уже привязанные комнаты
        map_info, markers = self.db.get_map_data(branch_id, floor)
        bound_rooms = set()
        if markers:
            for marker in markers:
                bound_rooms.add(marker[2])  # room_id

        for room in rooms:
            id_item = QtGui.QStandardItem(str(room['room_id']))
            num_item = QtGui.QStandardItem(room['room_number'])
            name_item = QtGui.QStandardItem(room['room_name'])
            capacity_item = QtGui.QStandardItem(str(room['capacity']))
            bound_item = QtGui.QStandardItem("✓ Привязана" if room['room_id'] in bound_rooms else "")
            bound_item.setEditable(False)

            id_item.setEditable(False)
            num_item.setEditable(False)
            name_item.setEditable(False)
            capacity_item.setEditable(False)

            # Если комната уже привязана, делаем её серой
            if room['room_id'] in bound_rooms:
                for item in [id_item, num_item, name_item, capacity_item, bound_item]:
                    item.setForeground(QtGui.QBrush(Qt.gray))

            model.appendRow([id_item, num_item, name_item, capacity_item, bound_item])

        self.ui.tableView.setModel(model)
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnWidth(4, 100)
        self.show_status(f"Загружено {len(rooms)} комнат, привязано {len(bound_rooms)}")

    def on_table_double_click(self, index):
        """Обработчик двойного клика по таблице комнат (привязка точки)"""
        if not self.pending_marker:
            self.show_status("Сначала поставьте точку на схеме!", True)
            return

        if not hasattr(self.ui, 'tableView') or not self.ui.tableView.model():
            return

        model = self.ui.tableView.model()
        row = index.row()
        room_id = int(model.data(model.index(row, 0)))
        room_number = model.data(model.index(row, 1))
        room_name = model.data(model.index(row, 2))
        bound_status = model.data(model.index(row, 4))

        # Проверяем, не привязана ли уже комната
        if bound_status and "Привязана" in bound_status:
            self.show_status(f"Комната {room_number} уже привязана к другой точке!", True)
            return

        if self.pending_marker:
            # Обновляем точку
            self.pending_marker.room_id = room_id
            self.pending_marker.room_number = room_number
            self.pending_marker.room_name = room_name
            self.pending_marker.setToolTip(f"{room_number} - {room_name}")
            self.pending_marker.setBrush(QBrush(QColor(0, 255, 0, 180)))

            # Обновляем текст
            if self.pending_marker_text:
                self.pending_marker_text.setPlainText(room_number)
                self.pending_marker_text.setToolTip(f"{room_number} - {room_name}")

            # Обновляем модель таблицы (отмечаем комнату как привязанную)
            bound_item = QStandardItem("✓ Привязана")
            bound_item.setEditable(False)
            bound_item.setForeground(QtGui.QBrush(Qt.gray))
            model.setItem(row, 4, bound_item)
            for col in range(4):
                item = model.item(row, col)
                if item:
                    item.setForeground(QtGui.QBrush(Qt.gray))

            self.marker_items.append(self.pending_marker)
            if self.pending_marker_text:
                self.marker_texts.append(self.pending_marker_text)

            self.pending_marker = None
            self.pending_marker_text = None
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
            if self.pending_marker and self.current_scene:
                self.current_scene.removeItem(self.pending_marker)
                if self.pending_marker_text:
                    self.current_scene.removeItem(self.pending_marker_text)
            self.pending_marker = None
            self.pending_marker_text = None
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
            self.marker_texts = []
            self.load_rooms_to_table()
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
            self.load_rooms_to_table()
            self.show_status("Все точки удалены")

    def on_save_map_clicked(self):
        """Сохранение точек на карте"""
        if not self.current_map_id or not self.current_scene:
            return

        # Удаляем старые маркеры
        self.db.delete_markers_by_map(self.current_map_id)

        saved_count = 0
        for item in self.marker_items:
            if hasattr(item, 'room_id') and item.room_id:
                rect = item.rect()
                center = item.mapToScene(rect.center())
                x, y = center.x(), center.y()
                self.db.add_marker(self.current_map_id, item.room_id, x, y)
                saved_count += 1

        if saved_count > 0:
            self.show_status(f"Сохранено {saved_count} точек")
            self.load_rooms_to_table()
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
        """Создание временного маркера (фиксированного размера)"""
        if not self.current_scene:
            return

        if self.pending_marker and self.current_scene:
            self.current_scene.removeItem(self.pending_marker)
            if self.pending_marker_text:
                self.current_scene.removeItem(self.pending_marker_text)

        size = self.MARKER_SIZE
        radius = self.MARKER_RADIUS

        pen = QPen(Qt.blue)
        pen.setWidth(2)
        brush = QBrush(QColor(0, 0, 255, 180))

        # Создаем временную точку
        ellipse = CustomEllipseItem(x - radius, y - radius, size, size, None, None, None)
        ellipse.setPen(pen)
        ellipse.setBrush(brush)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        ellipse.setToolTip("Новая точка - выберите комнату в таблице")

        # Создаем временный текст
        font = QFont("Arial", 9)
        text = self.current_scene.addText("?", font)
        text.setPos(x + radius + 2, y - radius)
        text.setDefaultTextColor(Qt.blue)

        self.current_scene.addItem(ellipse)
        self.pending_marker = ellipse
        self.pending_marker_text = text

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
        self.marker_texts = []
        size = self.MARKER_SIZE
        radius = self.MARKER_RADIUS

        for marker in markers:
            x, y, room_id, room_name, room_number = marker

            pen = QPen(Qt.green)
            pen.setWidth(2)
            brush = QBrush(QColor(0, 255, 0, 180))

            ellipse = CustomEllipseItem(x - radius, y - radius, size, size, room_id, room_number, room_name)
            ellipse.setPen(pen)
            ellipse.setBrush(brush)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
            scene.addItem(ellipse)
            self.marker_items.append(ellipse)

            font = QFont("Arial", 9)
            text = scene.addText(room_number, font)
            text.setPos(x + radius + 2, y - radius)
            text.setDefaultTextColor(Qt.darkGreen)
            text.setToolTip(f"{room_number} - {room_name}")
            self.marker_texts.append(text)

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
            self.show_status(f"Нет схемы для {self.get_floor_display_text(floor)}", True)
            self.equipment_model.removeRows(0, self.equipment_model.rowCount())
            return

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
        self.marker_texts_display = []
        size = self.MARKER_SIZE
        radius = self.MARKER_RADIUS

        for marker in markers:
            x, y, room_id, room_name, room_number = marker

            pen = QPen(Qt.blue)
            pen.setWidth(2)
            brush = QBrush(QColor(0, 0, 255, 150))

            ellipse = CustomEllipseItem(x - radius, y - radius, size, size, room_id, room_number, room_name)
            ellipse.setPen(pen)
            ellipse.setBrush(brush)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, False)

            ellipse.mousePressEvent = lambda event, e=ellipse: self.on_marker_clicked(event, e)

            scene.addItem(ellipse)
            self.marker_items_display.append(ellipse)

            font = QFont("Arial", 8)
            text = scene.addText(room_number, font)
            text.setPos(x + radius + 2, y - radius)
            text.setDefaultTextColor(Qt.darkBlue)
            text.setToolTip(f"{room_number} - {room_name}")
            self.marker_texts_display.append(text)

        self.ui.graphicsView_2.setScene(scene)
        self.ui.graphicsView_2.fitInView(pixmap_item, Qt.KeepAspectRatio)

        self.equipment_model.removeRows(0, self.equipment_model.rowCount())
        self.show_status(f"Показан {self.get_floor_display_text(floor)}, {len(markers)} помещений")

    def on_marker_clicked(self, event, marker):
        """Обработчик клика по маркеру на схеме просмотра"""
        room_id = marker.room_id
        room_number = marker.room_number
        room_name = marker.room_name

        if room_id:
            self.load_room_equipment(room_id, f"Кабинет {room_number} - {room_name}")

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

        self.equipment_model.removeRows(0, self.equipment_model.rowCount())

        room_item = QStandardItem(room_title)
        room_item.setEditable(False)
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        room_item.setFont(font)
        room_item.setTextAlignment(Qt.AlignCenter)
        empty_items = [QStandardItem("") for _ in range(9)]
        self.equipment_model.appendRow([room_item] + empty_items)

        if not rows:
            no_equip_item = QStandardItem("Нет оборудования в этом кабинете")
            no_equip_item.setTextAlignment(Qt.AlignCenter)
            no_equip_item.setEditable(False)
            empty_items2 = [QStandardItem("") for _ in range(9)]
            self.equipment_model.appendRow([no_equip_item] + empty_items2)
        else:
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
            QMessageBox.warning(self, "Ошибка", "Библиотека reportlab не установлена")
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

            if FONT_REGISTERED:
                title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontName='CyrillicFont-Bold', fontSize=18, alignment=1, spaceAfter=20)
                heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontName='CyrillicFont-Bold', fontSize=14, spaceAfter=10)
                normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontName='CyrillicFont', fontSize=10)
            else:
                title_style = styles['Title']
                heading_style = styles['Heading2']
                normal_style = styles['Normal']

            story.append(Paragraph(f"ИНВЕНТАРИЗАЦИОННАЯ ОПИСЬ", title_style))
            story.append(Paragraph(f"Филиал: {branch['name']}", heading_style))
            story.append(Paragraph(f"Адрес: {branch['address']}", normal_style))
            story.append(Paragraph(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style))
            story.append(Spacer(1, 10*mm))

            for floor in range(-3, branch['floors_count'] + 1):
                story.append(Paragraph(f"{self.get_floor_display_text(floor)}", heading_style))
                story.append(Spacer(1, 5*mm))

                map_info, markers = self.db.get_map_data(branch_id, floor)

                if map_info and os.path.exists(map_info['image_path']):
                    try:
                        img = Image(map_info['image_path'])
                        img.drawHeight = 80*mm
                        img.drawWidth = 120*mm
                        story.append(img)
                        story.append(Spacer(1, 5*mm))
                    except:
                        pass

                if markers:
                    for marker in markers:
                        room_id = marker[2]
                        room_number = marker[4]
                        room_name = marker[3]
                        equipment = self.get_equipment_for_room(room_id)

                        story.append(Paragraph(f"Кабинет {room_number} - {room_name}", normal_style))

                        if equipment:
                            data = [['№', 'Наименование', 'Категория', 'Кол-во', 'Цена', 'Сумма', 'Серийный №']]
                            room_total = 0
                            for i, eq in enumerate(equipment, 1):
                                try:
                                    sum_val = float(eq[3]) * float(eq[4] if eq[4] else 0)
                                    room_total += sum_val
                                except:
                                    sum_val = 0
                                data.append([
                                    str(i),
                                    (eq[0] or '')[:25],
                                    (eq[1] or '')[:15],
                                    str(eq[3]),
                                    f"{eq[4]:.2f}" if eq[4] else '0.00',
                                    f"{sum_val:.2f}",
                                    (eq[5] or '')[:15]
                                ])
                            data.append(['', '', '', '', '', f'Итого: {room_total:.2f}', ''])

                            table = Table(data, colWidths=[10*mm, 35*mm, 20*mm, 15*mm, 20*mm, 25*mm, 25*mm])
                            table.setStyle(TableStyle([
                                ('GRID', (0,0), (-1,-2), 0.5, colors.grey),
                                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                ('SPAN', (0,-1), (4,-1)),
                                ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                                ('FONTSIZE', (0,0), (-1,-1), 7),
                            ]))
                            story.append(table)
                            story.append(Spacer(1, 5*mm))
                else:
                    story.append(Paragraph("Нет помещений на этаже", normal_style))

                story.append(PageBreak())

            doc.build(story)
            self.show_status(f"Отчет сохранен")

        except Exception as e:
            self.show_status(f"Ошибка создания PDF: {str(e)}", True)

    def on_export_floor_pdf(self):
        """Экспорт одного этажа в PDF"""
        if not REPORTLAB_AVAILABLE:
            QMessageBox.warning(self, "Ошибка", "Библиотека reportlab не установлена")
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
            self, "Сохранить отчет", f"инвентаризация_{branch['name']}_{self.get_floor_display_text(floor)}.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        try:
            self.show_status("Генерация PDF...")

            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
            story = []
            styles = getSampleStyleSheet()

            if FONT_REGISTERED:
                title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontName='CyrillicFont-Bold', fontSize=18, alignment=1, spaceAfter=20)
                heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontName='CyrillicFont-Bold', fontSize=14, spaceAfter=10)
                normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontName='CyrillicFont', fontSize=10)
            else:
                title_style = styles['Title']
                heading_style = styles['Heading2']
                normal_style = styles['Normal']

            story.append(Paragraph(f"ИНВЕНТАРИЗАЦИОННАЯ ОПИСЬ", title_style))
            story.append(Paragraph(f"Филиал: {branch['name']}", heading_style))
            story.append(Paragraph(f"Адрес: {branch['address']}", normal_style))
            story.append(Paragraph(f"{self.get_floor_display_text(floor)}", heading_style))
            story.append(Paragraph(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style))
            story.append(Spacer(1, 10*mm))

            map_info, markers = self.db.get_map_data(branch_id, floor)

            if map_info and os.path.exists(map_info['image_path']):
                try:
                    img = Image(map_info['image_path'])
                    img.drawHeight = 100*mm
                    img.drawWidth = 150*mm
                    story.append(img)
                    story.append(Spacer(1, 5*mm))
                except:
                    pass

            if markers:
                for marker in markers:
                    room_id = marker[2]
                    room_number = marker[4]
                    room_name = marker[3]
                    equipment = self.get_equipment_for_room(room_id)

                    story.append(Paragraph(f"Кабинет {room_number} - {room_name}", normal_style))

                    if equipment:
                        data = [['№', 'Наименование', 'Категория', 'Кол-во', 'Цена', 'Сумма', 'Серийный №']]
                        room_total = 0
                        for i, eq in enumerate(equipment, 1):
                            try:
                                sum_val = float(eq[3]) * float(eq[4] if eq[4] else 0)
                                room_total += sum_val
                            except:
                                sum_val = 0
                            data.append([
                                str(i),
                                (eq[0] or '')[:25],
                                (eq[1] or '')[:15],
                                str(eq[3]),
                                f"{eq[4]:.2f}" if eq[4] else '0.00',
                                f"{sum_val:.2f}",
                                (eq[5] or '')[:15]
                            ])
                        data.append(['', '', '', '', '', f'Итого: {room_total:.2f}', ''])

                        table = Table(data, colWidths=[10*mm, 35*mm, 20*mm, 15*mm, 20*mm, 25*mm, 25*mm])
                        table.setStyle(TableStyle([
                            ('GRID', (0,0), (-1,-2), 0.5, colors.grey),
                            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('SPAN', (0,-1), (4,-1)),
                            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                            ('FONTSIZE', (0,0), (-1,-1), 7),
                        ]))
                        story.append(table)
                        story.append(Spacer(1, 5*mm))
            else:
                story.append(Paragraph("Нет помещений на этаже", normal_style))

            doc.build(story)
            self.show_status(f"Отчет сохранен")

        except Exception as e:
            self.show_status(f"Ошибка создания PDF: {str(e)}", True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())