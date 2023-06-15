import tkinter as tk
from tkinter import filedialog
import json


def process_file():
    # Открываем диалоговое окно для выбора файла
    file_path = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')])

    if file_path:
        try:
            # Открываем файл и загружаем его содержимое
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Проверяем наличие необходимых полей
            if all(('question' in item and 'answer' in item) for item in data):
                # Удаляем все поля, кроме 'question' и 'answer'
                data = [{'question': item['question'], 'answer': item['answer']} for item in data]

                # Перезаписываем файл с обновленными данными
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False)

                # Выводим уведомление об успешной обработке
                tk.messagebox.showinfo('Успех', 'Файл успешно обработан')
            else:
                # Выводим уведомление о неподходящем файле
                tk.messagebox.showwarning('Ошибка', 'Файл не подходит')
        except json.JSONDecodeError:
            # Выводим уведомление об ошибке при чтении файла
            tk.messagebox.showerror('Ошибка', 'Ошибка чтения файла')
    else:
        # Выводим уведомление, если файл не был выбран
        tk.messagebox.showinfo('Информация', 'Файл не выбран')


# Создаем графический интерфейс
root = tk.Tk()

# Создаем кнопку "Выбрать файл"
select_button = tk.Button(root, text='Выбрать файл', command=process_file)
select_button.pack()

# Запускаем основной цикл обработки событий
root.mainloop()
