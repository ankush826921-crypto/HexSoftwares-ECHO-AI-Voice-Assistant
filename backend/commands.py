import datetime, webbrowser, os, subprocess, pyautogui, json, random, platform, psutil
from plyer import notification

class CommandHandler:
    def __init__(self):
        self.reminders_file = "data/reminders.json"
        self.notes_file = "data/notes.json"
        os.makedirs("data", exist_ok=True)
        for f in [self.reminders_file, self.notes_file]:
            if not os.path.exists(f):
                with open(f, "w") as fp:
                    json.dump([], fp)
    
    def execute(self, intent, params):
        # Time & Date
        if intent == "time":
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
        if intent == "date":
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
        
        # Web & Search
        if intent == "open":
            site = params.get("site", "")
            sites = {
                "youtube": "https://youtube.com",
                "google": "https://google.com",
                "github": "https://github.com",
                "gmail": "https://gmail.com",
                "facebook": "https://facebook.com",
                "twitter": "https://twitter.com",
                "instagram": "https://instagram.com",
                "linkedin": "https://linkedin.com",
                "reddit": "https://reddit.com",
                "amazon": "https://amazon.com",
                "flipkart": "https://flipkart.com",
                "netflix": "https://netflix.com",
                "spotify": "https://spotify.com",
                "whatsapp": "https://web.whatsapp.com",
                "chatgpt": "https://chat.openai.com",
                "gemini": "https://gemini.google.com"
            }
            url = sites.get(site, f"https://{site}.com")
            webbrowser.open(url)
            return f"Opening {site}"
        
        if intent == "search":
            query = params.get("query", "")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            return f"Searching Google for {query}"
        
        if intent == "youtube":
            query = params.get("query", "")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            return f"Playing {query} on YouTube"
        
        if intent == "weather":
            city = params.get("city", "Delhi")
            try:
                import requests
                url = f"https://wttr.in/{city}?format=%C+%t"
                resp = requests.get(url, timeout=5)
                weather_info = resp.text.strip()
                condition_parts = weather_info.split(' ')
                temp = condition_parts[-1]
                condition = ' '.join(condition_parts[:-1]) if len(condition_parts) > 1 else weather_info
                
                widget_html = f'''
                <div class="weather-widget">
                    <div class="weather-icon">🌤️</div>
                    <div class="weather-details">
                        <div class="weather-city">{city}</div>
                        <div class="weather-temp">{temp}</div>
                        <div class="weather-cond">{condition}</div>
                    </div>
                </div>
                '''
                return {
                    "response": f"The weather in {city} is {weather_info}.",
                    "widget": widget_html
                }
            except:
                return "Weather service unavailable."
        
        # Productivity: Reminders & Notes
        if intent == "reminder":
            text = params.get("text", "")
            reminders = json.load(open(self.reminders_file))
            reminders.append({"text": text, "created": str(datetime.datetime.now())})
            json.dump(reminders, open(self.reminders_file, "w"))
            return f"Reminder set: {text}"
        
        if intent == "show_reminders":
            reminders = json.load(open(self.reminders_file))
            if not reminders:
                return "No reminders."
            return "\n".join([f"• {r['text']}" for r in reminders[-5:]])
        
        if intent == "note":
            text = params.get("text", "")
            notes = json.load(open(self.notes_file))
            notes.append({"text": text, "created": str(datetime.datetime.now())})
            json.dump(notes, open(self.notes_file, "w"))
            return f"Note saved: {text}"
        
        if intent == "show_notes":
            notes = json.load(open(self.notes_file))
            if not notes:
                return "No notes."
            return "\n".join([f"• {n['text']}" for n in notes[-5:]])
        
        # Calculator
        if intent == "calculate":
            expr = params.get("expr", "")
            try:
                result = eval(expr)
                return f"{expr} = {result}"
            except:
                return "Sorry, couldn't calculate that."
        
        # Entertainment
        if intent == "joke":
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "What do you call a snake that builds computers? A python!",
                "Why did the developer go broke? Because he used up all his cache!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
                "Why do Python developers have poor sense of smell? Because they can't parse air."
            ]
            return random.choice(jokes)
        
        if intent == "quote":
            quotes = [
                "The only way to do great work is to love what you do. – Steve Jobs",
                "Innovation distinguishes between a leader and a follower. – Steve Jobs",
                "Stay hungry, stay foolish. – Steve Jobs",
                "Talk is cheap. Show me the code. – Linus Torvalds",
                "Simplicity is the soul of efficiency. – Austin Freeman"
            ]
            return random.choice(quotes)
        
        # System Control
        if intent == "screenshot":
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot(filename)
            return f"Screenshot saved as {filename}"
        
        if intent == "shutdown":
            if platform.system() == "Windows":
                os.system("shutdown /s /t 10")
                return "Shutting down in 10 seconds. Say 'cancel shutdown' to abort."
            else:
                return "Shutdown not supported."
        
        if intent == "restart":
            if platform.system() == "Windows":
                os.system("shutdown /r /t 10")
                return "Restarting in 10 seconds. Say 'cancel shutdown' to abort."
            else:
                return "Restart not supported."
        
        if intent == "cancel_shutdown":
            os.system("shutdown /a")
            return "Shutdown cancelled."
        
        if intent == "lock":
            if platform.system() == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "Screen locked."
            else:
                return "Lock not supported."
        
        if intent == "volume_up":
            pyautogui.press("volumeup", presses=3)
            return "Volume increased."
        
        if intent == "volume_down":
            pyautogui.press("volumedown", presses=3)
            return "Volume decreased."
        
        if intent == "mute":
            pyautogui.press("volumemute")
            return "System muted."
        
        if intent == "unmute":
            pyautogui.press("volumemute")
            return "Unmuted."
        
        if intent == "battery":
            battery = psutil.sensors_battery()
            percent = battery.percent
            plugged = battery.power_plugged
            status = "plugged in" if plugged else "not plugged"
            return f"Battery is at {percent}% and {status}."
        
        if intent == "cpu":
            cpu_percent = psutil.cpu_percent(interval=0.5)
            return f"CPU usage is {cpu_percent}%."
        
        if intent == "memory":
            mem = psutil.virtual_memory()
            return f"Memory usage is {mem.percent}%."
        
        # Open Apps
        if intent == "open_app":
            app = params.get("app", "")
            apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "vscode": "code",
                "spotify": "spotify",
                "camera": "start microsoft.windows.camera:"
            }
            if app in apps:
                os.system(apps[app])
                return f"Opening {app}"
            return f"App '{app}' not recognized."
        
        if intent == "close_app":
            app = params.get("app", "")
            # Simple: taskkill on Windows
            os.system(f"taskkill /f /im {app}.exe >nul 2>&1")
            return f"Attempted to close {app}."
        
        # AI Chat (optional, needs API key)
        if intent == "ai":
            from backend.ai_chat import AIChat
            api_key = params.get("api_key", "")
            history = params.get("history", [])
            ai = AIChat(api_key=api_key)
            return ai.ask(params.get("question", ""), history=history)
        
        # News (simple scraping)
        if intent == "news":
            try:
                import requests
                from bs4 import BeautifulSoup
                url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
                response = requests.get(url)
                # quick hack: extract titles
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                titles = []
                for item in root.findall(".//item")[:5]:
                    title = item.find("title").text
                    titles.append(f"• {title}")
                return "Top headlines:\n" + "\n".join(titles)
            except:
                return "News service unavailable. Try 'search Google for news'."
        
        # Exit
        if intent == "exit":
            return "Goodbye! Have a great day."
        
        # Unknown
        return "I didn't understand that command. Please try again."