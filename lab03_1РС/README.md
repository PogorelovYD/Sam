# 📘 Лабораторная работа №3.1

## Вариант 16

### Тема: Синхронное взаимодействие через gRPC и асинхронное взаимодействие через RabbitMQ

---

## 📌 Постановка задачи

В рамках лабораторной работы необходимо изучить и реализовать два подхода к взаимодействию между сервисами:

1. **Синхронное прямое взаимодействие** с использованием gRPC.
2. **Асинхронное взаимодействие** через брокер сообщений RabbitMQ.

Для реализации инфраструктурной части используется Docker и Docker Compose.  
Producer отправляет сообщения в очередь RabbitMQ, Consumer получает сообщения из очереди и вызывает соответствующий метод gRPC-сервиса.

---

## 🧩 Вариант 16

Необходимо реализовать три задания:

| № | Задание | Описание |
|---|---|---|
| 1 | Запись в CSV-файл | Producer отправляет строку с данными через запятую. gRPC-сервис имитирует запись этой строки в CSV-файл и возвращает `"Записано"` |
| 2 | Проверка домена | Producer отправляет email. gRPC-сервис извлекает домен и проверяет наличие MX-записей, возвращая `True` или `False` |
| 3 | Поиск самого длинного слова | Producer отправляет текст. gRPC-сервис находит самое длинное слово и возвращает его |

---

## 🎯 Цель работы

Целью лабораторной работы является изучение синхронного и асинхронного взаимодействия между сервисами.

В ходе выполнения работы необходимо:

- изучить прямое взаимодействие сервисов через gRPC;
- реализовать gRPC-сервис с несколькими методами;
- изучить асинхронное взаимодействие через брокер сообщений RabbitMQ;
- запустить RabbitMQ с помощью Docker;
- реализовать Producer для отправки сообщений в очередь;
- реализовать Consumer для чтения сообщений из очереди;
- связать RabbitMQ и gRPC в одной системе;
- проверить выполнение всех заданий варианта.

---

## 🛠 Стек технологий

| Технология | Назначение |
|---|---|
| Ubuntu Linux | Операционная система |
| Python 3 | Язык программирования |
| gRPC | Синхронное RPC-взаимодействие |
| Protocol Buffers | Описание интерфейса gRPC-сервиса |
| RabbitMQ | Брокер сообщений |
| Docker | Запуск инфраструктурных компонентов |
| Docker Compose | Описание и запуск RabbitMQ |
| pika | Python-клиент для RabbitMQ |
| dnspython | Проверка MX-записей домена |
| VS Code | Среда разработки |

---

## 📚 Теоретические сведения

### gRPC

gRPC — это фреймворк для реализации удалённого вызова процедур.  
Он позволяет клиенту вызывать методы сервера так, как будто это обычные локальные функции.

В gRPC используется файл `.proto`, в котором описываются:

- сервисы;
- методы;
- входные сообщения;
- выходные сообщения.

На основе `.proto` файла генерируется Python-код для клиента и сервера.

---

### RabbitMQ

RabbitMQ — это брокер сообщений, который используется для асинхронного взаимодействия между сервисами.

При использовании RabbitMQ:

- Producer отправляет сообщение в очередь;
- RabbitMQ хранит сообщение;
- Consumer получает сообщение из очереди;
- Consumer обрабатывает сообщение.

Такой подход позволяет разделить отправителя и получателя сообщений.

---

### Docker

Docker используется для запуска RabbitMQ в контейнере.  
Это позволяет быстро развернуть брокер сообщений без ручной установки и настройки RabbitMQ в системе.

---

# 🏗 Архитектура решения

## Часть 1. Синхронное взаимодействие через gRPC

В первой части лабораторной работы клиент напрямую вызывает методы gRPC-сервера.

```text
+----------------+        gRPC        +----------------+
|  grpc_client   |  ----------------> |  grpc_server   |
| grpc_client.py |                    | grpc_server.py |
+----------------+                    +----------------+
```

Клиент отправляет запрос, сервер выполняет обработку и сразу возвращает результат.

---

## Часть 2. Асинхронное взаимодействие через RabbitMQ + gRPC

Во второй части используется брокер сообщений RabbitMQ.

