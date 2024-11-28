# import sys
# import os
# import csv
# import pandas as pd
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog,
#                              QLabel, QProgressBar, QVBoxLayout, QWidget, QFrame)
# from PyQt6.QtCore import Qt, QThread, pyqtSignal
# from PyQt6.QtGui import QDropEvent, QDragEnterEvent
# from customdict_mapmaint import get_golden_dict
# import json
# import requests
#
#
# async def validate(file_path):
#     requests.post('http://127.0.0.1:8080')
#
# class WorkerThread(QThread):
#     progress = pyqtSignal(int)
#     finished = pyqtSignal(dict)
#     error = pyqtSignal(str)
#
#     def __init__(self, file_path):
#         super().__init__()
#         self.file_path = file_path
#
#     def run(self):
#         try:
#             # Имитация прогресса обработки
#             self.progress.emit(20)
#             matrix = self.matrix_from_csv(self.file_path)
#             self.progress.emit(60)
#             result = get_golden_dict(matrix)
#             # result = requests.get('http://127.0.0.1:8000')
#             self.progress.emit(100)
#             self.finished.emit(result)
#         except Exception as e:
#             self.error.emit(str(e))
#
#     def matrix_from_csv(self, file_path):
#         matrix = []
#         with open(file_path, mode="r", encoding="utf-8") as file:
#             csv_reader = csv.reader(file)
#             for row in csv_reader:
#                 matrix.append(row)
#         return matrix
#
#
# class DropZone(QFrame):
#     def __init__(self):
#         super().__init__()
#         self.setAcceptDrops(True)
#         self.setStyleSheet("""
#             QFrame {
#                 border: 2px dashed #666;
#                 border-radius: 10px;
#                 background-color: #2a2a2a;
#                 min-height: 200px;
#             }
#             QFrame:hover {
#                 border-color: #888;
#                 background-color: #333;
#             }
#         """)
#
#         layout = QVBoxLayout()
#         self.label = QLabel("Перетащите файл сюда или нажмите для выбора")
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.label)
#         self.setLayout(layout)
#
#     def dragEnterEvent(self, event: QDragEnterEvent):
#         if event.mimeData().hasUrls():
#             event.accept()
#         else:
#             event.ignore()
#
#     def dropEvent(self, event: QDropEvent):
#         files = [u.toLocalFile() for u in event.mimeData().urls()]
#         if files:
#             self.parent().process_file(files[0])
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Data Processor")
#         self.setMinimumSize(600, 400)
#
#         # Основной виджет
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         layout = QVBoxLayout(main_widget)
#
#         # Зона для перетаскивания
#         self.drop_zone = DropZone()
#         self.drop_zone.mousePressEvent = lambda x: self.open_file_dialog()
#         layout.addWidget(self.drop_zone)
#
#         # Прогресс бар
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setVisible(False)
#         self.progress_bar.setStyleSheet("""
#             QProgressBar {
#                 border: 2px solid #666;
#                 border-radius: 5px;
#                 text-align: center;
#             }
#             QProgressBar::chunk {
#                 background-color: #3daee9;
#             }
#         """)
#         layout.addWidget(self.progress_bar)
#
#         # Статус
#         self.status_label = QLabel()
#         self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.status_label)
#
#         # Кнопка сохранения
#         self.save_button = QPushButton("Сохранить результат")
#         self.save_button.setVisible(False)
#         self.save_button.clicked.connect(self.save_result)
#         self.save_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #3daee9;
#                 border: none;
#                 border-radius: 5px;
#                 padding: 10px;
#                 color: white;
#             }
#             QPushButton:hover {
#                 background-color: #4dc4ff;
#             }
#         """)
#         layout.addWidget(self.save_button)
#
#         self.result = None
#
#     def open_file_dialog(self):
#         file_name, _ = QFileDialog.getOpenFileName(
#             self,
#             "Выберите файл",
#             "",
#             "CSV Files (*.csv);;All Files (*)"
#         )
#         if file_name:
#             self.process_file(file_name)
#
#     def process_file(self, file_path):
#         self.progress_bar.setVisible(True)
#         self.status_label.setText("Обработка файла...")
#         self.save_button.setVisible(False)
#
#         self.worker = WorkerThread(file_path)
#         self.worker.progress.connect(self.update_progress)
#         self.worker.finished.connect(self.process_complete)
#         self.worker.error.connect(self.process_error)
#         self.worker.start()
#
#     def update_progress(self, value):
#         self.progress_bar.setValue(value)
#
#     def process_complete(self, result):
#         self.result = result
#         self.status_label.setText("Обработка завершена успешно!")
#         self.save_button.setVisible(True)
#
#     def process_error(self, error_message):
#         self.status_label.setText(f"Ошибка: {error_message}")
#         self.progress_bar.setVisible(False)
#
#     def save_result(self):
#         if self.result:
#             file_name, _ = QFileDialog.getSaveFileName(
#                 self,
#                 "Сохранить результат",
#                 "",
#                 "JSON Files (*.json);;All Files (*)"
#             )
#             if file_name:
#                 with open(file_name, 'w', encoding='utf-8') as f:
#                     json.dump(self.result, f, ensure_ascii=False, indent=4)
#                 self.status_label.setText("Результат сохранен!")
#
#
# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())


