# 🎧 ECHO AI Voice Assistant (v2.0)

**ECHO** is a modern, intelligent, web‑based voice assistant that bridges the gap between your browser and your local system. Built with **Python (Flask)** on the backend and a premium, interactive frontend, ECHO lets you control your PC, boost productivity, and talk to Generative AI – all using just your voice.

![img](https://github.com/user-attachments/assets/f3dec23f-a302-47cd-ae04-4450acd60726) 


---

## ✨ Key Features

### 🧠 Advanced AI & Smart Fallback
- **Google Gemini 2.0 Flash** integration – natural, context‑aware conversations.
- **Smart fallback** – if no API key is provided or the AI service fails, ECHO automatically uses the **Wikipedia API** to answer your questions. You'll always get a response.

### 💻 System Control (Windows)
- **Hardware stats** – battery percentage, CPU usage, memory usage.
- **Power management** – shutdown, restart, cancel shutdown, lock screen.
- **Media controls** – volume up/down, mute/unmute.
- **Screen capture** – take a screenshot instantly.
- **App launcher** – open Notepad, Calculator, Paint, Chrome, VS Code, CMD, and more.

### 🌐 Web Automation & Productivity
- **Open websites** – YouTube, GitHub, LinkedIn, Netflix, Spotify, Gmail, etc.
- **Search** – Google and YouTube search by voice.
- **Real‑time weather** – get temperature and conditions for any city.
- **Top news headlines** – fetched live.
- **Reminders & notes** – save and retrieve them locally (JSON).
- **Built‑in calculator** – evaluate expressions like "calculate 15% of 200".
- **Entertainment** – tell a joke, give a motivational quote.

### 🎨 Premium UI/UX
- **Dynamic voice orb** – glows and pulses when listening.
- **Particle background** – a subtle, animated particle system for a modern look.
- **Always listening** – after a single click, ECHO listens continuously for the wake word **"Hey Echo"**. No need to click every time.
- **Sidebar with all commands** – searchable, categorized list of 50+ commands.
- **Quick command chips** – click any example to execute it immediately.
- **Responsive design** – works on desktop and mobile (touch‑friendly).

---

## 🛠️ Tech Stack

| Layer       | Technologies |
|-------------|--------------|
| **Backend** | Python, Flask, Psutil, PyAutoGUI, Requests, BeautifulSoup |
| **Frontend**| HTML5, CSS3 (Vanilla), JavaScript, Web Speech API |
| **APIs**    | Gemini 2.0 (optional), Wikipedia, OpenWeatherMap (optional), NewsAPI (optional) |

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** (3.10+ recommended)
- **Windows** (for system control features like lock, shutdown, app launcher; other OS have limited system commands)
- A **working microphone** and a modern browser (Chrome or Edge recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone (https://github.com/ankush826921-crypto/HexSoftwares-ECHO-AI-Voice-Assistant)
   cd ECHO-AI-Assistant
