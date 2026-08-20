import sys
import os
import json

from extraction.text_extractor import extract_text
from cleaning.text_cleaner import clean_text
from parsing.field_extractors import extract_all_fields
from database.db_operations import insert_candidate
from database.models import get_session


def process_cv(file_path: str, session) -> dict | None:
    print(f"\n--- Traitement de {file_path} ---")

    try:
        raw_text = extract_text(file_path)
        if not raw_text.strip():
            print(f"[main] Aucun texte extrait pour {file_path}, fichier ignoré.")
            return None

        text = clean_text(raw_text)
        fields = extract_all_fields(text)

        insert_candidate(session, fields, source_file=file_path)

        name = fields.get('name') or 'nom non détecté'
        email = fields.get('email') or 'email non détecté'
        print(f"[main] OK — {name} / {email}")

        return fields

    except Exception as e:
        print(f"[main] Erreur lors du traitement de {file_path}: {e}")
        return None


def process_directory(directory_path: str, session) -> list[dict]:
    results = []
    
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".pdf", ".docx")):
            file_path = os.path.join(directory_path, filename)
            result = process_cv(file_path, session)
            if result:
                results.append(result)
                
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <fichier_ou_dossier>")
        sys.exit(1)

    input_path = sys.argv[1]
    session = get_session()

    if os.path.isdir(input_path):
        results = process_directory(input_path, session)
        print(f"\n{len(results)} CV traités avec succès.")
    elif os.path.isfile(input_path):
        result = process_cv(input_path, session)
        if result:
            print("\nRésultat JSON :")
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Chemin introuvable : {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()