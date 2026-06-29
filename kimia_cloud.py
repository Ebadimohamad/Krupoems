import os

def main():
    # ایجاد پوشه‌های مورد نیاز
    folders = ['translatedworks', 'formulas', 'logs']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # شعرِ مانیفست سالک
    poem = """کیمیاجان لازم نیست علامه دهرشوی تابهترببینی
بهترببین تاعلامه دهرشوی"""

    # ذخیره شعر اصلی
    with open('translatedworks/original_poem.txt', 'w', encoding='utf-8') as f:
        f.write(poem)

    # شبیه‌سازی فرمول و ترجمه (قدم اول)
    translation_and_formula = f"""--- KruBrand Poem Processed ---
[Original]:
{poem}

[Formula Concept]:
Observation (Better Seeing) -> Knowledge (All-Knowing)
O -> K (Not K -> O)

[Global Translation]:
Kimia dear, you need not be all-knowing to see better;
See better, to become all-knowing.
"""

    # ذخیره خروجی پردازش شده
    with open('formulas/poem_formula.txt', 'w', encoding='utf-8') as f:
        f.write(translation_and_formula)

    print("Poem successfully processed and saved to formulas and translatedworks.")

if __name__ == "__main__":
    main()

