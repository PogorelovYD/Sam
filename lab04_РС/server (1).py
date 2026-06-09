import ssl
import sys
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet


app = Flask(__name__)


def load_fernet():
    with open("encryption_key.txt", "rb") as key_file:
        key = key_file.read()
    return Fernet(key)


fernet = load_fernet()


TRANSLATIONS = {
    "ru": {
        "processed": "Данные успешно обработаны сервером",
        "received": "Полученные данные",
        "language": "Язык ответа"
    },
    "en": {
        "processed": "Data successfully processed by server",
        "received": "Received data",
        "language": "Response language"
    },
    "es": {
        "processed": "Datos procesados correctamente por el servidor",
        "received": "Datos recibidos",
        "language": "Idioma de respuesta"
    }
}


def get_language():
    header = request.headers.get("Accept-Language", "en").lower()

    if header.startswith("ru"):
        return "ru"
    if header.startswith("es"):
        return "es"

    return "en"


@app.route("/process", methods=["POST"])
def process_data():
    port = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    lang = get_language()

    data = request.get_json()

    if not data or "payload" not in data:
        return jsonify({"error": "Encrypted payload is required"}), 400

    encrypted_payload = data["payload"].encode("utf-8")

    try:
        decrypted_payload = fernet.decrypt(encrypted_payload).decode("utf-8")
    except Exception:
        return jsonify({"error": "Cannot decrypt payload"}), 400

    print(f"[Server {port}] Получен зашифрованный запрос")
    print(f"[Server {port}] Расшифрованные данные: {decrypted_payload}")
    print(f"[Server {port}] Accept-Language: {lang}")

    text = TRANSLATIONS[lang]

    response_text = (
        f"{text['processed']} {port}. "
        f"{text['received']}: {decrypted_payload}. "
        f"{text['language']}: {lang}"
    )

    encrypted_response = fernet.encrypt(response_text.encode("utf-8")).decode("utf-8")

    return jsonify({
        "server": port,
        "payload": encrypted_response
    })


@app.route("/health", methods=["GET"])
def health():
    port = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    return jsonify({"status": "ok", "server": port})


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
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    ssl_context = create_ssl_context()

    print(f"Secure server started on https://127.0.0.1:{port}")
    print("mTLS is enabled")
    print("Fernet encryption is enabled")

    app.run(
        host="127.0.0.1",
        port=port,
        ssl_context=ssl_context
    )