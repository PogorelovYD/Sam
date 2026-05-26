# 📘 Лабораторная работа №1

## Вариант 16

### Тема: Реализация RPC-сервиса с использованием gRPC

### Сервис: GameLobby

### Тип RPC: Bidirectional Streaming RPC

---

## 📌 Задание

Необходимо реализовать gRPC-сервис **GameLobby**.

Сервис должен содержать метод:

```proto
rpc Matchmaking(stream PlayerInfo) returns (stream MatchResult);
```

Метод `Matchmaking` предназначен для поиска игроков и формирования игровой сессии.

Данный метод использует **Bidirectional Streaming RPC**, то есть двусторонний потоковый обмен данными.  
Клиент отправляет на сервер поток сообщений с информацией об игроках, а сервер в ответ отправляет поток сообщений с результатами подбора игроков.

---

## 🎯 Цель работы

Целью лабораторной работы является освоение принципов удалённого вызова процедур и получение практических навыков работы с gRPC.

В ходе выполнения работы необходимо:

- изучить основные принципы RPC;
- познакомиться с фреймворком gRPC;
- изучить язык описания интерфейсов Protocol Buffers;
- описать сервис и сообщения в `.proto` файле;
- сгенерировать Python-код на основе `.proto` файла;
- реализовать серверную часть приложения;
- реализовать клиентскую часть приложения;
- проверить работу двустороннего потокового RPC-вызова.

---

## 🛠 Используемые технологии

| Технология | Назначение |
|---|---|
| Python 3 | Язык программирования |
| gRPC | Фреймворк для реализации RPC |
| Protocol Buffers | Описание структуры сообщений и сервисов |
| grpcio | Основная библиотека gRPC для Python |
| grpcio-tools | Инструменты для генерации gRPC-кода |
| venv | Виртуальное окружение Python |
| VS Code | Среда разработки |
| Ubuntu Linux | Операционная система |

---

## 📚 Теоретическая часть

**RPC** — это технология удалённого вызова процедур. Она позволяет программе вызывать метод, который выполняется в другом процессе или на другом компьютере, как будто это обычный локальный вызов.

**gRPC** — это современный фреймворк для реализации RPC. Он использует HTTP/2 и Protocol Buffers, поддерживает разные языки программирования и позволяет реализовывать разные типы взаимодействия между клиентом и сервером.

**Protocol Buffers** — это механизм сериализации данных. С помощью `.proto` файла описываются сообщения и сервисы, а затем на основе этого файла автоматически генерируется код.

---

## 🔄 Типы RPC в gRPC

| Тип RPC | Описание |
|---|---|
| Unary RPC | Клиент отправляет один запрос и получает один ответ |
| Server Streaming RPC | Клиент отправляет один запрос, сервер возвращает поток ответов |
| Client Streaming RPC | Клиент отправляет поток запросов, сервер возвращает один ответ |
| Bidirectional Streaming RPC | Клиент и сервер обмениваются потоками сообщений |

В данной лабораторной работе используется **Bidirectional Streaming RPC**.

---

## 🏗 Архитектура решения

В работе реализована клиент-серверная архитектура.

```text
+-------------+        gRPC         +-------------+
|   Клиент    |  <--------------->  |   Сервер    |
|  client.py  |                     |  server.py  |
+-------------+                     +-------------+
                                           |
                                           |
                                    +--------------+
                                    | Matchmaking  |
                                    |    Queue     |
                                    +--------------+
```

Клиент отправляет поток игроков на сервер.  
Сервер принимает игроков, сохраняет их во временную очередь и формирует игровые пары.  
После формирования пары сервер отправляет клиенту сообщение с результатом матчмейкинга.

---

## 📁 Структура проекта

```text
lab01РС/
│
├── README.md
├── game.proto
├── server.py
├── client.py
├── game_pb2.py
└── game_pb2_grpc.py
```

Описание файлов:

