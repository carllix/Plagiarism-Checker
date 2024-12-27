import PyPDF2
import numpy as np
import os
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
    return similarity


def check_plagiarism(file1_path, file2_path, show_details=True):
    """
    Fungsi untuk memeriksa plagiarisme antara dua file PDF
    Parameters:
        file1_path (str): Path ke file PDF pertama
        file2_path (str): Path ke file PDF kedua
        show_details (bool): Menampilkan detail perhitungan
    Return:
        float: Nilai similarity atau None jika terjadi error
    """
    # Mengekstrak teks dari kedua file
    text1 = extract_text_from_pdf(file1_path)
    text2 = extract_text_from_pdf(file2_path)

    if not text1 or not text2:
        return None

    # Mendapatkan kata unik dan vektor
    unique_words, vector1, vector2 = get_unique_words_and_vectors(text1, text2)

    # Menampilkan detail perhitungan jika diminta
    if show_details:
        print("\nDetail Perhitungan:")
        print("\nTeks setelah dibersihkan:")
        print("Dokumen Uji:", clean_text(text1))
        print("Dokumen Refensi:", clean_text(text2))

        print("\nKata Unik:", unique_words)
        print("\nVektor Dokumen Uji:", vector1)
        print("Vektor Dokumen Referensi:", vector2)

        # Menampilkan frekuensi kata dalam format tabel
        print("\nTabel Frekuensi Kata:")
        print("-" * 50)
        print(f"{'Kata':<15} {'Dokumen Uji':<12} {'Dokumen Referensi':<12}")
        print("-" * 50)
        for i, word in enumerate(unique_words):
            print(f"{word:<15} {vector1[i]:<12} {vector2[i]:<12}")
        print("-" * 50)

    # Menghitung similarity
    return cosine_similarity(vector1, vector2)


def main():
    """
    Fungsi utama untuk menjalankan program
    """
    print("=== Program Deteksi Plagiarisme PDF ===")
    print("\nPastikan file PDF berada dalam folder 'documents'")

    # Meminta input nama file dari pengguna
    dok_uji = input("\nMasukkan nama file Dokumen Uji (contoh: dok1.pdf): ")
    dok_query = input("Masukkan nama file Dokumen Referensi (contoh: dok2.pdf): ")

    # Membuat path lengkap ke file
    file1_path = os.path.join("documents", dok_uji)
    file2_path = os.path.join("documents", dok_query)

    # Memeriksa keberadaan file
    if not os.path.exists(file1_path):
        print(f"\nError: File {dok_uji} tidak ditemukan dalam folder documents!")
        return

    if not os.path.exists(file2_path):
        print(f"\nError: File {dok_query} tidak ditemukan dalam folder documents!")
        return

    # Menghitung similarity
    similarity = check_plagiarism(file1_path, file2_path, show_details=True)

    print("\n" + "=" * 50)
    if similarity is not None:
        print("Hasil Deteksi Plagiarisme:")
        print(f"Dokumen Uji\t\t: {dok_uji}")
        print(f"Dokumen Referensi\t: {dok_query}")
        print(f"Similarity\t\t: {similarity:.2%}")

        # Memberikan interpretasi hasil
        if similarity >= 0.80:
            print("Interpretasi\t\t: Tingkat kemiripan sangat tinggi!")
        elif similarity >= 0.60:
            print("Interpretasi\t\t: Tingkat kemiripan tinggi")
        elif similarity >= 0.40:
            print("Interpretasi\t\t: Tingkat kemiripan sedang")
        else:
            print("Interpretasi\t\t: Tingkat kemiripan rendah")
    else:
        print("Terjadi error saat memproses dokumen")
    print("=" * 50)


if __name__ == "__main__":
    main()
