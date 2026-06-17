import re
from pathlib import Path

import pdfplumber

COMMON_SKILLS = {
    "python",
    "django",
    "flask",
    "fastapi",
    "sql",
    "postgresql",
    "mysql",
    "redis",
    "celery",
    "aws",
    "docker",
    "javascript",
    "react",
    "html",
    "css",
    "bootstrap",
    "machine learning",
    "nlp",
    "excel",
}


def extract_text_from_pdf(file_path):
    text_parts = []
    with pdfplumber.open(Path(file_path)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return clean_text("\n".join(text_parts))


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_email(text):
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0).lower() if match else ""


def extract_name(text):
    lines = [line.strip() for line in text.split() if line.strip()]
    # Reconstruct first 10 "lines" by splitting on common separators
    raw_lines = []
    current = []
    for word in text[:500].split():
        if any(sep in word for sep in ["|", "•", "-", "/"]) and current:
            raw_lines.append(" ".join(current))
            current = []
        else:
            current.append(word)
        if len(raw_lines) >= 10:
            break
    if current:
        raw_lines.append(" ".join(current))

    skip_words = [
        "@", "http", "www", "phone", "mobile", "email", "address",
        "linkedin", "github", "objective", "summary", "experience",
        "education", "skills", "resume", "cv", "leetcode",
    ]

    for line in raw_lines[:5]:
        line = line.strip()
        if not line or len(line) > 60:
            continue
        if any(word in line.lower() for word in skip_words):
            continue
        if re.search(r"[\d@]", line):
            continue
        # Match names like "M.V Ashika Reddy" or "John Smith"
        match = re.match(r"^([A-Z][A-Za-z.]+(?:\s+[A-Z][A-Za-z.]+){1,4})$", line)
        if match:
            return match.group(1).strip()

    # Fallback — match name with initials like M.V or A.B.C
    match = re.search(
        r"\b([A-Z][A-Za-z.]*\.?\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})\b",
        text[:200]
    )
    if match:
        name = match.group(1).strip()
        if not any(w in name.lower() for w in skip_words):
            return name

    return "Unknown Candidate"

def extract_skills(text):
    lowered = text.lower()
    found = sorted(skill for skill in COMMON_SKILLS if skill in lowered)
    return ", ".join(found)


def extract_experience_years(text):
    patterns = [
        r"(\d+)\+?\s+years?\s+of\s+experience",
        r"experience\s+of\s+(\d+)\+?\s+years?",
        r"(\d+)\+?\s+yrs",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0


def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)
    return {
        "raw_text": text,
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience_years(text),
    }