| Файл | Назначение |
|---|---|
| README.md | Отчёт по лабораторной работе |
| game.proto | Описание gRPC-сервиса и сообщений |
| server.py | Реализация серверной части |
| client.py | Реализация клиентской части |
| game_pb2.py | Сгенерированные классы сообщений |
| game_pb2_grpc.py | Сгенерированные классы сервиса и клиента |

---

## 🧩 Описание Proto-файла

Описание сервиса выполнено в файле:

```text
game.proto
```

В файле описан сервис **GameLobby** и метод **Matchmaking**.

Метод принимает поток сообщений `PlayerInfo` и возвращает поток сообщений `MatchResult`.

---

## 📄 Код файла `game.proto`

```proto
syntax = "proto3";

package game;

service GameLobby {
    rpc Matchmaking(stream PlayerInfo) returns (stream MatchResult);
}

message PlayerInfo {
    string nickname = 1;
    int32 level = 2;
}

message MatchResult {
    string message = 1;
}
```

## ⚙️ Генерация gRPC-кода

После создания файла `game.proto` была выполнена команда генерации Python-кода:

```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. game.proto
```

В результате выполнения команды были автоматически созданы файлы:

```text
game_pb2.py
game_pb2_grpc.py
```

Файл `game_pb2.py` содержит классы сообщений, описанных в `.proto` файле.

Файл `game_pb2_grpc.py` содержит классы для реализации сервера и клиента gRPC.

---

## 📷 Скриншот №1 — сгенерированные файлы

- `game_pb2.py`
- `game_pb2_grpc.py`

<img width="303" height="297" alt="Image" src="https://github.com/user-attachments/assets/9e8290ea-00f1-4761-a79b-b8f4a137e736" />

---

## 🖥 Реализация сервера

Серверная часть реализована в файле:

```text
server.py
```

Сервер создаёт gRPC-сервер, регистрирует сервис `GameLobbyServicer` и запускается на порту `50051`.

В методе `Matchmaking` сервер принимает поток сообщений от клиента.  
Каждое сообщение содержит информацию об игроке.

Игроки добавляются в список `players`.  
Когда в списке появляется два игрока, сервер формирует игровую пару и отправляет клиенту результат.

Для отправки ответа используется оператор `yield`, так как метод возвращает поток сообщений.

---

## 📄 Код файла `server.py`

```python
from concurrent import futures
import grpc

import game_pb2
import game_pb2_grpc


class GameLobbyServicer(game_pb2_grpc.GameLobbyServicer):

    def Matchmaking(self, request_iterator, context):
        players = []

        for player in request_iterator:
            print(f"Получен игрок: {player.nickname}, level {player.level}")

            players.append(player)

            if len(players) >= 2:
                p1 = players.pop(0)
                p2 = players.pop(0)

                yield game_pb2.MatchResult(
                    message=f"Match found: {p1.nickname} vs {p2.nickname}"
                )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    game_pb2_grpc.add_GameLobbyServicer_to_server(
        GameLobbyServicer(),
        server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Server started on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
```

---

## 📷 Скриншот №2 — код сервера

скриншот открытого файла `server.py`.

<img width="1268" height="885" alt="Image" src="https://github.com/user-attachments/assets/64ce13df-2e5b-4095-a724-a98d11c584eb" />

---

## 📷 Скриншот №4 — запущенный сервер

```text
Server started on port 50051
```

Также могут быть видны сообщения о полученных игроках:

```text
Получен игрок: PlayerOne, level 10
Получен игрок: PlayerTwo, level 20
```
<img width="692" height="240" alt="Image" src="https://github.com/user-attachments/assets/b9cc27a3-817b-43e5-9890-828616f194fa" />

---

## 💻 Реализация клиента

Клиентская часть реализована в файле:

```text
client.py
```

Клиент создаёт канал подключения к серверу:

```python
grpc.insecure_channel('localhost:50051')
```

После этого создаётся объект `stub`, через который вызывается удалённый метод `Matchmaking`.

