import sys
import os
import shutil
from datetime import datetime

# Добавляем путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QFile, QIODevice
from PySide6.QtGui import QPixmap, QPen, QBrush, QColor, QFont
from PySide6.QtWidgets import QMessageBox, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem
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
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️ reportlab не установлен, функции PDF будут недоступны")

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

        self.load_ui()
        self.setup_ui()
        self.connect_signals()
        self.load_branches_to_combobox()
        self.show_status("Готов к работе")

    def load_ui(self):
        loader = QUiLoader()
        ui_file_path = paths.get_ui_path("UI_diagramms/plane.ui")

        if not os.path.exists(ui_file_path):
            QMessageBox.critical(self, "Ошибка", f"Файл интерфейса не найден:\n{ui_file_path}")
            sys.exit(1)

        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл интерфейса:\n{ui_file_path}")
            sys.exit(1)

        self.ui = loader.load(ui_file, self)
        ui_file.close()

        if not self.ui:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить интерфейс")
            sys.exit(1)

        self.setCentralWidget(self.ui.centralwidget)

    def setup_ui(self):
        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("QLabel { color: green; font-weight: bold; padding: 2px; }")
        self.ui.statusbar.addPermanentWidget(self.status_label)

        if hasattr(self.ui, 'tableView'):
            self.ui.tableView.doubleClicked.connect(self.on_table_double_click)

    def show_status(self, message, is_error=False):
        self.status_label.setText(f"  {message}  ")
        if is_error:
            self.status_label.setStyleSheet("QLabel { color: red; font-weight: bold; padding: 2px; }")
        else:
            self.status_label.setStyleSheet("QLabel { color: green; font-weight: bold; padding: 2px; }")

    def connect_signals(self):
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
        branches = self.db.get_all_branches()
        for combo_name in ['comboBox', 'comboBox_2']:
            combo = getattr(self.ui, combo_name, None)
            if combo:
                combo.clear()
                combo.addItem("Выберите филиал", None)
                for branch in branches:
                    combo.addItem(branch['name'], branch['branch_id'])
        self.show_status(f"Загружено {len(branches)} филиалов")

    def clear_graphics_view(self, graphics_view):
        if graphics_view:
            graphics_view.setScene(None)

    def on_branch_changed_settings(self, index):
        self.clear_graphics_view(getattr(self.ui, 'graphicsView', None))
        self.current_scene = None
        self.marker_items = []
        self.current_map_id = None
        if hasattr(self.ui, 'spinBox'):
            self.ui.spinBox.setValue(1)
        self.load_rooms_to_table()

    def on_floor_changed_settings(self, floor):
        self.load_rooms_to_table()
        branch_id = self.ui.comboBox.currentData() if hasattr(self.ui, 'comboBox') else None
        if branch_id:
            self.display_map_settings(branch_id, floor)

    def load_rooms_to_table(self):
        if not hasattr(self.ui, 'tableView'):
            return

        branch_id = self.ui.comboBox.currentData() if hasattr(self.ui, 'comboBox') else None
        floor = self.ui.spinBox.value() if hasattr(self.ui, 'spinBox') else 1

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

        self.pending_marker.setBrush(QBrush(QColor(0, 255, 0, 180)))
        self.pending_marker.setData(0, room_id)

        if self.current_scene:
            font = QFont("Arial", 8)
            text = self.current_scene.addText(f"{room_number}", font)
            text.setPos(self.pending_marker.rect().center().x() + 15,
                        self.pending_marker.rect().center().y() - 10)
            text.setData(0, room_id)

            self.marker_items.append(self.pending_marker)
            self.marker_items.append(text)

        self.pending_marker = None
        self.show_status(f"Точка привязана к комнате {room_number} - {room_name}")

    def on_load_map_clicked(self):
        branch_id = self.ui.comboBox.currentData() if hasattr(self.ui, 'comboBox') else None
        floor = self.ui.spinBox.value() if hasattr(self.ui, 'spinBox') else 1

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
            branch_id = self.ui.comboBox.currentData() if hasattr(self.ui, 'comboBox') else None
            floor = self.ui.spinBox.value() if hasattr(self.ui, 'spinBox') else 1
            self.display_map_settings(branch_id, floor)
            self.show_status("Все точки удалены")

    def on_save_map_clicked(self):
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
        if not self.current_scene:
            return

        if self.pending_marker and self.current_scene:
            self.current_scene.removeItem(self.pending_marker)

        pen = QPen(Qt.blue)
        pen.setWidth(2)
        brush = QBrush(QColor(0, 0, 255, 180))

        ellipse = QGraphicsEllipseItem(x - 8, y - 8, 16, 16)
        ellipse.setPen(pen)
        ellipse.setBrush(brush)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        ellipse.setData(0, None)

        self.current_scene.addItem(ellipse)
        self.pending_marker = ellipse

        self.show_status("Точка поставлена, выберите комнату в таблице двойным кликом")

    def display_map_settings(self, branch_id, floor):
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
            pen.setWidth(2)
            brush = QBrush(QColor(0, 255, 0, 180))

            ellipse = QGraphicsEllipseItem(x - 8, y - 8, 16, 16)
            ellipse.setPen(pen)
            ellipse.setBrush(brush)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
            ellipse.setData(0, room_id)
            scene.addItem(ellipse)
            self.marker_items.append(ellipse)

            font = QFont("Arial", 8)
            text = scene.addText(f"{room_number}", font)
            text.setPos(x + 12, y - 8)
            text.setData(0, room_id)
            self.marker_items.append(text)

        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(pixmap_item, Qt.KeepAspectRatio)
        self.show_status(f"Загружено {len(markers)} точек")

    def on_branch_changed_display(self, index):
        branch_id = self.ui.comboBox_2.currentData() if hasattr(self.ui, 'comboBox_2') else None
        if branch_id and hasattr(self.ui, 'spinBox_2'):
            self.ui.spinBox_2.setValue(1)
            self.display_map_display(branch_id, 1)

    def on_floor_changed_display(self, floor):
        branch_id = self.ui.comboBox_2.currentData() if hasattr(self.ui, 'comboBox_2') else None
        if branch_id:
            self.display_map_display(branch_id, floor)

    def display_map_display(self, branch_id, floor):
        if not hasattr(self.ui, 'graphicsView_2'):
            return

        self.clear_graphics_view(self.ui.graphicsView_2)

        map_info, markers = self.db.get_map_data(branch_id, floor)
        if not map_info:
            self.show_status(f"Нет схемы для этажа {floor}", True)
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
            pen.setWidth(2)
            brush = QBrush(QColor(0, 0, 255, 100))

            ellipse = QGraphicsEllipseItem(x - 8, y - 8, 16, 16)
            ellipse.setPen(pen)
            ellipse.setBrush(brush)
            ellipse.setData(0, room_id)
            ellipse.setToolTip(f"{room_number} - {room_name}")
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, False)
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable, False)
            scene.addItem(ellipse)
            self.marker_items_display.append(ellipse)

            font = QFont("Arial", 6)
            text = scene.addText(room_number, font)
            text.setPos(x + 6, y - 6)
            text.setFlag(QGraphicsEllipseItem.ItemIsSelectable, False)
            self.marker_items_display.append(text)

        self.ui.graphicsView_2.setScene(scene)
        self.ui.graphicsView_2.fitInView(pixmap_item, Qt.KeepAspectRatio)
        self.show_status(f"Показан этаж {floor}, {len(markers)} помещений")

    def on_export_all_pdf(self):
        if not REPORTLAB_AVAILABLE:
            QMessageBox.warning(self, "Ошибка", "Библиотека reportlab не установлена. Установите: pip install reportlab")
            return

        branch_id = self.ui.comboBox_2.currentData() if hasattr(self.ui, 'comboBox_2') else None
        if not branch_id:
            self.show_status("Выберите филиал!", True)
            return

        branch = self.db.get_branch(branch_id)
        if not branch:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет", f"отчет_{branch['name']}.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        try:
            self.show_status("Генерация PDF...")

            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
            story = []
            styles = getSampleStyleSheet()

            story.append(Paragraph(f"Филиал: {branch['name']}", styles['Title']))
            story.append(Paragraph(f"Адрес: {branch['address']}", styles['Normal']))
            story.append(Paragraph(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 10*mm))

            for floor in range(1, branch['floors_count'] + 1):
                story.append(Paragraph(f"Этаж {floor}", styles['Heading2']))
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
                    data = [['№', 'Кабинет', 'Название', 'Вместимость']]
                    for i, marker in enumerate(markers, 1):
                        room = self.db.get_room(marker['room_id'])
                        data.append([
                            str(i),
                            marker['room_number'],
                            marker['room_name'],
                            str(room['capacity'] if room else '')
                        ])

                    table = Table(data, colWidths=[20*mm, 30*mm, 70*mm, 30*mm])
                    table.setStyle(TableStyle([
                        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ]))
                    story.append(table)

                story.append(Spacer(1, 10*mm))

            doc.build(story)
            self.show_status(f"Отчет сохранен: {os.path.basename(file_path)}")

        except Exception as e:
            self.show_status(f"Ошибка создания PDF: {str(e)}", True)

    def on_export_floor_pdf(self):
        if not REPORTLAB_AVAILABLE:
            QMessageBox.warning(self, "Ошибка", "Библиотека reportlab не установлена. Установите: pip install reportlab")
            return

        branch_id = self.ui.comboBox_2.currentData() if hasattr(self.ui, 'comboBox_2') else None
        floor = self.ui.spinBox_2.value() if hasattr(self.ui, 'spinBox_2') else 1

        if not branch_id:
            self.show_status("Выберите филиал!", True)
            return

        branch = self.db.get_branch(branch_id)
        if not branch:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет", f"отчет_{branch['name']}_этаж_{floor}.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        try:
            self.show_status("Генерация PDF...")

            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
            story = []
            styles = getSampleStyleSheet()

            story.append(Paragraph(f"Филиал: {branch['name']}", styles['Title']))
            story.append(Paragraph(f"Адрес: {branch['address']}", styles['Normal']))
            story.append(Paragraph(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 10*mm))

            story.append(Paragraph(f"Этаж {floor}", styles['Heading2']))
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
                data = [['№', 'Кабинет', 'Название', 'Вместимость']]
                for i, marker in enumerate(markers, 1):
                    room = self.db.get_room(marker['room_id'])
                    data.append([
                        str(i),
                        marker['room_number'],
                        marker['room_name'],
                        str(room['capacity'] if room else '')
                    ])

                table = Table(data, colWidths=[20*mm, 30*mm, 70*mm, 30*mm])
                table.setStyle(TableStyle([
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                    ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ]))
                story.append(table)

            doc.build(story)
            self.show_status(f"Отчет сохранен: {os.path.basename(file_path)}")

        except Exception as e:
            self.show_status(f"Ошибка создания PDF: {str(e)}", True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())