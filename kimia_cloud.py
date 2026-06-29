import os
import requests
import json

def call_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None

    # آدرس API جمینی برای مدل پیش‌فرض
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"API Error: Status code {response.status_code}")
            return None
        
        data = response.json()
        # استخراج پاسخ متنی از جی‌سون جمینی
        text_response = data['candidates'][0]['content']['parts'][0]['text']
        return text_response
    except Exception as e:
        print(f"Exception during request: {e}")
        return None

def clean_json_text(text):
    text = text.strip()
    # تمیز کردن تگ‌های مارک‌داون جی‌سون که ممکن است مدل برگردانده باشد
    if text.startswith("
```json"):
text = text[7:]
elif text.startswith("
```"):
        text = text[3:]
        
    if text.endswith("
```"):
text = text[:-3]

return text.strip()

# برای آزمایش صحت اجرا در محیط کلود
if __name__ == "__main__":
print("Kimia Cloud Processor started successfully...")
# یک پرامپت ساده برای تست اتصال
test_result = call_gemini("Say 'Kimia is ready' in Persian.")
print("Test Response from Gemini:", test_result)
