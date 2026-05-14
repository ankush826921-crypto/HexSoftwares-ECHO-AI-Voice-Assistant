import requests
import os
import urllib.parse

class AIChat:
    def __init__(self, api_key=""):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        if not self.api_key:
            self.enabled = False
        else:
            self.enabled = True
            self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
    
    def ask(self, question, history=None):
        if history is None:
            history = []
            
        if self.enabled:
            contents = []
            for msg in history:
                gemini_role = "user" if msg.get("role") == "user" else "model"
                contents.append({"role": gemini_role, "parts": [{"text": msg.get("text", "")}]})
            
            contents.append({"role": "user", "parts": [{"text": question}]})
            
            try:
                response = requests.post(self.url, json={"contents": contents})
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                print(e)
                pass # fallback to wiki if AI fails
                
        # Fallback to Wikipedia API using requests
        headers = {'User-Agent': 'NovaWebAssistant/1.0'}
        try:
            # 1. Search for title
            query = urllib.parse.quote(question)
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=1&namespace=0&format=json"
            res = requests.get(search_url, headers=headers).json()
            
            # If no results on direct search, strip generic words and try again
            if len(res) < 2 or len(res[1]) == 0:
                clean_q = question.lower().replace("what is", "").replace("who is", "").replace("tell me about", "").strip()
                if clean_q:
                    query = urllib.parse.quote(clean_q)
                    search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=1&namespace=0&format=json"
                    res = requests.get(search_url, headers=headers).json()

            if len(res) >= 2 and len(res[1]) > 0:
                title = res[1][0]
                # 2. Get short summary
                title_encoded = urllib.parse.quote(title)
                prop_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=2&exlimit=1&titles={title_encoded}&explaintext=1&format=json"
                data = requests.get(prop_url, headers=headers).json()
                pages = data.get("query", {}).get("pages", {})
                for page_id in pages:
                    extract = pages[page_id].get("extract", "")
                    if extract:
                        return extract
            return "I don't have an answer for that. My capabilities are limited without an AI API key."
        except Exception as e:
            return "I am currently offline or experiencing a server issue."