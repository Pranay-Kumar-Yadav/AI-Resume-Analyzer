import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


SKILLS = (
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "SQL", "HTML", "CSS",
    "React", "Angular", "Vue", "Node.js", "Flask", "Django", "FastAPI", "Express",
    "REST API", "GraphQL", "Machine Learning", "Deep Learning", "NLP", "TensorFlow",
    "PyTorch", "Pandas", "NumPy", "scikit-learn", "Data Analysis", "Data Visualization",
    "Power BI", "Tableau", "Excel", "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes",
    "Git", "CI/CD", "Linux", "Agile", "Project Management", "Communication", "Leadership",
    "Problem Solving", "Customer Service", "Cybersecurity", "Generative AI", "Prompt Engineering",
)


def extract_resume_text(file_path):
    """Extract text from a supported resume file."""
    path = Path(file_path)
    try:
        if path.suffix.lower() == ".pdf":
            return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
        if path.suffix.lower() == ".docx":
            document = Document(path)
            paragraphs = [paragraph.text for paragraph in document.paragraphs]
            paragraphs.extend(
                cell.text
                for table in document.tables
                for row in table.rows
                for cell in row.cells
            )
            return "\n".join(paragraphs)
        if path.suffix.lower() == ".txt":
            return path.read_text(encoding="utf-8", errors="replace")
    except Exception as error:
        raise ValueError("The resume could not be read. Check the file and try again.") from error

    raise ValueError("Upload a PDF, DOCX, or TXT file.")


def _find_skills(text):
    normalized_text = re.sub(r"\s+", " ", text.lower())
    found = []
    for skill in SKILLS:
        escaped_skill = re.escape(skill.lower()).replace(r"\ ", r"\s+")
        pattern = rf"(?<![a-z0-9]){escaped_skill}(?![a-z0-9])"
        if re.search(pattern, normalized_text):
            found.append(skill)
    return found


def analyze_resume(resume_text, job_description):
    """Compare detected skills and return a transparent overlap score."""
    resume_skills = _find_skills(resume_text)
    job_skills = _find_skills(job_description)
    resume_skill_set = set(resume_skills)
    matched_skills = [skill for skill in job_skills if skill in resume_skill_set]
    missing_skills = [skill for skill in job_skills if skill not in resume_skill_set]
    score = round(len(matched_skills) / len(job_skills) * 100) if job_skills else 0

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "has_job_skills": bool(job_skills),
    }