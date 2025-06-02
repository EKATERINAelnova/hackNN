## Установка ollama 
```curl -fsSL https://ollama.com/install.sh | sh```

## Установка llama3:8b-instruct-q4_0
```ollama pull llama3:8b-instruct-q4_0```

## Запуск llama3 как сервер для доступо по api, запускает сервер на localhost:11434
```ollama serve```

## Установка зависимости для создания запроса к api llama3:8b-instruct-q4_0
```pip install requests```

## Описание модулей
* app.py - файл с api на flask
* main.py - основной файл, запуск пайплайна
* ollama.py - запус сервера Ollama
* survey.py - проведение опроса, необходимо подстроить под web
* qualifier.py - классификация ответа на положительны/отрицательный
* summarization.py - суммарищация полученных ответов в краткий отзыв
* rentability.py - классификация отзыва на рентабельный/нерентабельный
* survey.html - пример использования api