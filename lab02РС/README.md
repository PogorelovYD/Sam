# 📘 Лабораторная работа №2

## Вариант 16

### Тема: HTTP-запросы, REST API на Flask и настройка Nginx

---

## 📌 Задание

В рамках лабораторной работы необходимо выполнить три части:

1. Выполнить анализ HTTP-запросов и заголовков безопасности.
2. Реализовать REST API на языке Python с использованием Flask.
3. Настроить Nginx как обратный прокси и включить кеширование GET-запросов на 10 минут.

---

## 🧩 Вариант 16

### Часть 1. HTTP-анализ

Проверить заголовки безопасности сайта:

```text
https://tinkoff.ru
```

Особое внимание уделить заголовку:

```text
Content-Security-Policy
```

---

### Часть 2. REST API

Реализовать API для сущности:

```text
Файловое хранилище
```

Сущность должна содержать поля:

| Поле | Описание |
|---|---|
| id | Уникальный идентификатор файла |
| filename | Имя файла |
| size | Размер файла |
| upload_date | Дата загрузки файла |

---

### Часть 3. Nginx

Настроить кеширование GET-запросов на:

```text
10 минут
```

---

## 🎯 Цель работы

Целью лабораторной работы является изучение методов отправки и анализа HTTP-запросов, настройка веб-сервера Nginx, а также получение практических навыков создания REST API на языке Python.

В ходе работы необходимо:

- изучить работу HTTP-запросов;
- выполнить ручной HTTP-запрос через telnet;
- выполнить автоматические HTTP-запросы через curl;
- проанализировать коды состояния HTTP;
- изучить заголовки безопасности веб-сайта;
- реализовать REST API на Flask;
- настроить Nginx как обратный прокси;
- настроить кеширование GET-запросов.

---

## 🛠 Используемые технологии

| Технология | Назначение |
|---|---|
| Ubuntu Linux | Операционная система |
| Python 3 | Язык программирования |
| Flask | Фреймворк для реализации REST API |
| curl | Утилита для отправки HTTP-запросов |
| telnet | Утилита для ручной отправки HTTP-запросов |
| Nginx | Веб-сервер и обратный прокси |
| venv | Виртуальное окружение Python |
| VS Code | Среда разработки |

---

## 📚 Краткие теоретические сведения

### HTTP

HTTP — это протокол прикладного уровня, предназначенный для передачи данных между клиентом и сервером.  
Клиент отправляет HTTP-запрос, а сервер возвращает HTTP-ответ.

HTTP-ответ содержит:

- код состояния;
- заголовки;
- тело ответа.

Примеры кодов состояния:

| Код | Значение |
|---|---|
| 200 OK | Запрос выполнен успешно |
| 201 Created | Ресурс успешно создан |
| 301 Moved Permanently | Ресурс перемещён на другой адрес |
| 404 Not Found | Ресурс не найден |
| 500 Internal Server Error | Внутренняя ошибка сервера |

---

### REST API

REST API — это архитектурный стиль для создания веб-сервисов.  
Он основан на использовании стандартных HTTP-методов.

Основные методы REST:

| Метод | Назначение |
|---|---|
| GET | Получение данных |
| POST | Создание нового ресурса |
| PUT/PATCH | Обновление ресурса |
| DELETE | Удаление ресурса |

В данной лабораторной работе был реализован REST API для файлового хранилища.

---

### Nginx

Nginx — это веб-сервер, который может использоваться для:

- отдачи статических файлов;
- проксирования запросов;
- балансировки нагрузки;
- кеширования ответов сервера.

В данной работе Nginx используется как обратный прокси для Flask-приложения.

---

### Заголовки безопасности

Заголовки безопасности позволяют повысить защищённость веб-приложений.

Примеры таких заголовков:

| Заголовок | Назначение |
|---|---|
| Content-Security-Policy | Ограничивает источники загрузки контента |
| Strict-Transport-Security | Принудительно использует HTTPS |
| X-Frame-Options | Защищает от clickjacking |
| X-Content-Type-Options | Запрещает браузеру угадывать MIME-тип |

---

# Ход выполнения работы

---

## Часть 1. Анализ HTTP-запросов

### Установка утилит

Для выполнения HTTP-запросов были установлены утилиты `telnet` и `curl`.

```bash
sudo apt update
sudo apt install telnet curl -y
```

---

## Ручной HTTP-запрос через telnet

Было выполнено подключение к сайту `mgpu.ru` по порту `80`.

