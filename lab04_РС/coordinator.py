import ssl
from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


BACKEND_SERVERS = [
    "https://127.0.0.1:5001/process",
    "https://127.0.0.1:5002/process"
]


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    language = request.headers.get("Accept-Language", "en")

    print("\n[Coordinator] Получен запрос от клиента")
    print(f"[Coordinator] Accept-Language: {language}")

    for server_url in BACKEND_SERVERS:
        try:
            print(f"[Coordinator] Пробую отправить запрос на {server_url}")

            response = requests.post(
                server_url,
                json=data,
                headers={"Accept-Language": language},
                cert=("certs/client_cert.pem", "certs/client_key.pem"),
                verify="certs/ca_cert.pem",
                timeout=3
            )

            if response.status_code == 200:
                print(f"[Coordinator] Успешный ответ от {server_url}")
                return jsonify(response.json()), 200

            print(f"[Coordinator] Сервер {server_url} вернул ошибку {response.status_code}")

        except requests.exceptions.RequestException as error:
            print(f"[Coordinator] Сервер {server_url} недоступен")
            print(f"[Coordinator] Ошибка: {error}")
            print("[Coordinator] Выполняю failover на следующий сервер")

    return jsonify({"error": "All backend servers are unavailable"}), 503


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "coordinator ok"})


def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(
        certfile="certs/server_cert.pem",
        keyfile="certs/server_key.pem"
    )
    context.load_verify_locations(cafile="certs/ca_cert.pem")

    return context


if __name__ == "__main__":
    ssl_context = create_ssl_context()

    print("Coordinator started on https://127.0.0.1:8000")
    print("mTLS is enabled")
    print("Failover is enabled")

    app.run(
        host="127.0.0.1",
        port=8000,
        ssl_context=ssl_context
    )