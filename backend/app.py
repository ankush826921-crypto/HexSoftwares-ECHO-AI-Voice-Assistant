# backend/app.py
from flask import Flask, render_template, request, jsonify
from backend.commands import CommandHandler
import re

app = Flask(__name__, template_folder="../templates", static_folder="../static")
handler = CommandHandler()

def parse_command(text):
    text = text.lower().strip()
    
    # Time
    if re.search(r"(time|current time|what.*time|tell.*time)", text):
        return ("time", {})
    # Date
    if re.search(r"(date|today'?s date|what.*date)", text):
        return ("date", {})
    # Weather
    weather_match = re.search(r"weather in (\w+)", text)
    if weather_match:
        return ("weather", {"city": weather_match.group(1)})
    if "weather" in text:
        return ("weather", {"city": "Delhi"})
    # Open website
    open_match = re.search(r"open\s+(\w+)", text)
    if open_match:
        return ("open", {"site": open_match.group(1)})
    # Search Google
    search_match = re.search(r"search\s+(.*)", text)
    if search_match:
        return ("search", {"query": search_match.group(1)})
    # YouTube
    yt_match = re.search(r"play\s+(.*)\s+on\s+youtube", text)
    if yt_match:
        return ("youtube", {"query": yt_match.group(1)})
    # Reminder
    rem_match = re.search(r"set\s+reminder\s+(.*)", text)
    if rem_match:
        return ("reminder", {"text": rem_match.group(1)})
    # Show reminders
    if re.search(r"(show|list)\s+reminders", text):
        return ("show_reminders", {})
    # Note
    note_match = re.search(r"take\s+note\s+(.*)", text)
    if note_match:
        return ("note", {"text": note_match.group(1)})
    # Show notes
    if re.search(r"(show|read)\s+notes", text):
        return ("show_notes", {})
    # Calculator
    calc_match = re.search(r"calculate\s+(.*)", text)
    if calc_match:
        return ("calculate", {"expr": calc_match.group(1)})
    # Joke
    if re.search(r"(joke|tell me a joke|funny)", text):
        return ("joke", {})
    # Quote
    if re.search(r"(quote|inspirational quote|motivational)", text):
        return ("quote", {})
    # Screenshot
    if "screenshot" in text:
        return ("screenshot", {})
    # Shutdown
    if re.search(r"shutdown|turn off", text):
        return ("shutdown", {})
    # Restart
    if re.search(r"restart|reboot", text):
        return ("restart", {})
    # Cancel shutdown
    if re.search(r"cancel shutdown|abort shutdown", text):
        return ("cancel_shutdown", {})
    # Lock
    if re.search(r"lock screen|lock computer", text):
        return ("lock", {})
    # Volume
    if "volume up" in text:
        return ("volume_up", {})
    if "volume down" in text:
        return ("volume_down", {})
    if "mute" in text:
        return ("mute", {})
    if "unmute" in text:
        return ("unmute", {})
    # Battery
    if "battery" in text:
        return ("battery", {})
    # CPU
    if "cpu" in text:
        return ("cpu", {})
    # Memory
    if "memory" in text:
        return ("memory", {})
    # Open app
    app_match = re.search(r"open\s+(notepad|calculator|paint|chrome|firefox|edge|cmd|powershell|vscode|spotify|camera)", text)
    if app_match:
        return ("open_app", {"app": app_match.group(1)})
    # Close app
    close_match = re.search(r"close\s+(\w+)", text)
    if close_match:
        return ("close_app", {"app": close_match.group(1)})
    # AI chat
    ai_match = re.search(r"(ask|chat with ai|question for ai)\s+(.*)", text)
    if ai_match:
        return ("ai", {"question": ai_match.group(2)})
    # News
    if "news" in text:
        return ("news", {})
    # Exit
    if re.search(r"(exit|quit|goodbye|bye)", text):
        return ("exit", {})
    
    # If no explicit command is matched, use AI to answer
    if text:
        return ("ai", {"question": text})
        
    return ("unknown", {})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    text = data.get("text", "")
    api_key = data.get("api_key", "")
    history = data.get("history", [])
    
    intent, params = parse_command(text)
    params["api_key"] = api_key
    params["history"] = history
    
    response = handler.execute(intent, params)
    
    if isinstance(response, dict):
        return jsonify(response)
        
    return jsonify({"response": str(response)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)