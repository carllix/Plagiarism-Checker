import PyPDF2
import numpy as np
import re

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.lower()
    except Exception as e:
        print(f"Error membaca file {pdf_path}: {str(e)}")
        return ""


def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_unique_words_and_vectors(text1, text2):
    clean_text1 = clean_text(text1)
    clean_text2 = clean_text(text2)

    words1 = clean_text1.split()
    words2 = clean_text2.split()

    unique_words = sorted(list(set(words1 + words2)))

    vector1 = []
    vector2 = []

    for word in unique_words:
        vector1.append(words1.count(word))
        vector2.append(words2.count(word))

    return unique_words, vector1, vector2


def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    dot_product = np.dot(v1, v2)

    magnitude1 = np.sqrt(np.sum(v1**2))
    magnitude2 = np.sqrt(np.sum(v2**2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    similarity = dot_product / (magnitude1 * magnitude2)
    return float(similarity)


def get_plagiarism_level(similarity):
    if similarity > 0.70:
        return "Plagiarisme Berat"
    elif 0.30 <= similarity <= 0.70:
        return "Plagiarisme Sedang"
    elif 0 < similarity < 0.30:
        return "Plagiarisme Ringan"
    else:
        return "Tidak Plagiarisme" 


def check_plagiarism(file1_path, file2_path):
    text1 = extract_text_from_pdf(file1_path)
    text2 = extract_text_from_pdf(file2_path)

    if not text1 or not text2:
        return {
            "error": "Extraction error",
            "message": "Error extracting text from PDF files",
        }

    unique_words, vector1, vector2 = get_unique_words_and_vectors(text1, text2)

    similarity = cosine_similarity(vector1, vector2)

    plagiarism_level = get_plagiarism_level(similarity)

    return {"similarity": similarity, "plagiarism_level": plagiarism_level}
