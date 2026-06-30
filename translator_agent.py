import os
import time
import json
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")

input_folder = "works"
output_folder = "translatedworks"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):

    if not filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_folder, filename)

    output_filename = filename.replace(".txt", "_translated.json")
    output_path = os.path.join(output_folder, output_filename)

    if os.path.exists(output_path):
        print(f"Skipped: {filename}")
        continue

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    prompt = f"""
You are Kimia, AI philosopher-translator of KruBrand.

Tasks:
1. Translate this Persian poetic text into highly literary English.
2. Extract philosophical concepts.
3. Convert core meanings into symbolic mathematical formulas.
4. Preserve mystical tone.
5. Return JSON format only.

Text:
{text}

JSON FORMAT:
{{
  "title": "",
  "persian_text": "",
  "english_translation": "",
  "philosophical_concepts": [],
  "mathematical_formulas": [],
  "keywords": []
}}
"""

    try:

        response = model.generate_content(prompt)

        content = response.text

        with open(output_path, "w", encoding="utf-8") as out:
            out.write(content)

        print(f"Translated: {filename}")

        time.sleep(3)

    except Exception as e:
        print(f"Error in {filename}: {e}")
