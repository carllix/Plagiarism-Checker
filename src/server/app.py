from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Konfigurasi folder upload
BASE_UPLOAD_FOLDER = "../../test"
REFERENCE_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "referensi")
TEST_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "uji")
ALLOWED_EXTENSIONS = {"pdf"}

# Membuat folder test dan subfoldernya jika belum ada
for folder in [REFERENCE_FOLDER, TEST_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def clear_directory(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error: {e}")


@app.route("/upload/reference", methods=["POST"])
def upload_reference():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Bersihkan folder referensi terlebih dahulu
        clear_directory(REFERENCE_FOLDER)

        # Simpan file baru
        filename = secure_filename(file.filename)
        file_path = os.path.join(REFERENCE_FOLDER, filename)
        file.save(file_path)

        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"message": "Invalid file type"}), 400


@app.route("/upload/test", methods=["POST"])
def upload_test():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Bersihkan folder uji terlebih dahulu
        clear_directory(TEST_FOLDER)

        # Simpan file baru
        filename = secure_filename(file.filename)
        file_path = os.path.join(TEST_FOLDER, filename)
        file.save(file_path)

        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"message": "Invalid file type"}), 400


@app.route("/check", methods=["GET"])
def check_similarity():
    # Placeholder untuk fungsi pengecekan similarity
    return jsonify({"message": "Similarity check endpoint"})


if __name__ == "__main__":
    app.run(debug=True)
