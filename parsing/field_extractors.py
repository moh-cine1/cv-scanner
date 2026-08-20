import re
import json
from parsing.section_finder import find_section


def extract_email(text: str) -> str | None:
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group() if match else None


def extract_phone(text: str) -> str | None:
    pattern = r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,5}\d{2,4}"
    matches = re.findall(pattern, text)
    candidates = [m.strip() for m in matches if len(re.sub(r"\D", "", m)) >= 8]
    return candidates[0] if candidates else None


def extract_linkedin(text: str) -> str | None:
    match = re.search(r"linkedin\.com/in/[\w-]+", text, re.IGNORECASE)
    return match.group() if match else None


def extract_github(text: str) -> str | None:
    match = re.search(r"github\.com/[\w-]+", text, re.IGNORECASE)
    return match.group() if match else None


def extract_skills(text: str) -> list[str]:
    skills_block = find_section(text, "skills")
    if not skills_block:
        return []

    clean_block = re.sub(r"\s+", " ", skills_block.replace("\n", " ")).strip()
    return [s.strip() for s in re.split(r",(?![^(]*\))", clean_block) if s.strip()]


def extract_education(text: str) -> str:
    return find_section(text, "education")


def extract_experience(text: str) -> str:
    return find_section(text, "experience")


def extract_languages(text: str) -> list[str]:
    block = find_section(text, "languages")
    if not block:
        return []
    return [lang.strip() for lang in block.replace("\n", ",").split(",") if lang.strip()]


def extract_name_heuristic(text: str) -> str | None:
    for line in text.strip().split("\n"):
        clean_line = line.strip()
        if clean_line and not re.search(r"[\d@]", clean_line) and len(clean_line.split()) <= 5:
            return clean_line
    return None


def extract_all_fields(text: str) -> dict:
    return {
        "name": extract_name_heuristic(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "languages": extract_languages(text),
    }


if __name__ == "__main__":
    sample = """John Smith
    Email: john.smith@email.com
    Phone: 0555-123-456
    LinkedIn: linkedin.com/in/johnsmith

    Skills
    Python, SQL, Microsoft Office (Excel, Word, PowerPoint), Machine Learning

    Education
    Bachelor's in Computer Science, University of Algiers, 2022

    Experience
    Software Developer at TechCorp, 2022-2024
    """
    print(json.dumps(extract_all_fields(sample), indent=2, ensure_ascii=False))