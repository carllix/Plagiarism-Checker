import PyPDF2
import numpy as np
import re


def extract_text_from_pdf(pdf_path):
    """
    Fungsi untuk mengekstrak teks dari file PDF
    Parameter:
        pdf_path (str): Path ke file PDF
    Return:
        str: Teks yang diekstrak dari PDF dalam bentuk lowercase
    """
    try:
        with open(pdf_path, "rb") as file:
            # Membuat PDF reader
            pdf_reader = PyPDF2.PdfReader(file)

            # Mengambil teks dari setiap halaman
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            return text.lower()  # Mengubah ke lowercase
    except Exception as e:
        print(f"Error membaca file {pdf_path}: {str(e)}")
        return ""


def clean_text(text):
    """
    Fungsi untuk membersihkan teks dari tanda baca dan karakter khusus
    Parameter:
        text (str): Teks yang akan dibersihkan
    Return:
        str: Teks yang sudah bersih
    """
    # Menghilangkan tanda baca dan karakter khusus
    text = re.sub(r"[^\w\s]", "", text)

    # Menghilangkan angka
    text = re.sub(r"\d+", "", text)

    # Menghilangkan multiple spasi
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_unique_words_and_vectors(text1, text2):
    """
    Fungsi untuk mendapatkan kata unik dan vektor frekuensi
    Parameters:
        text1 (str): Teks dokumen pertama
        text2 (str): Teks dokumen kedua
    Return:
        tuple: (kata_unik, vektor1, vektor2)
    """
    # Membersihkan teks
    clean_text1 = clean_text(text1)
    clean_text2 = clean_text(text2)

    # Memisahkan kata-kata
    words1 = clean_text1.split()
    words2 = clean_text2.split()

    # Mendapatkan kata unik dari kedua dokumen
    unique_words = sorted(list(set(words1 + words2)))

    # Membuat vektor frekuensi untuk setiap dokumen
    vector1 = []
    vector2 = []

    # Menghitung frekuensi setiap kata unik di masing-masing dokumen
    for word in unique_words:
        vector1.append(words1.count(word))
        vector2.append(words2.count(word))

    return unique_words, vector1, vector2


def cosine_similarity(vector1, vector2):
    """
    Menghitung cosine similarity antara dua vektor
    Parameters:
        vector1 (list): Vektor pertama
        vector2 (list): Vektor kedua
    Return:
        float: Nilai cosine similarity
    """
    # Mengubah list menjadi numpy array
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    # Menghitung dot product
    dot_product = np.dot(v1, v2)

    # Menghitung magnitude
    magnitude1 = np.sqrt(np.sum(v1**2))
    magnitude2 = np.sqrt(np.sum(v2**2))

    # Menghitung cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    similarity = dot_product / (magnitude1 * magnitude2)
    return float(similarity)  # Convert numpy float to Python float


def get_plagiarism_level(similarity):
    """
    Menentukan level plagiarisme berdasarkan nilai similarity
    Parameter:
        similarity (float): Nilai similarity
    Return:
        str: Level plagiarisme
    """
    if similarity > 0.70:
        return "Plagiarisme Berat"
    elif 0.30 <= similarity <= 0.70:
        return "Plagiarisme Sedang"
    elif 0 < similarity < 0.30:
        return "Plagiarisme Ringan"
    else:
        return "Tidak Plagiarisme" 


def check_plagiarism(file1_path, file2_path):
    """
    Fungsi untuk memeriksa plagiarisme antara dua file PDF
    Parameters:
        file1_path (str): Path ke file PDF pertama
        file2_path (str): Path ke file PDF kedua
    Return:
        dict: Hasil pengecekan plagiarisme
    """
    # Mengekstrak teks dari kedua file
    text1 = extract_text_from_pdf(file1_path)
    text2 = extract_text_from_pdf(file2_path)

    if not text1 or not text2:
        return {
            "error": "Extraction error",
            "message": "Error extracting text from PDF files",
        }

    # Mendapatkan kata unik dan vektor
    unique_words, vector1, vector2 = get_unique_words_and_vectors(text1, text2)

    # Menghitung similarity
    similarity = cosine_similarity(vector1, vector2)

    # Mendapatkan level plagiarisme
    plagiarism_level = get_plagiarism_level(similarity)

    return {"similarity": similarity, "plagiarism_level": plagiarism_level}
