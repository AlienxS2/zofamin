def add_question():
    print("Добавить вопрос")

def edit_question():
    print("Редактировать вопрос")

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


def start_training():
    print("Начать обучение")