Клиент отправляет поток игроков с помощью функции `generate_players`.

Каждый игрок имеет:

- никнейм;
- уровень.

После отправки игроков клиент получает поток ответов от сервера и выводит результаты в терминал.

---

## 📄 Код файла `client.py`

```python
import grpc
import time

import game_pb2
import game_pb2_grpc


def generate_players():
    players = [
        ("PlayerOne", 10),
        ("PlayerTwo", 20),
        ("PlayerThree", 30),
        ("PlayerFour", 40),
    ]

    for nickname, level in players:
        print(f"Отправка: {nickname}")

        yield game_pb2.PlayerInfo(
            nickname=nickname,
            level=level
        )

        time.sleep(1)


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = game_pb2_grpc.GameLobbyStub(channel)

    responses = stub.Matchmaking(generate_players())

    for response in responses:
        print("Ответ сервера:", response.message)


if __name__ == "__main__":
    run()
```

---

## 📷 Скриншот №5 — код клиента

<img width="1191" height="860" alt="Image" src="https://github.com/user-attachments/assets/e871a17d-3228-4379-b943-88909aced4c3" />

---

## 📷 Скриншот №6 — работа клиента

```text
Отправка: PlayerOne
Отправка: PlayerTwo
Ответ сервера: Match found: PlayerOne vs PlayerTwo
Отправка: PlayerThree
Отправка: PlayerFour
Ответ сервера: Match found: PlayerThree vs PlayerFour
```

<img width="828" height="398" alt="Image" src="https://github.com/user-attachments/assets/d28c68bd-41ca-40b7-b863-afc338261a25" />

---

## 🚀 Запуск проекта

Для запуска проекта сначала необходимо активировать виртуальное окружение.

```bash
source venv/bin/activate
```

Если зависимости ещё не установлены, необходимо выполнить команду:

```bash
pip install grpcio grpcio-tools
```

После этого необходимо сгенерировать gRPC-код:

```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. game.proto
```

---

## ▶️ Запуск сервера

Сервер запускается командой:

```bash
python3 server.py
```

После запуска сервер ожидает подключения клиента.

---

## ▶️ Запуск клиента

Клиент запускается во втором терминале командой:

```bash
python3 client.py
```

---

## 📊 Результат работы

После запуска сервера и клиента выполняется обмен сообщениями между клиентом и сервером.

Клиент отправляет данные игроков:

```text
PlayerOne
PlayerTwo
PlayerThree
PlayerFour
```

Сервер формирует игровые пары:

```text
PlayerOne vs PlayerTwo
PlayerThree vs PlayerFour
```

Клиент получает результаты:

```text
Ответ сервера: Match found: PlayerOne vs PlayerTwo
Ответ сервера: Match found: PlayerThree vs PlayerFour
```

---

## ✅ Проверка соответствия заданию

| Требование | Выполнение |
|---|---|
| Реализован сервис GameLobby | Выполнено |
| Реализован метод Matchmaking | Выполнено |
| Используется stream PlayerInfo | Выполнено |
| Используется stream MatchResult | Выполнено |
| Используется Bidirectional Streaming RPC | Выполнено |
| Реализован сервер | Выполнено |
| Реализован клиент | Выполнено |
| Выполнена генерация gRPC-кода | Выполнено |
| Выполнено тестирование | Выполнено |

---

## 📌 Вывод

В ходе выполнения лабораторной работы был реализован gRPC-сервис **GameLobby** с методом **Matchmaking**.

Метод `Matchmaking` использует **Bidirectional Streaming RPC**, что позволяет клиенту и серверу обмениваться потоками сообщений.

В результате работы был реализован механизм поиска игроков и формирования игровых сессий.  
Клиент отправляет информацию об игроках, сервер принимает данные, формирует игровые пары и возвращает результат клиенту.

Также были изучены основы gRPC, Protocol Buffers, генерации кода и реализации клиент-серверного взаимодействия на языке Python.

Лабораторная работа выполнена успешно.