```bash
telnet mgpu.ru 80
```

После подключения был вручную отправлен HTTP-запрос:

```http
GET / HTTP/1.1
Host: mgpu.ru
```

---

### Результат выполнения telnet-запроса

Сервер вернул ответ:

```text
HTTP/1.1 301 Moved Permanently
Server: ddos-guard
Location: https://mgpu.ru/
Content-Type: text/html; charset=utf-8
```

Код состояния:

```text
301 Moved Permanently
```

означает, что ресурс был перемещён на другой адрес.

В заголовке:

```text
Location: https://mgpu.ru/
```

указано, что сервер перенаправляет пользователя с HTTP-версии сайта на HTTPS-версию.

---

## 📷 Скриншот №1 — telnet-запрос

```bash
telnet mgpu.ru 80
```

На скриншоте должен быть виден ответ:

```text
HTTP/1.1 301 Moved Permanently
```

<img width="1279" height="325" alt="Image" src="https://github.com/user-attachments/assets/dd6b4222-38a9-4b80-91e1-401ef8edca75" />

---

## Анализ заголовков безопасности tinkoff.ru

Для анализа заголовков сайта `tinkoff.ru` была использована команда:

```bash
curl -I https://tinkoff.ru
```

Также был выполнен запрос с переходом по редиректам:

```bash
curl -I -L https://tinkoff.ru
```

---

## Проверка заголовков безопасности

Для поиска заголовков безопасности была использована команда:

```bash
curl -I -L https://tinkoff.ru | grep -i "content-security-policy\|strict-transport-security\|x-frame-options\|x-content-type-options"
```

В результате был найден заголовок:

```text
content-security-policy
```

---

## Анализ Content-Security-Policy

Заголовок `Content-Security-Policy` задаёт политику безопасности контента.  
Он ограничивает источники, с которых браузер может загружать:

- JavaScript-файлы;
- изображения;
- стили;
- шрифты;
- фреймы;
- сетевые соединения.

В результате анализа было установлено, что сайт `tinkoff.ru` использует заголовок `Content-Security-Policy`.

Это повышает безопасность веб-приложения и помогает снизить риск атак типа XSS.

---

## 📷 Скриншот №2 — проверка заголовков tinkoff.ru

```bash
curl -I https://tinkoff.ru
```

<img width="531" height="203" alt="Image" src="https://github.com/user-attachments/assets/7e208b57-9d78-4c13-aa5c-7ee797f23540" />

---

## 📷 Скриншот №3 — Content-Security-Policy

```bash
curl -I -L https://tinkoff.ru | grep -i "content-security-policy\|strict-transport-security\|x-frame-options\|x-content-type-options"
```

На скриншоте должен быть виден заголовок:

```text
content-security-policy
```

<img width="549" height="216" alt="Image" src="https://github.com/user-attachments/assets/2fd41f62-7783-4646-9b6c-d01379ad47ad" />

---

# Часть 2. Реализация REST API на Flask

## Подготовка окружения

Для выполнения работы была создана отдельная папка лабораторной работы и виртуальное окружение Python.

```bash
python3 -m venv venv
source venv/bin/activate
```

После активации окружения был установлен Flask:

```bash
pip install Flask
```

---

## Структура проекта

```text
lab02РС/
│
├── README.md
├── app.py
└── venv/
```

Файл `app.py` содержит реализацию REST API.

---

## Описание API

В рамках лабораторной работы было реализовано REST API для файлового хранилища.

Сущность файла содержит следующие поля:

| Поле | Тип | Описание |
|---|---|---|
| id | int | Уникальный идентификатор |
| filename | string | Имя файла |
| size | int | Размер файла |
| upload_date | string | Дата загрузки |

---

## Реализованные эндпоинты

| Метод | URL | Описание |
|---|---|---|
| GET | /api/files | Получение списка всех файлов |
| GET | /api/files/&lt;id&gt; | Получение файла по идентификатору |
| POST | /api/files | Добавление нового файла |
| DELETE | /api/files/&lt;id&gt; | Удаление файла по идентификатору |

---

## Код файла app.py