```text
+-------------+       message        +-------------+       message       +-------------+
|  Producer   |  ----------------->  |  RabbitMQ   |  ----------------> |  Consumer   |
| producer.py |                      |   Queue     |                    | consumer.py |
+-------------+                      +-------------+                    +-------------+
                                                                            |
                                                                            | gRPC
                                                                            v
                                                                     +-------------+
                                                                     | gRPC Server |
                                                                     |grpc_server.py|
                                                                     +-------------+
```

Producer отправляет сообщение в очередь.  
Consumer получает сообщение, определяет тип задания и вызывает соответствующий метод gRPC-сервиса.

---

# 📁 Структура проекта

```text
lab03_1/
│
├── README.md
├── venv/
│
├── grpc_sync/
│   ├── task_service.proto
│   ├── grpc_server.py
│   ├── grpc_client.py
│   ├── task_service_pb2.py
│   ├── task_service_pb2_grpc.py
│   └── data.csv
│
└── rabbitmq_async/
    ├── docker-compose.yml
    ├── producer.py
    └── consumer.py
```

---

## Описание файлов

| Файл | Описание |
|---|---|
| `task_service.proto` | Контракт gRPC-сервиса |
| `grpc_server.py` | Реализация логики gRPC-сервера |
| `grpc_client.py` | Тестовый клиент для прямого вызова gRPC |
| `task_service_pb2.py` | Сгенерированные классы сообщений |
| `task_service_pb2_grpc.py` | Сгенерированные классы сервиса и клиента |
| `docker-compose.yml` | Конфигурация RabbitMQ |
| `producer.py` | Отправляет сообщения в очередь RabbitMQ |
| `consumer.py` | Получает сообщения из RabbitMQ и вызывает gRPC |
| `data.csv` | Файл, в который записываются CSV-строки |

---

# Часть 1. Реализация gRPC

## Описание gRPC-сервиса

Для выполнения заданий был создан gRPC-сервис `TaskService`.

Сервис содержит три метода:

| Метод | Назначение |
|---|---|
| `WriteCsv` | Записывает строку в CSV-файл |
| `CheckDomain` | Проверяет наличие MX-записей у домена email |
| `LongestWord` | Находит самое длинное слово в тексте |

---

## Код файла `task_service.proto`

```proto
syntax = "proto3";

package taskservice;

service TaskService {
    rpc WriteCsv (CsvRequest) returns (CsvResponse);
    rpc CheckDomain (EmailRequest) returns (DomainResponse);
    rpc LongestWord (TextRequest) returns (WordResponse);
}

message CsvRequest {
    string row = 1;
}

message CsvResponse {
    string message = 1;
}

message EmailRequest {
    string email = 1;
}

message DomainResponse {
    bool has_mx = 1;
    string domain = 2;
}

message TextRequest {
    string text = 1;
}

message WordResponse {
    string word = 1;
}
```

---

## 📷 Скриншот №1 — файл `task_service.proto`

<img width="1268" height="923" alt="Image" src="https://github.com/user-attachments/assets/36456a82-fa69-4120-9754-93bacf345d5c" />

---

## Генерация gRPC-кода

После создания `.proto` файла была выполнена команда:

```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. task_service.proto
```

В результате были созданы файлы:

```text
task_service_pb2.py
task_service_pb2_grpc.py
```

Эти файлы используются для работы gRPC-клиента и gRPC-сервера.

---

## Реализация gRPC-сервера

Сервер реализован в файле:

```text
grpc_server.py
```

Сервер запускается на порту:

```text
50051
```

и ожидает подключения клиентов.

---

## Код файла `grpc_server.py`

```python
from concurrent import futures
import csv
import re

import grpc
import dns.resolver

import task_service_pb2
import task_service_pb2_grpc


class TaskServiceServicer(task_service_pb2_grpc.TaskServiceServicer):
    def WriteCsv(self, request, context):
        row = request.row

        with open("data.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row.split(","))

        print(f"[CSV] Записана строка: {row}")

        return task_service_pb2.CsvResponse(message="Записано")

    def CheckDomain(self, request, context):
        email = request.email

        if "@" not in email:
            print(f"[DOMAIN] Некорректный email: {email}")
            return task_service_pb2.DomainResponse(
                has_mx=False,
                domain=""
            )

        domain = email.split("@")[-1]

        try:
            dns.resolver.resolve(domain, "MX")
            has_mx = True
        except Exception:
            has_mx = False

        print(f"[DOMAIN] Email: {email}, domain: {domain}, MX: {has_mx}")

        return task_service_pb2.DomainResponse(
            has_mx=has_mx,
            domain=domain
        )

    def LongestWord(self, request, context):
        text = request.text

        words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", text)

        if not words:
            longest = ""
        else:
            longest = max(words, key=len)

        print(f"[TEXT] Текст: {text}")
        print(f"[TEXT] Самое длинное слово: {longest}")

        return task_service_pb2.WordResponse(word=longest)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    task_service_pb2_grpc.add_TaskServiceServicer_to_server(
        TaskServiceServicer(),
        server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("gRPC server started on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
```

