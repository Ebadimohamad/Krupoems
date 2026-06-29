import os
import json
import requests

INPUT_FOLDER = "works"
OUTPUT_TRANSLATION = "translatedworks"
OUTPUT_FORMULA = "formulas"

API_KEY = os.environ.get("GEMINI_API_KEY")
if not APIATION = "translatedworks"
OUTPUT_FORMULA = "formulas"

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY is not set.")
    raise SystemExit(1)

API_URL = (
    "https://_KEY}"
)

os.makedirs(OUTPUT_TRANSLATION, exist_ok=True)
os.makedirs(OUTPUT_FORMULA, exist_ok=True)


def call_gemini(prompt: str) -> str | None:
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        if response.status_code != 200:
            print(f"API error {response.status_code}: {response.text}")
            return None

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as exc:
        print(f"Request error: {exc}")
        return None


def clean_json_text(text: str) -> str:
    text = text.strip()
    if text.startswith("
```json"):
text = text[7:]
if text.startswith("
```"):
        text = text[3:]
    if text.endswith("
```"):
text = text[:-3]
return text.strip()


def main():
if not os.path.isdir(INPUT_FOLDER):
print(f"Input folder not found: {INPUT_FOLDER}")
return

files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".txt")]
if not files:
print("No .txt files found.")
return

for filename in files:
input_path = os.path.join(INPUT_FOLDER, filename)
translation_path = os.path.join(OUTPUT_TRANSLATION, filename)
formula_path = os.path.join(OUTPUT_FORMULA, filename.replace(".txt", ".json"))

print(f"Processing: {filename}")

with open(input_path, "r", encoding="utf-8") as f:
poem = f.read()

translation_prompt = (
"You are Kimia. Translate this Persian poem into elegant poetic English. "
"Keep the meaning, tone, and literary depth.\n\n"
f"Poem:\n{poem}"
)

formula_prompt = (
"Analyze this poem and return ONLY valid JSON with these keys: "
"rhythm_structure, semantic_density, mystic_factor, core_equation, key_concepts.\n\n"
f"Poem:\n{poem}"
)

translated = call_gemini(translation_prompt)
formula_raw = call_gemini(formula_prompt)

if translated:
with open(translation_path, "w", encoding="utf-8") as f:
f.write(translated)

if formula_raw:
cleaned = clean_json_text(formula_raw)
try:
parsed = json.loads(cleaned)
with open(formula_path, "w", encoding="utf-8") as f:
json.dump(parsed, f, ensure_ascii=False, indent=2)
except Exception:
with open(formula_path, "w", encoding="utf-8") as f:
f.write(cleaned)

print(f"Done: {filename}")


if __name__ == "__main__":
main()
