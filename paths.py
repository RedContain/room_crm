import os
import sys

def get_base_path():
    """Возвращает базовый путь в зависимости от того, запущено ли приложение как exe"""
    if getattr(sys, 'frozen', False):
        # Запущено как exe
        return os.path.dirname(sys.executable)
    else:
        # Запущено как скрипт
        return os.path.dirname(os.path.abspath(__file__))

def get_db_file_path():
    """Возвращает путь к файлу базы данных"""
    base_path = get_base_path()
    db_dir = os.path.join(base_path, "database")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "company.db")

def get_ui_path(filename):
    """Возвращает путь к UI файлу"""
    base_path = get_base_path()

    # Проверяем несколько возможных расположений
    possible_paths = [
        os.path.join(base_path, "UI_diagramms", filename),
        os.path.join(base_path, filename),
        os.path.join(base_path, "python_files", filename),
        os.path.join(os.path.dirname(base_path), "UI_diagramms", filename)
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # Если не нашли, возвращаем путь по умолчанию
    return os.path.join(base_path, "UI_diagramms", filename)

def get_maps_dir():
    """Возвращает путь к папке с картами этажей"""
    base_path = get_base_path()
    maps_dir = os.path.join(base_path, "floor_maps")
    os.makedirs(maps_dir, exist_ok=True)
    return maps_dir

def get_report_images_dir():
    """Возвращает путь к папке с изображениями для отчетов"""
    base_path = get_base_path()
    images_dir = os.path.join(base_path, "report_images")
    os.makedirs(images_dir, exist_ok=True)
    return images_dir