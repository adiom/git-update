from fastapi import FastAPI, HTTPException
from git import Repo
import os
import uuid
from datetime import datetime

app = FastAPI()

# Git конфигурации
GIT_REPO_PATH = "/Users/adiom/Canfly/b"
POSTS_PATH = os.path.join(GIT_REPO_PATH, "content/posts/adiom")

# Инициализация Git репозитория
try:
    repo = Repo(GIT_REPO_PATH)
    if repo.bare:
        raise Exception("Не удалось инициализировать репозиторий")
except Exception as e:
    raise Exception(f"Ошибка инициализации Git репозитория: {e}")


@app.post("/git_commit_push/")
def git_commit_push(author: str, title: str, description: str, text: str):
    """
    Создает новый Markdown-файл, добавляет его в репозиторий, делает commit и push
    """
    try:
        # Генерируем случайное имя для файла
        random_filename = f"{uuid.uuid4().hex}.md"
        file_path = os.path.join(POSTS_PATH, random_filename)

        # Убедимся, что директория существует
        os.makedirs(POSTS_PATH, exist_ok=True)

        # Форматируем данные в структуру Markdown
        today = datetime.now().strftime("%Y-%m-%d")
        markdown_content = f"""---
title: "{title}"
description: "{description}"
author: "{author}"
date: "{today}"
---

{text.strip()}
"""

        # Сохраняем данные в файл
        with open(file_path, "w", encoding="utf-8") as f:  # Убедитесь, что используете кодировку utf-8
            f.write(markdown_content)

        # Добавляем файл в Git
        repo.index.add([file_path])

        # Выполняем commit
        commit_message = f"Добавлен файл {random_filename} с заголовком '{title}'"
        repo.index.commit(commit_message)

        # Делаем push
        origin = repo.remote(name="origin")
        origin.push()

        return {
            "message": "Файл успешно добавлен, закоммичен и отправлен",
            "filename": random_filename,
            "path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка выполнения Git операций: {e}")
