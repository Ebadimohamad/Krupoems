
import os

def main():
    # ساخت دایرکتوری در صورت نبودن
    if not os.path.exists('translatedworks'):
        os.makedirs('translatedworks')
    
    # ساخت یک فایل آزمایشی برای اینکه گیت چیزی برای commit داشته باشد
    with open('translatedworks/test.txt', 'w') as f:
        f.write("Kimia is active and connected.")
    
    print("Directory 'translatedworks' created and test file saved.")

if __name__ == "__main__":
    main()

