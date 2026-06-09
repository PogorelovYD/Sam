import sys
import requests
from cryptography.fernet import Fernet


def load_fernet():
    with open("encryption_key.txt", "rb") as key_file:
        key = key_file.read()
    return Fernet(key)


def main():
    language = "ru"
    message = "Привет от клиента"

    if len(sys.argv) >= 2:
        language = sys.argv[1]

    if len(sys.argv) >= 3:
        message = " ".join(sys.argv[2:])

    fernet = load_fernet()

    encrypted_payload = fernet.encrypt(message.encode("utf-8")).decode("utf-8")

    print("[Client] Исходное сообщение:", message)
    print("[Client] Язык:", language)
    print("[Client] Зашифрованная полезная нагрузка:", encrypted_payload)

    response = requests.post(
        "https://127.0.0.1:8000/process",
        json={"payload": encrypted_payload},
        headers={"Accept-Language": language},
        cert=("certs/client_cert.pem", "certs/client_key.pem"),
        verify="certs/ca_cert.pem",
        timeout=5
    )

    print("[Client] HTTP status:", response.status_code)

    if response.status_code != 200:
        print("[Client] Ошибка:", response.text)
        return

    response_data = response.json()
    encrypted_response = response_data["payload"]

    decrypted_response = fernet.decrypt(
        encrypted_response.encode("utf-8")
    ).decode("utf-8")

    print("[Client] Ответил сервер:", response_data["server"])
    print("[Client] Зашифрованный ответ:", encrypted_response)
    print("[Client] Расшифрованный ответ:", decrypted_response)


if __name__ == "__main__":
    main()