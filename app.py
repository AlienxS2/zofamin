import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QAction, QVBoxLayout, QWidget, QHeaderView
from open_file import open_file
from start_training import start_training
from add_question import add_question
from edit_question import edit_question
from delete_question import delete_question

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zofamin")
        self.resize(1366, 768)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Вопрос", "Ответ"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
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
        self.open_action.triggered.connect(open_file)

        self.exit_action = QAction("Выход", self)
        self.exit_action.triggered.connect(self.close)

        self.start_action = QAction("Начать", self)
        self.start_action.triggered.connect(start_training)

        self.add_action = QAction("Добавить вопрос", self)
        self.add_action.triggered.connect(add_question)

        self.edit_action = QAction("Редактировать вопрос", self)
        self.edit_action.triggered.connect(edit_question)

        self.delete_action = QAction("Удалить вопрос", self)
        self.delete_action.triggered.connect(delete_question)

    def create_menus(self):
        file_menu = self.menuBar().addMenu("Файл")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.exit_action)

        training_menu = self.menuBar().addMenu("Обучение")
        training_menu.addAction(self.start_action)
        training_menu.addAction(self.add_action)
        training_menu.addAction(self.edit_action)
        training_menu.addAction(self.delete_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
