from database.models import Candidate, Skill, Education, Experience, Language, get_session


def insert_candidate(session, fields: dict, source_file: str = "") -> Candidate:
    candidate = Candidate(
        name=fields.get("name"),
        email=fields.get("email"),
        phone=fields.get("phone"),
        linkedin=fields.get("linkedin"),
        github=fields.get("github"),
        source_file=source_file,
    )

    candidate.skills = [Skill(name=skill) for skill in fields.get("skills", [])]
    candidate.languages = [Language(name=lang) for lang in fields.get("languages", [])]

    if education := fields.get("education"):
        candidate.educations.append(Education(raw_text=education))

    if experience := fields.get("experience"):
        candidate.experiences.append(Experience(raw_text=experience))

    session.add(candidate)
    session.commit()
    return candidate


if __name__ == "__main__":
    session = get_session()
    sample_fields = {
        "name": "John Smith",
        "email": "john.smith@email.com",
        "phone": "0555-123-456",
        "linkedin": "linkedin.com/in/johnsmith",
        "github": None,
        "skills": ["Python", "SQL", "Machine Learning"],
        "education": "Bachelor's in Computer Science, University of Algiers, 2022",
        "experience": "Software Developer at TechCorp, 2022-2024",
        "languages": ["French", "English"],
    }
    inserted = insert_candidate(session, sample_fields, source_file="test.pdf")
    print(f"Candidat inséré avec l'ID {inserted.id}")