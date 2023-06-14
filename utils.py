import tkinter as tk
from tkinter import messagebox

def add_question(app):
    def save_question():
        question_text = question_entry.get("1.0", tk.END).strip()
        answer_text = answer_entry.get("1.0", tk.END).strip()
        difficulty_text = difficulty_entry.get()
        date_text = date_entry.get()
        memory_text = memory_entry.get()

        if not question_text or not answer_text or not difficulty_text or not date_text or not memory_text:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            difficulty = int(difficulty_text)
            memory = int(memory_text)
        except ValueError:
            messagebox.showerror("Ошибка", "Поле сложности и поле зауч должны быть целыми числами")
            return

        new_question = {
            "question": question_text,
            "answer": answer_text,
            "difficulty": difficulty,
            "date": date_text,
            "memory": memory
        }

        app.data.append(new_question)
        add_question_window.destroy()
        app.display_data()
        messagebox.showinfo("Сохранено", "Вопрос сохранен")

        if messagebox.askyesno("Добавить вопрос", "Хотите добавить еще один вопрос?"):
            add_question(app)
        # else:
        #     add_question_window.destroy()

    add_question_window = tk.Toplevel(app)
    add_question_window.title("Добавление нового вопроса")
    add_question_window.geometry("800x600")

    question_label = tk.Label(add_question_window, text="Вопрос:")
    question_label.pack()
    question_entry = tk.Text(add_question_window, height=5)
    question_entry.pack()

    answer_label = tk.Label(add_question_window, text="Ответ:")
    answer_label.pack()
    answer_entry = tk.Text(add_question_window, height=5)
    answer_entry.pack()

    difficulty_label = tk.Label(add_question_window, text="Сложность:")
    difficulty_label.pack()
    difficulty_entry = tk.Entry(add_question_window)
    difficulty_entry.insert(tk.END, "10")
    difficulty_entry.pack()

    date_label = tk.Label(add_question_window, text="Дата:")
    date_label.pack()
    date_entry = tk.Entry(add_question_window)
    date_entry.insert(tk.END, "01-01-2020")
    date_entry.pack()

    memory_label = tk.Label(add_question_window, text="Зауч:")
    memory_label.pack()
    memory_entry = tk.Entry(add_question_window)
    memory_entry.insert(tk.END, "0")
    memory_entry.pack()

    save_button = tk.Button(add_question_window, text="Сохранить", command=save_question)
    save_button.pack()

    cancel_button = tk.Button(add_question_window, text="Отменить", command=add_question_window.destroy)
    cancel_button.pack()

    add_question_window.mainloop()

def edit_question(app):
    selected_question = app.get_selected_question()
    if selected_question is None:
        messagebox.showerror("Ошибка", "Выберите вопрос для редактирования")
        return

    def save_question():
        question_text = question_entry.get("1.0", tk.END).strip()
        answer_text = answer_entry.get("1.0", tk.END).strip()
        difficulty_text = difficulty_entry.get()
        date_text = date_entry.get()
        memory_text = memory_entry.get()

        if not question_text or not answer_text or not difficulty_text or not date_text or not memory_text:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            difficulty = int(difficulty_text)
            memory = int(memory_text)
        except ValueError:
            messagebox.showerror("Ошибка", "Поле сложности и поле зауч должны быть целыми числами")
            return

        updated_question = {
            "question": question_text,
            "answer": answer_text,
            "difficulty": difficulty,
            "date": date_text,
            "memory": memory
        }

        app.data.remove(selected_question)
        app.data.append(updated_question)
        edit_question_window.destroy()
        app.display_data()
        messagebox.showinfo("Сохранено", "Вопрос отредактирован успешно")

    edit_question_window = tk.Toplevel(app)
    edit_question_window.title("Редактирование вопроса")
    edit_question_window.geometry("800x600")

    question_label = tk.Label(edit_question_window, text="Вопрос:")
    question_label.pack()
    question_entry = tk.Text(edit_question_window, height=5)
    question_entry.insert(tk.END, selected_question["question"])
    question_entry.pack()

    answer_label = tk.Label(edit_question_window, text="Ответ:")
    answer_label.pack()
    answer_entry = tk.Text(edit_question_window, height=5)
    answer_entry.insert(tk.END, selected_question["answer"])
    answer_entry.pack()

    difficulty_label = tk.Label(edit_question_window, text="Сложность:")
    difficulty_label.pack()
    difficulty_entry = tk.Entry(edit_question_window)
    difficulty_entry.insert(tk.END, str(selected_question["difficulty"]))
    difficulty_entry.pack()

    date_label = tk.Label(edit_question_window, text="Дата:")
    date_label.pack()
    date_entry = tk.Entry(edit_question_window)
    date_entry.insert(tk.END, selected_question["date"])
    date_entry.pack()

    memory_label = tk.Label(edit_question_window, text="Зауч:")
    memory_label.pack()
    memory_entry = tk.Entry(edit_question_window)
    memory_entry.insert(tk.END, str(selected_question["memory"]))
    memory_entry.pack()

    save_button = tk.Button(edit_question_window, text="Сохранить", command=save_question)
    save_button.pack()

    cancel_button = tk.Button(edit_question_window, text="Отменить", command=edit_question_window.destroy)
    cancel_button.pack()

    edit_question_window.mainloop()

def delete_question(app):
    # Получаем выделенный вопрос
    selected_item = app.table.selection()
    if not selected_item:
        print("Выделите вопрос для удаления")
        return

    # Получаем индекс выделенного вопроса
    index = int(app.table.item(selected_item)["values"][0]) - 1

    # Удаляем вопрос из self.data
    del app.data[index]

    # Обновляем отображение таблицы
    app.display_data()
    print("Вопрос удален")


def start_training(app):
    print("Начать обучение")
