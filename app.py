import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QAction, QVBoxLayout, QWidget, QHeaderView, QTableWidgetItem, QTextEdit, QPushButton, QFileDialog, QMessageBox, QDialog, QLabel, QPlainTextEdit
import json
import random

class TrainingWindow(QDialog):
    def __init__(self, questions):
        super().__init__()
        self.setWindowTitle("Обучение")
        self.resize(800, 600)

        self.current_question_index = 0
        self.questions = questions

        self.question_text = QTextEdit(self.questions[self.current_question_index]["question"])
        self.question_text.setReadOnly(True)

        self.answer_text = QTextEdit(self.questions[self.current_question_index]["answer"])
        self.answer_text.setReadOnly(True)
        self.answer_text.hide()

        self.show_answer_button = QPushButton("Показать ответ")
        self.next_question_button = QPushButton("Следующий вопрос")
        self.finish_button = QPushButton("Завершить")

        self.show_answer_button.clicked.connect(self.show_answer)
        self.next_question_button.clicked.connect(self.next_question)
        self.finish_button.clicked.connect(self.close)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.question_text)
        main_layout.addWidget(self.answer_text)
        main_layout.addWidget(self.show_answer_button)
        main_layout.addWidget(self.next_question_button)
        main_layout.addWidget(self.finish_button)

        self.setLayout(main_layout)

    def show_answer(self):
        self.answer_text.show()

    def next_question(self):
        self.current_question_index = (self.current_question_index + 1) % len(self.questions)
        self.question_text.setPlainText(self.questions[self.current_question_index]["question"])
        self.answer_text.setPlainText(self.questions[self.current_question_index]["answer"])
        self.answer_text.hide()


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

        self.save_action = QAction("Сохранить", self)
        self.save_action.triggered.connect(self.save_file)

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
        file_menu.addAction(self.save_action)
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
                        QMessageBox.warning(self, "Ошибка", "Файл не соответствует требованиям")
            except (IOError, json.JSONDecodeError) as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при открытии файла: {str(e)}")

    def save_file(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения")
            return

        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setDirectory("data")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                data = []
                for row in range(self.table.rowCount()):
                    question = self.table.item(row, 0).text()
                    answer = self.table.item(row, 1).text()
                    data.append({"question": question, "answer": answer})

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)

                QMessageBox.information(self, "Сохранено", "Данные успешно сохранены")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении файла: {str(e)}")

    def load_data_to_table(self, data):
        self.table.setRowCount(0)
        for row, item in enumerate(data):
            question = item["question"]
            answer = item["answer"]
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(question))
            self.table.setItem(row, 1, QTableWidgetItem(answer))

    def start_training(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите файл для обучения")
        else:
            questions = []
            for row in range(self.table.rowCount()):
                question = self.table.item(row, 0).text()
                answer = self.table.item(row, 1).text()
                questions.append({"question": question, "answer": answer})

            random.shuffle(questions)

            training_window = TrainingWindow(questions)
            training_window.exec_()

    def add_question(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить вопрос")
        dialog.resize(800, 600)

        question_text = QPlainTextEdit()
        answer_text = QPlainTextEdit()

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        def save_question():
            question = question_text.toPlainText()
            answer = answer_text.toPlainText()
            if question and answer:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(question))
                self.table.setItem(row, 1, QTableWidgetItem(answer))
                dialog.close()
            else:
                QMessageBox.warning(dialog, "Ошибка", "Заполните все поля")

        save_button.clicked.connect(save_question)
        cancel_button.clicked.connect(dialog.close)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Вопрос:"))
        layout.addWidget(question_text)
        layout.addWidget(QLabel("Ответ:"))
        layout.addWidget(answer_text)
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def edit_question(self):
        selected_rows = set(index.row() for index in self.table.selectionModel().selectedIndexes())

        if len(selected_rows) == 1:
            row = selected_rows.pop()
            question = self.table.item(row, 0).text()
            answer = self.table.item(row, 1).text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Редактировать вопрос")
            dialog.resize(800, 600)

            question_text = QPlainTextEdit(question)
            answer_text = QPlainTextEdit(answer)

            save_button = QPushButton("Сохранить")
            cancel_button = QPushButton("Отмена")

            def save_question():
                new_question = question_text.toPlainText()
                new_answer = answer_text.toPlainText()
                if new_question and new_answer:
                    self.table.setItem(row, 0, QTableWidgetItem(new_question))
                    self.table.setItem(row, 1, QTableWidgetItem(new_answer))
                    dialog.close()
                else:
                    QMessageBox.warning(dialog, "Ошибка", "Заполните все поля")

            save_button.clicked.connect(save_question)
            cancel_button.clicked.connect(dialog.close)

            layout = QVBoxLayout()
            layout.addWidget(QLabel("Вопрос:"))
            layout.addWidget(question_text)
            layout.addWidget(QLabel("Ответ:"))
            layout.addWidget(answer_text)
            layout.addWidget(save_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()
        elif len(selected_rows) == 0:
            selected_cells = self.table.selectionModel().selectedIndexes()
            if len(selected_cells) == 1:
                row = selected_cells[0].row()
                question = self.table.item(row, 0).text()
                answer = self.table.item(row, 1).text()

                dialog = QDialog(self)
                dialog.setWindowTitle("Редактировать вопрос")
                dialog.resize(800, 600)

                question_text = QPlainTextEdit(question)
                answer_text = QPlainTextEdit(answer)

                save_button = QPushButton("Сохранить")
                cancel_button = QPushButton("Отмена")

                def save_question():
                    new_question = question_text.toPlainText()
                    new_answer = answer_text.toPlainText()
                    if new_question and new_answer:
                        self.table.setItem(row, 0, QTableWidgetItem(new_question))
                        self.table.setItem(row, 1, QTableWidgetItem(new_answer))
                        dialog.close()
                    else:
                        QMessageBox.warning(dialog, "Ошибка", "Заполните все поля")

                save_button.clicked.connect(save_question)
                cancel_button.clicked.connect(dialog.close)

                layout = QVBoxLayout()
                layout.addWidget(QLabel("Вопрос:"))
                layout.addWidget(question_text)
                layout.addWidget(QLabel("Ответ:"))
                layout.addWidget(answer_text)
                layout.addWidget(save_button)
                layout.addWidget(cancel_button)

                dialog.setLayout(layout)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "Ошибка", "Выберите одну строку или одну ячейку для редактирования")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите одну строку или одну ячейку для редактирования")



    def delete_question(self):
        selected_rows = self.table.selectionModel().selectedRows()
        selected_cells = self.table.selectionModel().selectedIndexes()
        
        if len(selected_rows) == 1:
            row = selected_rows[0].row()
            self.table.removeRow(row)
            QMessageBox.information(self, "Удалено", "Выбранный вопрос удален")
        elif len(selected_cells) == 1:
            row = selected_cells[0].row()
            self.table.removeRow(row)
            QMessageBox.information(self, "Удалено", "Выбранный вопрос удален")
        else:
            QMessageBox.warning(self, "Ошибка", "Выделите вопрос для удаления")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
