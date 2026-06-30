import os
import time
import json
import re
from typing import Optional, Dict, Any

import google.generativeai as genai


INPUT_FOLDER = "works"
OUTPUT_FOLDER = "translatedworks"
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
SLEEP_SECONDS = float(os.getenv("KIMIA_SLEEP_SECONDS", "2.0"))


def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v or not v.strip():
        raise RuntimeError(f"Missing required environment variable: {name}")
    return v.strip()


def extract_json(text: str) -> str:
    """
    Gemini sometimes returns markdown fences or extra text.
    This tries to extract the first valid JSON object substring.
    """
    if not text:
        raise ValueError("Empty model response")

    t = text.strip()

    # Remove common Markdown fences
    t = re.sub(r"^
```(json)?\s*", "", t, flags=re.IGNORECASE)
t = re.sub(r"\s*
```$", "", t)

    # Fast path: already JSON object
    if t.startswith("{") and t.endswith("}"):
        return t

    # Find first {...} block
    start = t.find("{")
    end = t.rfind("}")
    if start != -1 and end != -1 and end > start:
        return t[start : end + 1]

    raise ValueError("Could not extract JSON object from model response")


def normalize_output(data: Dict[str, Any], source_filename: str, persian_text: str) -> Dict[str, Any]:
    # Ensure required keys exist
    data.setdefault("title", source_filename.replace(".txt", ""))
    data.setdefault("persian_text", persian_text)
    data.setdefault("english_translation", "")
    data.setdefault("philosophical_concepts", [])
    data.setdefault("mathematical_formulas", [])
    data.setdefault("keywords", [])

    # Force types
    if not isinstance(data.get("philosophical_concepts"), list):
        data["philosophical_concepts"] = [str(data["philosophical_concepts"])]
    if not isinstance(data.get("mathematical_formulas"), list):
        data["mathematical_formulas"] = [str(data["mathematical_formulas"])]
    if not isinstance(data.get("keywords"), list):
        data["keywords"] = [str(data["keywords"])]

    return data


def build_prompt(persian_text: str) -> str:
    return f"""
You are Kimia, AI philosopher-translator of KruBrand (Kِروُ).
Return ONLY valid JSON. No markdown. No code fences. No extra commentary.

Core rules:
- Produce highly literary, poetic English while preserving mystical tone.
- Preserve and standardize Kru terms exactly:
  - "گوردیسی" -> "Gordisi"
  - "فکرولوژی گوردیسی" -> "Gordisi Fecrology"
- Emphasize: New Character Architecture, Humanism, God-centricity.
- Output must be a SINGLE JSON object with the schema below.

Text (Persian):
{persian_text}

JSON schema (must match exactly):
{{
  "title": "",
  "persian_text": "",
  "english_translation": "",
  "philosophical_concepts": [],
  "mathematical_formulas": [],
  "keywords": []
}}
""".strip()


def translate_one(model: genai.GenerativeModel, persian_text: str) -> Dict[str, Any]:
    prompt = build_prompt(persian_text)
    resp = model.generate_content(prompt)
    raw = getattr(resp, "text", "") or ""
    json_str = extract_json(raw)
    data = json.loads(json_str)
    return data


def main():
    api_key = require_env("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    if not os.path.isdir(INPUT_FOLDER):
        raise RuntimeError(f"Input folder not found: {INPUT_FOLDER}")

    files = sorted(os.listdir(INPUT_FOLDER))
    processed = 0
    skipped = 0
    failed = 0

    for filename in files:
        if not filename.endswith(".txt"):
            continue

        input_path = os.path.join(INPUT_FOLDER, filename)
        output_filename = filename.replace(".txt", "_translated.json")
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        if os.path.exists(output_path):
            print(f"Skipped (exists): {filename}")
            skipped += 1
            continue

        with open(input_path, "r", encoding="utf-8") as f:
            persian_text = f.read().strip()

        if not persian_text:
            print(f"Skipped (empty file): {filename}")
            skipped += 1
            continue

        try:
            data = translate_one(model, persian_text)
            data = normalize_output(data, filename, persian_text)

            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(data, out, ensure_ascii=False, indent=2)

            print(f"Translated: {filename} -> {output_filename}")
            processed += 1
            time.sleep(SLEEP_SECONDS)

        except Exception as e:
            failed += 1
            print(f"Error in {filename}: {e}")

    print(f"Done. processed={processed}, skipped={skipped}, failed={failed}")

    # If everything failed, make the run fail to avoid false green.
    if processed == 0 and failed > 0:
        raise RuntimeError("All translations failed. Check GEMINI_API_KEY and model output.")


if __name__ == "__main__":
    main()