import sys
import os
import json
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QFileDialog, QTextEdit)
from PyQt5.QtCore import QThread, pyqtSignal
import requests
from flask import Flask, request
from threading import Thread
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Добавляем обработчик запросов для логирования
@app.before_request
def log_request_info():
    logger.info('Headers: %s', request.headers)
    logger.info('Body: %s', request.get_data())
    logger.info(f"""Request:
        Method: {request.method}
        Path: {request.path}
        IP: {request.remote_addr}
        Time: {datetime.now()}
    """)

# Добавляем обработчик ответов для логирования
@app.after_request
def log_response_info(response):
    logger.info(f"""Response:
        Status: {response.status}
        Time: {datetime.now()}
    """)
    return response


class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        logger.info("Starting Flask server...")
        app.run(port=8080)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Converter")
        self.setGeometry(100, 100, 600, 400)

        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Создаем кнопку для выбора файла
        self.select_button = QPushButton("Select CSV File")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        # Создаем текстовое поле для логов
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # Создаем директорию для загруженных файлов
        self.upload_dir = "uploaded_files"
        os.makedirs(self.upload_dir, exist_ok=True)

        # Запускаем Flask сервер в отдельном потоке
        server_thread = ServerThread()
        server_thread.start()

    def log_message(self, message):
        """Добавляет сообщение в лог"""
        self.log_text.append(message)

    def select_file(self):
        """Обработчик выбора файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            try:
                # Копируем файл в директорию uploaded_files
                filename = os.path.basename(file_path)
                save_path = os.path.join(self.upload_dir, filename)
                with open(file_path, 'rb') as src, open(save_path, 'wb') as dst:
                    dst.write(src.read())

                self.log_message(f"File saved to: {save_path}")

                # Отправляем POST запрос
                response = requests.post(
                    'http://127.0.0.1:3000',
                    json={'file_path': save_path}
                )

                if response.ok:
                    self.log_message("File path sent successfully")
                else:
                    self.log_message(f"Error sending file path: {response.status_code}")

            except Exception as e:
                self.log_message(f"Error: {str(e)}")


def convert_csv_to_json(file_path):
    """Конвертирует CSV файл в JSON"""
    try:
        data = []
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)

        json_path = os.path.splitext(file_path)[0] + '.json'
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        return True, json_path
    except Exception as e:
        return False, str(e)


@app.route('/', methods=['POST'])
def handle_request():
    """Обработчик POST запросов"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')

        logger.info(f"Received request to convert file: {file_path}")

        if not file_path:
            logger.error("No file_path provided")
            return {'error': 'No file_path provided'}, 400

        success, result = convert_csv_to_json(file_path)
        if success:
            logger.info(f"Successfully converted file to: {result}")
            return {'message': f'File converted successfully: {result}'}, 200
        else:
            logger.error(f"Conversion failed: {result}")
            return {'error': f'Conversion failed: {result}'}, 500

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {'error': str(e)}, 500


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()





