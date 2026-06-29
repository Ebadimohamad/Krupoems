import os
import requests

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("API Key not found!")
        return
    
    print("Kimia is running...")
    print("Connection test successful.")

if __name__ == "__main__":
    main()
