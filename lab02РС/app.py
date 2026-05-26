from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Имитация базы данных файлового хранилища
files = [
    {
        "id": 1,
        "filename": "document.pdf",
        "size": 2048,
        "upload_date": "2026-01-01 10:00:00"
    },
    {
        "id": 2,
        "filename": "image.png",
        "size": 1024,
        "upload_date": "2026-01-02 12:30:00"
    }
]

next_id = 3


# Получение списка всех файлов
@app.route("/api/files", methods=["GET"])
def get_files():
    return jsonify(files), 200


# Получение информации о файле по id
@app.route("/api/files/<int:file_id>", methods=["GET"])
def get_file(file_id):
    for file in files:
        if file["id"] == file_id:
            return jsonify(file), 200

    return jsonify({"error": "File not found"}), 404


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


# Удаление файла по id
@app.route("/api/files/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    for file in files:
        if file["id"] == file_id:
            files.remove(file)
            return jsonify({"message": "File deleted successfully"}), 200

    return jsonify({"error": "File not found"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)