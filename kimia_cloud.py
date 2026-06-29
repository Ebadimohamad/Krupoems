
import os

def main():
    # لیست تمام پوشه‌هایی که گیت‌هاب منتظر آن‌هاست
    folders = ['translatedworks', 'formulas', 'logs']
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            # ایجاد یک فایل خالی در هر پوشه برای شناسایی توسط گیت
            with open(f'{folder}/.keep', 'w') as f:
                f.write("placeholder")
    
    print("All necessary folders (translatedworks, formulas, logs) created successfully.")

if __name__ == "__main__":
    main()

