import os
import json
import requests
from colorama import Fore, Style
from config import GEMINI_API_KEY, IDENTITIES_DIR

def load_identity(identity_id):
    json_path = os.path.join(IDENTITIES_DIR, identity_id, "identity.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def chat_with_gemini(prompt, context):
    if not GEMINI_API_KEY:
        return "❌ Gemini API key not found. Please set GEMINI_API_KEY in .env"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    full_prompt = f"{context}\nUser: {prompt}\nAI:"
    
    data = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {e}"

def start_chat(identity_id):
    identity = load_identity(identity_id)
    if not identity:
        print(Fore.RED + "❌ Identity not found!")
        return
    
    print(Fore.GREEN + f"\n[+] Chatting with {identity['name']}")
    print(Fore.YELLOW + "Type 'exit' to end chat.\n")
    
    context = f"You are {identity['name']}, a {identity['job']} from {identity['nationality']}. Respond in character."
    
    while True:
        user_input = input(Fore.CYAN + "You: " + Style.RESET_ALL)
        if user_input.lower() == 'exit':
            break
        
        response = chat_with_gemini(user_input, context)
        print(Fore.MAGENTA + f"{identity['name']}: {response}" + Style.RESET_ALL)