```python
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Имитация базы данных файлового хранилища
files = [
    {
        "id": 1,
        "filename": "document.pdf",
        "size": 2048,
        "upload_date": "2026-05-26 10:00:00"
    },
    {
        "id": 2,
        "filename": "image.png",
        "size": 1024,
        "upload_date": "2026-05-26 12:30:00"
    }
]

next_id = 3


# GET /api/files
# Получение списка всех файлов
@app.route("/api/files", methods=["GET"])
def get_files():
    return jsonify(files), 200


# GET /api/files/<id>
# Получение информации о конкретном файле по id
@app.route("/api/files/<int:file_id>", methods=["GET"])
def get_file(file_id):
    for file in files:
        if file["id"] == file_id:
            return jsonify(file), 200

    return jsonify({"error": "File not found"}), 404


# POST /api/files
# Создание новой записи о файле
@app.route("/api/files", methods=["POST"])
def create_file():
    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    if "filename" not in data or "size" not in data:
        return jsonify({"error": "filename and size are required"}), 400

    new_file = {
        "id": next_id,
        "filename": data["filename"],
        "size": data["size"],
        "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    files.append(new_file)
    next_id += 1

    return jsonify(new_file), 201


# DELETE /api/files/<id>
# Удаление файла по id
@app.route("/api/files/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    for file in files:
        if file["id"] == file_id:
            files.remove(file)
            return jsonify({"message": "File deleted successfully"}), 200

    return jsonify({"error": "File not found"}), 404


# Запуск Flask-приложения
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
```

---

## Запуск Flask-приложения

Приложение запускается командой:

```bash
python3 app.py
```

После запуска сервер доступен по адресу:

```text
http://127.0.0.1:5000
```

---

## 📷 Скриншот №4 — код app.py

<img width="1211" height="652" alt="Image" src="https://github.com/user-attachments/assets/7b75a9c0-044e-4a1b-a821-54f0812010bb" />

---

## 📷 Скриншот №5 — запущенный Flask-сервер

На скриншоте должно быть видно:

```text
Running on http://127.0.0.1:5000
```
<img width="343" height="122" alt="Image" src="https://github.com/user-attachments/assets/2b9e8f61-29e2-4e89-bad4-11fc4795152a" />

---

## Тестирование REST API напрямую через Flask

### Получение списка файлов

Команда:

```bash
curl http://127.0.0.1:5000/api/files
```

Пример результата:

```json
[
  {
    "filename": "document.pdf",
    "id": 1,
    "size": 2048,
    "upload_date": "2026-05-26 10:00:00"
  },
  {
    "filename": "image.png",
    "id": 2,
    "size": 1024,
    "upload_date": "2026-05-26 12:30:00"
  }
]
```

---

### Получение файла по id

Команда:

```bash
curl http://127.0.0.1:5000/api/files/1
```

---

### Создание нового файла

Команда:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"filename": "test.txt", "size": 512}' http://127.0.0.1:5000/api/files
```

Пример результата:

```json
{
  "filename": "test.txt",
  "id": 3,
  "size": 512,
  "upload_date": "2026-05-26 13:30:00"
}
```

---

### Удаление файла

Команда:

```bash
curl -X DELETE http://127.0.0.1:5000/api/files/1
```

Пример результата:

```json
{
  "message": "File deleted successfully"
}
```

---

## 📷 Скриншот №6 — GET-запрос к API

```bash
curl http://127.0.0.1:5000/api/files
```

<img width="765" height="166" alt="Image" src="https://github.com/user-attachments/assets/8b74ca41-358a-4f91-9b62-d934ab88cd3a" />

---

## 📷 Скриншот №7 — POST-запрос к API

```bash
curl -X POST -H "Content-Type: application/json" -d '{"filename": "test.txt", "size": 512}' http://127.0.0.1:5000/api/files
```

<img width="1205" height="166" alt="Image" src="https://github.com/user-attachments/assets/6e833b2b-7deb-466a-8364-412b7c7be6ec" />

---

# Часть 3. Настройка Nginx

## Установка Nginx

Для установки Nginx была использована команда:

```bash
sudo apt install nginx -y
```

После установки сервер был запущен:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

Проверка работы Nginx выполнялась командой:

```bash
curl http://localhost
```

---

## Настройка Nginx как обратного прокси

Для настройки Nginx был изменён файл:

```text
/etc/nginx/sites-available/default
```

Nginx был настроен таким образом, чтобы запросы по адресу:

```text
http://localhost/api/files
```

перенаправлялись на Flask-приложение:

```text
http://127.0.0.1:5000/api/files
```

---

## Конфигурация Nginx

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        expires 10m;
        add_header Cache-Control "public, max-age=600";
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## Объяснение конфигурации Nginx

| Директива | Назначение |
|---|---|
| listen 80 | Nginx принимает HTTP-запросы на порту 80 |
| location /api/ | Обрабатывает запросы к API |
| proxy_pass | Перенаправляет запросы на Flask-сервер |
| proxy_set_header Host | Передаёт исходный заголовок Host |
| proxy_set_header X-Real-IP | Передаёт IP-адрес клиента |
| expires 10m | Устанавливает время кеширования 10 минут |
| Cache-Control max-age=600 | Указывает кеширование на 600 секунд |

---

## Проверка конфигурации Nginx

После изменения конфигурации была выполнена проверка:

```bash
sudo nginx -t
```

Результат успешной проверки:

```text
syntax is ok
test is successful
```

После этого Nginx был перезапущен:

```bash
sudo systemctl restart nginx
```

---

## 📷 Скриншот №8 — конфигурация Nginx

<img width="968" height="533" alt="Image" src="https://github.com/user-attachments/assets/23213eb8-f1a7-478f-b2ff-18790920794d" />

---

## Тестирование API через Nginx

Для проверки работы API через Nginx была выполнена команда:

```bash
curl -i http://localhost/api/files
```

В результате был получен ответ от Flask-приложения через Nginx.

В ответе присутствуют заголовки кеширования:

```text
Cache-Control: public, max-age=600
Expires: ...
```

Это подтверждает, что кеширование GET-запросов настроено на 10 минут.

---

## 📷 Скриншот №10 — GET через Nginx с кешированием

```bash
curl -i http://localhost/api/files
```

На скриншоте должны быть видны заголовки:

```text
Cache-Control: public, max-age=600
Expires
```

<img width="591" height="563" alt="Image" src="https://github.com/user-attachments/assets/34436d2c-d990-4c3d-aad0-0b5a3c9bbc55" />

---

## Проверка POST-запроса через Nginx

Команда:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"filename": "nginx_file.txt", "size": 777}' http://localhost/api/files
```

