import re


def clean_encoding_artifacts(text: str) -> str:
    return text.replace("Â", "").replace("\xa0", " ")


def remove_page_artifacts(text: str) -> str:
    text = re.sub(r"Page\s*\d+\s*/\s*\d+", "", text, flags=re.IGNORECASE)
    return re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_text(raw_text: str) -> str:
    if not raw_text:
        return ""

    text = clean_encoding_artifacts(raw_text)
    text = remove_page_artifacts(text)
    return normalize_whitespace(text)


if __name__ == "__main__":
    sample = "Filing,Â Employee training,Â\n\n\nPage 1/2\n   Multiple   spaces   here"
    print(clean_text(sample))