---

## 📷 Скриншот №2 — код `grpc_server.py`

<img width="1241" height="927" alt="Image" src="https://github.com/user-attachments/assets/63b75b9c-f38c-4036-9482-efc839f395b2" />

---

## Реализация gRPC-клиента

Для проверки прямого синхронного взаимодействия был создан файл:

```text
grpc_client.py
```

Клиент напрямую вызывает методы gRPC-сервера:

- `WriteCsv`;
- `CheckDomain`;
- `LongestWord`.

---

## Код файла `grpc_client.py`

```python
import grpc

import task_service_pb2
import task_service_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = task_service_pb2_grpc.TaskServiceStub(channel)

    print("=== Проверка записи в CSV ===")
    csv_response = stub.WriteCsv(
        task_service_pb2.CsvRequest(row="1,Ivan,ivan@example.com")
    )
    print("Ответ сервера:", csv_response.message)

    print("\n=== Проверка домена email ===")
    domain_response = stub.CheckDomain(
        task_service_pb2.EmailRequest(email="test@gmail.com")
    )
    print("Домен:", domain_response.domain)
    print("MX записи есть:", domain_response.has_mx)

    print("\n=== Поиск самого длинного слова ===")
    word_response = stub.LongestWord(
        task_service_pb2.TextRequest(text="RabbitMQ и gRPC используются для взаимодействия сервисов")
    )
    print("Самое длинное слово:", word_response.word)


if __name__ == "__main__":
    run()
```

---

## 📷 Скриншот №3 — код `grpc_client.py`

<img width="1385" height="833" alt="Image" src="https://github.com/user-attachments/assets/e44423e2-5826-46cc-acda-ed4cb5bf9320" />

---

## Запуск gRPC-сервера

Команда запуска:

```bash
cd grpc_sync
source ../venv/bin/activate
python3 grpc_server.py
```

После запуска сервер выводит сообщение:

```text
gRPC server started on port 50051
```

---

## 📷 Скриншот №4 — запущенный gRPC-сервер

<img width="611" height="177" alt="Image" src="https://github.com/user-attachments/assets/3cdf44fe-aa76-48e0-8b0b-04d6e2c0847d" />

---

## Проверка gRPC-клиента

Команда запуска клиента:

```bash
cd grpc_sync
source ../venv/bin/activate
python3 grpc_client.py
```

Пример результата:

```text
=== Проверка записи в CSV ===
Ответ сервера: Записано

=== Проверка домена email ===
Домен: gmail.com
MX записи есть: True

=== Поиск самого длинного слова ===
Самое длинное слово: взаимодействия
```

---

## 📷 Скриншот №5 — результат работы gRPC-клиента

<img width="622" height="295" alt="Image" src="https://github.com/user-attachments/assets/64543768-de9f-447c-b116-6bae7cb09a17" />

---

# Часть 2. RabbitMQ + gRPC

## Описание асинхронной части

Во второй части лабораторной работы Producer отправляет сообщения в очередь RabbitMQ.  
Consumer читает сообщения из очереди и вызывает нужный метод gRPC-сервера.

Для выбора задания используются префиксы сообщений:

| Префикс | Назначение | Пример |
|---|---|---|
| `csv:` | Запись строки в CSV | `csv:1,Ivan,ivan@example.com` |
| `email:` | Проверка домена email | `email:test@gmail.com` |
| `text:` | Поиск самого длинного слова | `text:RabbitMQ and gRPC are useful technologies` |

---

## Код `docker-compose.yml`

```yaml
version: "3.8"

services:
  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq_lab03
    ports:
      - "5672:5672"
      - "15672:15672"
```

RabbitMQ запускается в Docker-контейнере.  
Порт `5672` используется для подключения приложений, а порт `15672` — для веб-интерфейса RabbitMQ Management.

---

## 📷 Скриншот №6 — файл `docker-compose.yml`

