import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QAction, QVBoxLayout, QWidget, QHeaderView, QTableWidgetItem
import json
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zofamin")
        self.resize(1366, 768)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Вопрос", "Ответ"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Задаем растягивание колонки "Вопрос"
        self.table.horizontalHeader().setStretchLastSection(True)

        self.create_actions()
        self.create_menus()

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_actions(self):
        self.open_action = QAction("Открыть", self)
        self.open_action.triggered.connect(self.open_file)

        self.exit_action = QAction("Выход", self)
        self.exit_action.triggered.connect(self.close)

        self.start_action = QAction("Начать", self)
        self.start_action.triggered.connect(self.start_training)

        self.add_action = QAction("Добавить вопрос", self)
        self.add_action.triggered.connect(self.add_question)

        self.edit_action = QAction("Редактировать вопрос", self)
        self.edit_action.triggered.connect(self.edit_question)

        self.delete_action = QAction("Удалить вопрос", self)
        self.delete_action.triggered.connect(self.delete_question)

    def create_menus(self):
        file_menu = self.menuBar().addMenu("Файл")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.exit_action)

        training_menu = self.menuBar().addMenu("Обучение")
        training_menu.addAction(self.start_action)
        training_menu.addAction(self.add_action)
        training_menu.addAction(self.edit_action)
        training_menu.addAction(self.delete_action)

     
    def open_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setDirectory("data")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if isinstance(data, list) and all("question" in item and "answer" in item for item in data):
                        self.load_data_to_table(data)
                    else:
                        print("Файл не соответствует требованиям")
            except (IOError, json.JSONDecodeError) as e:
                print(f"Ошибка при открытии файла: {str(e)}")

    def load_data_to_table(self, data):
        self.table.setRowCount(0)
        for row, item in enumerate(data):
            question = item["question"]
            answer = item["answer"]
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(question))
            self.table.setItem(row, 1, QTableWidgetItem(answer))

    def start_training(self):
        print("Начать обучение")

    def add_question(self):
        print("Добавить вопрос")

    def edit_question(self):
        print("Редактировать вопрос")

    def delete_question(self):
        print("Удалить вопрос")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
