from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from PlagiarismChecker import check_plagiarism

app = Flask(__name__)
CORS(app)

BASE_UPLOAD_FOLDER = "../../test"
REFERENCE_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "referensi")
TEST_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "uji")
ALLOWED_EXTENSIONS = {"pdf"}

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
        clear_directory(REFERENCE_FOLDER)
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
        clear_directory(TEST_FOLDER)
        filename = secure_filename(file.filename)
        file_path = os.path.join(TEST_FOLDER, filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"message": "Invalid file type"}), 400

@app.route("/check", methods=["GET"])
def check_similarity():
    try:
        # Mendapatkan file dari folder
        test_files = os.listdir(TEST_FOLDER)
        ref_files = os.listdir(REFERENCE_FOLDER)

        if not test_files or not ref_files:
            return (
                jsonify(
                    {
                        "error": "Missing files",
                        "message": "Please upload both test and reference files",
                    }
                ),
                400,
            )

        test_file = os.path.join(TEST_FOLDER, test_files[0])
        ref_file = os.path.join(REFERENCE_FOLDER, ref_files[0])

        # Menjalankan pengecekan plagiarisme
        result = check_plagiarism(test_file, ref_file)

        # Jika ada error
        if "error" in result:
            return jsonify(result), 400

        # Menambahkan informasi nama file
        result["test_file"] = test_files[0]
        result["reference_file"] = ref_files[0]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Processing error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
