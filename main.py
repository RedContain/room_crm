import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Импортируем модули
import paths
from database_handler import DatabaseHandler
from report_window import ReportWindow

def main():
    """Главная функция запуска"""
    # Создаем приложение
    app = QApplication(sys.argv)
    app.setApplicationName("Система учета оборудования")

    # Создаем необходимые директории
    os.makedirs(os.path.join(paths.get_base_path(), "database"), exist_ok=True)
    os.makedirs(paths.get_maps_dir(), exist_ok=True)
    os.makedirs(paths.get_report_images_dir(), exist_ok=True)

    # Инициализируем БД
    db = DatabaseHandler()

    # Запускаем главное окно
    window = ReportWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()