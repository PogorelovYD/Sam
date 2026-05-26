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
