import re
from rapidfuzz import fuzz

SECTION_SYNONYMS = {
    "skills": [
        "skills", "technical skills", "core competencies", "competencies",
        "expertise", "compétences", "compétences techniques",
    ],
    "education": [
        "education", "education and training", "academic background",
        "academic history", "formation", "formation académique", "études",
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "employment history", "expérience", "expérience professionnelle",
    ],
    "languages": [
        "languages", "langues",
    ],
}


def find_section_exact(text: str, section_key: str) -> str | None:
    for heading in SECTION_SYNONYMS.get(section_key, []):
        pattern = rf"{re.escape(heading)}:?\s*\n(.*?)(?:\n[ \t]*[A-Z][a-zA-Z ]+\n|\Z)"
        if match := re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            return match.group(1)
    return None


def find_section_fuzzy(text: str, section_key: str, threshold: int = 80) -> str | None:
    lines = text.split("\n")
    headings = SECTION_SYNONYMS.get(section_key, [])

    for i, line in enumerate(lines):
        line_clean = line.strip().lower()
        if not line_clean or len(line_clean) > 40:
            continue

        for heading in headings:
            if fuzz.partial_ratio(line_clean, heading.lower()) >= threshold:
                block_lines = []
                for next_line in lines[i + 1:]:
                    clean_next = next_line.strip()
                    if clean_next and clean_next[0].isupper() and len(clean_next) < 30:
                        break
                    block_lines.append(next_line)
                return "\n".join(block_lines)

    return None


def find_section(text: str, section_key: str) -> str:
    if result := find_section_exact(text, section_key):
        return result.strip()

    if result := find_section_fuzzy(text, section_key):
        return result.strip()

    return ""


if __name__ == "__main__":
    sample = """
    Education and Training
    Bachelor's in Computer Science, 2022

    Skills
    Python, SQL, Excel
    """
    print("Formation:", find_section(sample, "education"))
    print("Compétences:", find_section(sample, "skills"))