<img width="473" height="286" alt="Image" src="https://github.com/user-attachments/assets/3e584e27-256d-4d4e-87ff-09ab1acf83fe" />

---

## Запуск RabbitMQ

Для запуска RabbitMQ была выполнена команда:

```bash
cd rabbitmq_async
docker compose up -d
```

Проверка контейнера:

```bash
docker ps
```

В списке контейнеров отображается контейнер:

```text
rabbitmq_lab03
```

---

## 📷 Скриншот №7 — запущенный RabbitMQ-контейнер

<img width="1055" height="137" alt="Image" src="https://github.com/user-attachments/assets/a0659c83-39c6-4af8-a0fd-b6c4dcd7e7b4" />

---

## Producer

Producer реализован в файле:

```text
producer.py
```

Он принимает сообщение из аргументов командной строки и отправляет его в очередь RabbitMQ.

---

## Код файла `producer.py`

```python
import sys
import pika


QUEUE_NAME = "tasks_queue"


def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("python3 producer.py csv:1,Ivan,ivan@example.com")
        print("python3 producer.py email:test@gmail.com")
        print("python3 producer.py text:\"RabbitMQ and gRPC are useful technologies\"")
        return

    message = sys.argv[1]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message.encode("utf-8")
    )

    print(f"[Producer] Отправлено сообщение: {message}")

    connection.close()


if __name__ == "__main__":
    main()
```

---

## 📷 Скриншот №8 — код `producer.py`

<img width="884" height="812" alt="Image" src="https://github.com/user-attachments/assets/d19bde7e-54b3-4362-b576-b68375e8a4b7" />

---

## Consumer

Consumer реализован в файле:

```text
consumer.py
```

Он получает сообщения из RabbitMQ, анализирует префикс сообщения и вызывает нужный метод gRPC-сервиса.

---

## Код файла `consumer.py`

```python
import os
import sys

import grpc
import pika

sys.path.append(os.path.abspath("../grpc_sync"))

import task_service_pb2
import task_service_pb2_grpc


QUEUE_NAME = "tasks_queue"


def process_message(message, stub):
    if message.startswith("csv:"):
        row = message.replace("csv:", "", 1)

        response = stub.WriteCsv(
            task_service_pb2.CsvRequest(row=row)
        )

        print(f"[Consumer] CSV result: {response.message}")

    elif message.startswith("email:"):
        email = message.replace("email:", "", 1)

        response = stub.CheckDomain(
            task_service_pb2.EmailRequest(email=email)
        )

        print(f"[Consumer] Email: {email}")
        print(f"[Consumer] Domain: {response.domain}")
        print(f"[Consumer] Has MX: {response.has_mx}")

    elif message.startswith("text:"):
        text = message.replace("text:", "", 1)

        response = stub.LongestWord(
            task_service_pb2.TextRequest(text=text)
        )

        print(f"[Consumer] Text: {text}")
        print(f"[Consumer] Longest word: {response.word}")

    else:
        print(f"[Consumer] Unknown task type: {message}")


def callback(ch, method, properties, body):
    message = body.decode("utf-8")

    print(f"\n[Consumer] Получено сообщение: {message}")

    grpc_channel = grpc.insecure_channel("localhost:50051")
    stub = task_service_pb2_grpc.TaskServiceStub(grpc_channel)

    process_message(message, stub)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )

    rabbit_channel = connection.channel()
    rabbit_channel.queue_declare(queue=QUEUE_NAME)

    print("[Consumer] Ожидание сообщений...")

    rabbit_channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    rabbit_channel.start_consuming()


if __name__ == "__main__":
    main()
```

---

## 📷 Скриншот №9 — код `consumer.py`

<img width="664" height="832" alt="Image" src="https://github.com/user-attachments/assets/999d5634-09ec-491d-a77e-7538a18db890" />

---

# 🚀 Порядок запуска системы

Для запуска всей системы используются четыре терминала.

---

## Терминал 1 — запуск gRPC-сервера

```bash
cd ~/Sam/lab03_1/grpc_sync
source ../venv/bin/activate
python3 grpc_server.py
```

---

## Терминал 2 — запуск RabbitMQ

```bash
cd ~/Sam/lab03_1/rabbitmq_async
docker compose up -d
docker ps
```

---

## Терминал 3 — запуск Consumer

```bash
cd ~/Sam/lab03_1/rabbitmq_async
source ../venv/bin/activate
python3 consumer.py
```

---