POST-запрос успешно создаёт новую запись о файле через Nginx.

---

## Проверка GET одного файла через Nginx

Команда:

```bash
curl -i http://localhost/api/files/2
```

Запрос возвращает информацию о файле с указанным идентификатором.

---

# 📊 Результаты выполнения

В ходе лабораторной работы были получены следующие результаты:

| Этап | Результат |
|---|---|
| Telnet-запрос | Получен ответ 301 Moved Permanently |
| Анализ tinkoff.ru | Найден заголовок Content-Security-Policy |
| REST API | Реализован сервис файлового хранилища |
| Flask | Сервер успешно запущен на порту 5000 |
| Nginx | Настроен как обратный прокси |
| Кеширование | GET-запросы кешируются на 10 минут |
| Тестирование | Все основные запросы успешно выполнены |

---

# ✅ Проверка соответствия заданию

| Требование | Выполнение |
|---|---|
| Выполнить HTTP-анализ | Выполнено |
| Проверить заголовки безопасности tinkoff.ru | Выполнено |
| Найти Content-Security-Policy | Выполнено |
| Реализовать API файлового хранилища | Выполнено |
| Использовать поля id, filename, size, upload_date | Выполнено |
| Реализовать GET /api/files | Выполнено |
| Реализовать GET /api/files/&lt;id&gt; | Выполнено |
| Реализовать POST /api/files | Выполнено |
| Реализовать DELETE /api/files/&lt;id&gt; | Выполнено |
| Настроить Nginx как обратный прокси | Выполнено |
| Настроить кеширование GET на 10 минут | Выполнено |

---

# 📌 Вывод

В ходе выполнения лабораторной работы были изучены основные принципы работы HTTP-запросов, REST API и веб-сервера Nginx.

С помощью `telnet` был вручную отправлен HTTP-запрос к сайту `mgpu.ru`, в результате чего был получен ответ `301 Moved Permanently`, указывающий на перенаправление с HTTP на HTTPS.

С помощью `curl` были проанализированы HTTP-заголовки сайта `tinkoff.ru`. В результате был найден заголовок `Content-Security-Policy`, который используется для повышения безопасности веб-приложений.

Также был реализован REST API для файлового хранилища на Flask. API поддерживает получение списка файлов, получение файла по идентификатору, создание новой записи о файле и удаление файла.

Дополнительно был настроен Nginx как обратный прокси для Flask-приложения. Для GET-запросов было настроено кеширование на 10 минут с помощью заголовка `Cache-Control: public, max-age=600`.

Лабораторная работа выполнена успешно.
