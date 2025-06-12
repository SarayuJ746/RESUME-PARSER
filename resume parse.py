# Resume Parser and Analyzer with Role Prediction, Scoring, and Insights

import re
import spacy
import joblib
from pdfminer.high_level import extract_text as extract_text_from_pdf
from docx import Document

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Try to load role prediction model and vectorizer
try:
    role_model = joblib.load("role_classifier_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
except:
    role_model = None
    vectorizer = None

# Databases
SKILLS_DB = ["python", "java", "sql", "machine learning", "deep learning",
             "data analysis", "django", "flask", "excel"]
LANGUAGES_DB = ["english", "hindi", "telugu", "tamil", "kannada", "french", "german"]

# --- Text Extraction ---
def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text(path):
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.endswith(".docx"):
        return extract_text_from_docx(path)
    else:
        raise ValueError("Unsupported file format (use .pdf or .docx)")

# --- Extraction Functions ---
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r"(\+?\d{1,3})?[\s-]?\(?\d{3,5}\)?[\s-]?\d{3,5}[\s-]?\d{3,5}", text)
    return match.group() if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_links(text):
    linkedin = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9\-_/]+", text)
    github = re.search(r"(https?://)?(www\.)?github\.com/[a-zA-Z0-9\-_/]+", text)
    return {
        "linkedin": linkedin.group() if linkedin else None,
        "github": github.group() if github else None
    }

def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in SKILLS_DB if skill in text_lower]

def extract_languages(text):
    text_lower = text.lower()
    return [lang for lang in LANGUAGES_DB if lang in text_lower]

def extract_section(text, section_name):
    pattern = re.compile(rf"{section_name}\s*[:\-]?\s*(.*?)(?=\n\n|\n[A-Z][a-zA-Z ]+:)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else None

# --- Role Prediction ---
def predict_role(text):
    if role_model and vectorizer:
        X = vectorizer.transform([text])
        return role_model.predict(X)[0]
    return "Unknown Role (model not loaded)"

# --- Resume Scoring ---
def score_resume(skills, required_skills):
    match_count = len(set(skills) & set(required_skills))
    return (match_count / len(required_skills)) * 100 if required_skills else 0

# --- Resume Parser ---
def parse_resume(file_path, required_skills=None):
    text = extract_text(file_path)
    links = extract_links(text)
    skills = extract_skills(text)
    languages = extract_languages(text)
    required_skills = required_skills or ["python", "sql", "data analysis"]

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": links["linkedin"],
        "github": links["github"],
        "skills": skills,
        "languages": languages,
        "education": extract_section(text, "education"),
        "experience": extract_section(text, "experience"),
        "predicted_role": predict_role(text),
        "resume_score": f"{score_resume(skills, required_skills):.2f}% match"
    }

# --- Run Example ---
if __name__ == "__main__":
    file_path = "C:/Users/nithy/Downloads/sample_resume.docx"
    result = parse_resume(file_path)
    for key, value in result.items():
        print(f"{key.capitalize()}: {value}\n")