## Терминал 4 — запуск Producer

### Задание 1. Запись в CSV

```bash
cd ~/Sam/lab03_1/rabbitmq_async
source ../venv/bin/activate
python3 producer.py csv:1,Ivan,ivan@example.com
```

Ожидаемый результат в Consumer:

```text
[Consumer] Получено сообщение: csv:1,Ivan,ivan@example.com
[Consumer] CSV result: Записано
```

---

### Задание 2. Проверка домена email

```bash
python3 producer.py email:test@gmail.com
```

Ожидаемый результат в Consumer:

```text
[Consumer] Получено сообщение: email:test@gmail.com
[Consumer] Email: test@gmail.com
[Consumer] Domain: gmail.com
[Consumer] Has MX: True
```

---

### Задание 3. Поиск самого длинного слова

```bash
python3 producer.py text:"RabbitMQ and gRPC are useful technologies"
```

Ожидаемый результат в Consumer:

```text
[Consumer] Получено сообщение: text:RabbitMQ and gRPC are useful technologies
[Consumer] Text: RabbitMQ and gRPC are useful technologies
[Consumer] Longest word: technologies
```

---

## 📷 Скриншот №10 — запущенный Consumer

<img width="629" height="87" alt="Image" src="https://github.com/user-attachments/assets/b77dc5a9-875a-46ae-95ac-95d371b8bb48" />

---

## 📷 Скриншот №11 — отправка сообщений Producer

<img width="825" height="61" alt="Image" src="https://github.com/user-attachments/assets/f75b5ba0-bbb0-4195-b328-29fb8f310f9c" />

---

## 📷 Скриншот №12 — результаты Consumer


<img width="682" height="402" alt="Image" src="https://github.com/user-attachments/assets/c89e52b9-6c35-45c3-bb9e-5840d05e9468" />

---

## Проверка CSV-файла

После выполнения задания с префиксом `csv:` в папке `grpc_sync` появляется файл:

```text
data.csv
```

Проверка содержимого файла:

```bash
cd ~/Sam/lab03_1/grpc_sync
cat data.csv
```

Пример результата:

```text
1,Ivan,ivan@example.com
```

---

## 📷 Скриншот №13 — файл `data.csv`

<img width="672" height="99" alt="Image" src="https://github.com/user-attachments/assets/3c817711-4304-4ee5-a96d-fd19ea28b5c2" />

---

# 📊 Результаты выполнения

В результате выполнения лабораторной работы:

| Этап | Результат |
|---|---|
| gRPC-сервер | Успешно запущен |
| gRPC-клиент | Успешно вызывает методы сервера |
| RabbitMQ | Запущен в Docker-контейнере |
| Producer | Отправляет сообщения в очередь |
| Consumer | Получает сообщения из очереди |
| CSV-запись | Строка записывается в `data.csv` |
| Проверка email | Домен извлекается, MX-записи проверяются |
| Поиск слова | Самое длинное слово находится |

---

# ✅ Проверка соответствия заданию

| Требование | Выполнение |
|---|---|
| Реализовать gRPC-сервис | Выполнено |
| Реализовать прямой gRPC-клиент | Выполнено |
| Запустить RabbitMQ через Docker | Выполнено |
| Реализовать Producer | Выполнено |
| Реализовать Consumer | Выполнено |
| Producer отправляет CSV-строку | Выполнено |
| gRPC-сервис записывает строку в CSV | Выполнено |
| Producer отправляет email | Выполнено |
| gRPC-сервис проверяет MX-записи домена | Выполнено |
| Producer отправляет текст | Выполнено |
| gRPC-сервис возвращает самое длинное слово | Выполнено |
| Подготовлен отчёт README.md | Выполнено |

---

# 📌 Вывод

В ходе выполнения лабораторной работы были реализованы два подхода к взаимодействию между сервисами.

В первой части было реализовано синхронное взаимодействие с использованием gRPC. Клиент напрямую вызывал методы сервера и получал результат выполнения операций.

Во второй части было реализовано асинхронное взаимодействие с использованием RabbitMQ. Producer отправлял сообщения в очередь, Consumer получал их, определял тип задачи и вызывал соответствующий метод gRPC-сервиса.

Были выполнены все задания варианта 16:

- строка с данными записывается в CSV-файл;
- email анализируется, из него извлекается домен и проверяются MX-записи;
- из текста определяется самое длинное слово.

Лабораторная работа выполнена успешно.
