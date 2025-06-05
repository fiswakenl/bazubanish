# Проект для парсинга вопросов с Google Sheets

## Установка зависимостей
# 1. **Создайте виртуальное окружение:**  
#    `python -m venv .venv`
# 2. **Активируйте виртуальное окружение:**  
#    - **Для Windows:** `.\.venv\Scripts\activate`  
#    - **Для macOS и Linux:** `source .venv/bin/activate`
# 3. **Выполните установку зависимостей:**  
#    `pip install pandas requests`
#    `pip install --upgrade pip`

## Запуск скрипта
# `python script.py`

## Структура проекта
# - `script.py` — основной скрипт для парсинга данных.

import os
import pandas as pd
from data_fetcher import data_fetcher


def save_questions_with_uids(data_frame: pd.DataFrame, output_directory: str):
    # Создание директории, если не существует
    os.makedirs(output_directory, exist_ok=True)

    # Подсчитываем количество повторений для каждого uid
    uid_counts = data_frame["uid"].value_counts().reset_index()
    uid_counts.columns = ["uid", "repetitions"]

    # Объединяем с основной таблицей, чтобы получить текст вопроса
    merged = data_frame.merge(uid_counts, on="uid")

    # Группируем данные по Category и uid, выбираем первый вопрос из группы
    grouped = (
        merged.groupby(["Category", "uid"])
        .agg(Question=("Question", "first"), repetitions=("repetitions", "first"))
        .reset_index()
    )

    # Подсчитываем общее количество повторений для каждой категории
    category_counts = grouped.groupby("Category")["repetitions"].sum().reset_index()
    category_counts.columns = [
        "Category",
        "total_repetitions",
    ]

    # Объединяем с группированным DataFrame, чтобы включить общее количество повторений
    grouped = grouped.merge(category_counts, on="Category")

    # Сортируем по категориям (typescript ниже javascript) и по количеству повторений
    category_order = {"javascript": 1, "typescript": 2}
    grouped["category_order"] = (
        grouped["Category"].map(category_order).fillna(3)
    )  # Остальные категории по умолчанию

    grouped.sort_values(
        by=["category_order", "total_repetitions", "repetitions"],
        ascending=[True, False, False],
        inplace=True,
    )

    # Создаем файлы для каждого uid в заданной директории, перезаписываем их
    for _, row in grouped.iterrows():
        question = row["Question"]
        uid = row["uid"]
        repetitions = row["repetitions"]
        category = row["Category"]

        cleaned_question = (
            question.replace("*", ".")
            .replace('"', ".")
            .replace("\\", ".")
            .replace("/", ".")
            .replace("<", ".")
            .replace(">", ".")
            .replace(":", ".")
            .replace("|", ".")
            .replace("?", ".")
        )

        uid_file_path = os.path.join(output_directory, f"{uid}.md")
        with open(
            uid_file_path, "w", encoding="utf-8"
        ) as uid_f:  # Изменено на "w" для перезаписи
            uid_f.write(
                f"---\nquestion: {cleaned_question}\ncount: {repetitions}\nuid: {uid}\ncategory: {category}\n---\n### {question}\n"
            )
            # Получаем уникальные ответы для данного uid
            answers = merged[merged["uid"] == uid][
                "Candidate's Answer"
            ].drop_duplicates()

            # Записываем ответы, разделяя их символами "---"
            if answers.empty:
                uid_f.write("- Нет ответов\n")  # Если ответов нет
            else:
                for answer in answers:
                    uid_f.write(f"---\n- {answer}\n")  # Добавляем ответ в файл


# Основной код
if __name__ == "__main__":
    # Ссылка на вашу Google Sheets в формате CSV
    URL = "https://docs.google.com/spreadsheets/d/1MEoQH8Z53_mjwLF0TcGA11ynjUkuJWDDz2mtaZj9qqA/export?format=csv&id=1MEoQH8Z53_mjwLF0TcGA11ynjUkuJWDDz2mtaZj9qqA&gid=648171770"

    # Получаем данные
    data_frame = data_fetcher(URL)

    # Проверяем первые 5 строк
    print(data_frame.head())  # Выводим первые 5 строк DataFrame

    # Создает директорию и сохраняет вопросы с UID и ответами в Markdown файлы
    save_questions_with_uids(data_frame, "questions_folder")
