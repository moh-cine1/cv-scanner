# CV Scanner — Projet de stage

Système d'extraction automatique d'informations à partir de CV (PDF/DOCX),
avec bascule OCR pour les documents scannés, parsing par regex enrichi
de synonymes/fuzzy matching, et stockage dans une base SQLite relationnelle.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt --break-system-packages
```

Dépendances système requises (Ubuntu) :
```bash
sudo apt install tesseract-ocr tesseract-ocr-fra poppler-utils
```

## Structure du projet

```
cv-scanner-project/
├── extraction/
│   └── text_extractor.py      # pdfplumber + fallback OCR (Tesseract)
├── cleaning/
│   └── text_cleaner.py        # nettoyage regex (encodage, espaces...)
├── parsing/
│   ├── section_finder.py      # détection de section (synonymes + fuzzy)
│   └── field_extractors.py    # extraction email, tél, compétences...
├── database/
│   ├── models.py              # schéma SQLAlchemy
│   └── db_operations.py       # insertion des CV parsés
├── llm/
│   └── ollama_client.py       # extraction complémentaire via LLM local (optionnel)
├── main.py                    # pipeline complet
└── tests/
    └── test_corpus/           # CV de test (PDF/DOCX)
```

## Utilisation

Traiter un seul CV :
```bash
python main.py tests/test_corpus/exemple.pdf
```

Traiter tout un dossier de CV :
```bash
python main.py tests/test_corpus/
```

Les résultats sont insérés dans `cv_database.db` (SQLite), consultable avec
n'importe quel client SQLite (ex: DB Browser for SQLite).

## Tester un module individuellement

Chaque module peut être exécuté seul pour du débogage rapide :
```bash
python -m extraction.text_extractor
python -m cleaning.text_cleaner
python -m parsing.field_extractors
```

## LLM local (optionnel)

Si Ollama est installé et un modèle téléchargé (`ollama pull qwen3:4b`) :
```bash
python -m llm.ollama_client
```

## Limites connues

- L'extraction du nom repose sur une heuristique simple (première ligne
  sans chiffre) — amélioration possible via spaCy NER (voir rapport).
- Les formats de date très hétérogènes ne sont pas encore normalisés.
- Le fuzzy matching des sections a un seuil fixe (80) qui peut nécessiter
  un ajustement selon le corpus réel de CV traités.
