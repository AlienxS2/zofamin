import tkinter as tk
from tkinter import Toplevel, Label, Button, Entry, messagebox
from datetime import datetime

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
    if not app.data:
        messagebox.showinfo("Нет вопросов", "Нет вопросов для обучения")
        return

    def calculate_how_old(date):
        current_date = datetime.now().date()
        question_date = datetime.strptime(date, "%d.%m.%Y").date()
        return (current_date - question_date).days

    def calculate_keff(difficulty, how_old):
        return difficulty * how_old

    def sort_by_keff(data):
        return sorted(data, key=lambda item: item["keff"], reverse=True)

    must_memorise = []
    just_memorise = []

    for item in app.data:
        how_old = calculate_how_old(item["date"])
        keff = calculate_keff(item["difficulty"], how_old)
        item["keff"] = keff

        if item["memory"] == 1:
            must_memorise.append(item)
        else:
            just_memorise.append(item)

    must_memorise = sort_by_keff(must_memorise)
    just_memorise = sort_by_keff(just_memorise)

    def show_question():
        nonlocal current_index

        if must_memorise:
            question = must_memorise.pop(0)
        elif just_memorise:
            question = just_memorise.pop(0)
        else:
            messagebox.showinfo("Тренировка завершена", "Больше нет вопросов")
            return

        question_window = tk.Toplevel(app)
        question_window.title("Вопрос")
        question_window.geometry("800x600")

        question_label = tk.Label(question_window, text="Вопрос:")
        question_label.pack()
        question_entry = tk.Text(question_window, height=20)
        question_entry.insert(tk.END, question["question"])
        question_entry.pack()

        def show_answer():
            nonlocal current_index

            question_window.destroy()

            answer_window = tk.Toplevel(app)
            answer_window.title("Ответ")
            answer_window.geometry("800x600")

            answer_label = tk.Label(answer_window, text="Ответ:")
            answer_label.pack()
            answer_entry = tk.Text(answer_window, height=20)
            answer_entry.insert(tk.END, question["answer"])
            answer_entry.pack()

            difficulty_label = tk.Label(answer_window, text="Сложность:")
            difficulty_label.pack()
            difficulty_entry = tk.Entry(answer_window)
            difficulty_entry.insert(tk.END, str(question["difficulty"]))
            difficulty_entry.pack()

            memory_label = tk.Label(answer_window, text="Зауч:")
            memory_label.pack()
            memory_entry = tk.Entry(answer_window)
            memory_entry.insert(tk.END, str(question["memory"]))
            memory_entry.pack()

            def save_feedback():
                nonlocal current_index

                new_difficulty = int(difficulty_entry.get())
                new_memory = int(memory_entry.get())

                app.data[current_index]["difficulty"] = new_difficulty
                app.data[current_index]["memory"] = new_memory

                answer_window.destroy()

                if must_memorise:
                    show_question()
                elif just_memorise:
                    show_question()
                else:
                    messagebox.showinfo("Тренировка завершена", "Больше нет вопросов")

            finish_button = tk.Button(answer_window, text="Далее", command=save_feedback)
            finish_button.pack()

            finish_training_button = tk.Button(answer_window, text="Завершить обучение", command=answer_window.destroy)
            finish_training_button.pack()

        next_button = tk.Button(question_window, text="Показать ответ", command=show_answer)
        next_button.pack()

        current_index = app.data.index(question)

    current_index = None
    show_question()
