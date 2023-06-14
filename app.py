import tkinter as tk
from tkinter import ttk, filedialog
import json
from utils import add_question, edit_question, delete_question, start_training

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zofamin: Total Memorization 🧠")
        self.geometry("1366x768")
        self.create_widgets()
        self.data = []  # Создаем переменную для хранения данных

    def create_widgets(self):
        self.menu = tk.Menu(self)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Закрыть", command=self.close_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выйти", command=self.quit)
        self.menu.add_cascade(label="Файл", menu=file_menu)

        questions_menu = tk.Menu(self.menu, tearoff=0)
        questions_menu.add_command(label="Добавить", command=add_question)
        questions_menu.add_command(label="Редактировать", command=edit_question)
        questions_menu.add_command(label="Удалить", command=lambda: delete_question(self))
        self.menu.add_cascade(label="Вопросы", menu=questions_menu)

        training_menu = tk.Menu(self.menu, tearoff=0)
        training_menu.add_command(label="Начать", command=start_training)
        self.menu.add_cascade(label="Обучение", menu=training_menu)

        self.config(menu=self.menu)

        self.table_frame = tk.Frame(self)
        self.table_frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(self.table_frame, columns=("number", "date", "question", "answer", "difficulty", "memory"),
                                  show="headings", selectmode="browse")
        self.table.column("number", width=20)
        self.table.column("date", width=50)
        self.table.column("question", minwidth=100)
        self.table.column("answer", minwidth=100)
        self.table.column("difficulty", width=50)
        self.table.column("memory", width=50)

        self.table.heading("number", text="№")
        self.table.heading("date", text="Дата")
        self.table.heading("question", text="Вопрос")
        self.table.heading("answer", text="Ответ")
        self.table.heading("difficulty", text="Сложность")
        self.table.heading("memory", text="Зауч")

        self.table.pack(fill="both", expand=True)

    def open_file(self):
        filetypes = [("JSON files", "*.json")]
        filepath = filedialog.askopenfilename(initialdir="data", title="Выберите файл", filetypes=filetypes)

        if filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                try:
                    self.data = json.load(file)  # Сохраняем данные в переменную класса
                    required_fields = ["date", "question", "answer", "difficulty", "memory"]

                    if all(field in self.data[0] for field in required_fields):
                        self.display_data()
                    else:
                        print("Данный файл не содержит вопросы в требуемом формате")

                except json.JSONDecodeError:
                    print("Ошибка чтения файла JSON")

    def display_data(self):
        # Очищаем таблицу
        self.table.delete(*self.table.get_children())

        # Заполняем таблицу данными из переменной класса
        for i, item in enumerate(self.data):
            number = i + 1
            date = item["date"]
            question = item["question"]
            answer = item["answer"]
            difficulty = item["difficulty"]
            memory = item["memory"]

            self.table.insert("", "end", values=(number, date, question, answer, difficulty, memory))

    def save_file(self):
        if not self.data:
            print("Нет данных для сохранения")
            return

        filetypes = [("JSON files", "*.json")]
        filepath = filedialog.asksaveasfilename(initialdir="data", title="Выберите файл для сохранения", filetypes=filetypes)

        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
                print("Файл сохранен")

    def close_file(self):
        self.data = []  # Очищаем данные
        self.table.delete(*self.table.get_children())  # Очищаем таблицу
        print("Файл закрыт")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
