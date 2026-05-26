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
