import json
import ollama

DEFAULT_MODEL = "qwen3:4b"


def extract_fields_llm(text: str, model: str = DEFAULT_MODEL) -> dict | None:
    prompt = f"""/no_think
Extract the following fields from this CV and return ONLY valid JSON, no explanation.
If a field is not found, use null.

Fields: name, email, phone, skills (as a list), education

CV text:
{text}
"""

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            think=False,
            format="json",
            options={"num_predict": 500, "num_ctx": 4096},
        )
        raw_output = response["message"]["content"]
        return json.loads(raw_output)

    except json.JSONDecodeError:
        print(f"Réponse non-JSON reçue du modèle: {raw_output}")
        return None
    except Exception as e:
        print(f"Erreur de connexion à Ollama: {e}")
        return None


if __name__ == "__main__":
    sample = "John Smith, john.smith@email.com, skills: Python, SQL"
    print(extract_fields_llm(sample))