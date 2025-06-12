# 📄 Resume Parser

A Python-based resume parser that extracts structured information from resumes (`.pdf` or `.docx`) using spaCy NLP, regex, and a machine learning classifier for job role prediction.

---

## 🚀 Features

- Extracts:
  - Name
  - Email
  - Phone Number
  - LinkedIn & GitHub URLs
  - Skills (from a predefined list)
  - Languages (from a predefined list)
  - Education and Experience sections
- Predicts the job role using a trained ML model
- Scores resume based on required skills match

---

## 🧠 Technologies Used

- `spaCy`: NLP for name/entity recognition
- `regex`: Pattern-based extraction
- `pdfminer.six` and `python-docx`: To extract text from PDF/DOCX
- `scikit-learn` + `joblib`: For role prediction
- Predefined skill/language databases

---

## 🗂️ File Structure

```plaintext
resume_parser/
│
├── role_classifier_model.pkl       # Trained ML model (pretrained)
├── vectorizer.pkl                  # Vectorizer used with ML model
├── sample_resume.docx              # Sample resume for testing
└── resume_parser.py                # Main Python script
```

---

## 🛠️ Setup Instructions

1. **Install Required Libraries**

```bash
pip install spacy joblib pdfminer.six python-docx
python -m spacy download en_core_web_sm
```

2. **Ensure You Have the Model Files**

Make sure `role_classifier_model.pkl` and `vectorizer.pkl` exist in your project directory.

3. **Run the Script**

Update the resume path and run the script:

```python
if __name__ == "__main__":
    file_path = "C:/Users/nithy/Downloads/sample_resume.docx"
    result = parse_resume(file_path)
    for key, value in result.items():
        print(f"{key.capitalize()}: {value}\n")
```

---

## 📊 Sample Output

```plaintext
Name: John Doe
Email: john.doe@example.com
Phone: +1 123-456-7890
Linkedin: https://linkedin.com/in/johndoe
Github: https://github.com/johndoe
Skills: ['python', 'sql', 'data analysis']
Languages: ['english']
Education: Bachelor of Science in Computer Science...
Experience: Worked at XYZ Corp as Data Analyst...
Predicted_role: Data Analyst
Resume_score: 100.00% match
```

---

## 🧪 Customization

- **Update `SKILLS_DB` and `LANGUAGES_DB`** to support your own criteria.
- **Improve section detection** by refining the `extract_section()` regex logic.
- **Train your own classifier** using `scikit-learn` and job role-labeled resumes.

---

