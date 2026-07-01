import os
import time
import google.generativeai as genai

# تنظیمات API
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

# انتخاب مدل
model = genai.GenerativeModel("gemini-1.5-pro")

# پوشه‌ها
input_folder = "works"
output_folder = "translated_works"

# ساخت پوشه خروجی در صورت نبودن
os.makedirs(output_folder, exist_ok=True)

print("🚀 ایجنت مترجم آماده به کار است...")

# گرفتن فایل‌های txt و md
if not os.path.exists(input_folder):
    print(f"⚠️ پوشه ورودی پیدا نشد: {input_folder}")
    raise SystemExit(1)

files = [f for f in os.listdir(input_folder) if f.endswith((".txt", ".md"))]

if not files:
    print("⚠️ هیچ فایل .txt یا .md در پوشه works پیدا نشد.")
    raise SystemExit(0)

for filename in files:
    file_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, f"translated_{filename}")

    # اگر فایل قبلاً ترجمه شده، رد کن
    if os.path.exists(output_path):
        print(f"⏩ قبلاً ترجمه شده: {filename}")
        continue

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        prompt = f"""
You are a professional literary translator.

Translate the following Persian text into fluent, natural English.
Preserve line breaks, structure, tone, and meaning.
Do not add explanations or comments.

TEXT:
{content}
"""

        response = model.generate_content(prompt)
        translated_text = response.text.strip()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_text)

        print(f"✅ ترجمه شد: {filename} -> {output_path}")

        time.sleep(3)

    except Exception as e:
        print(f"❌ خطا در ترجمه {filename}: {e}")

print("🎉 عملیات خزش و ترجمه به پایان رسید!")


