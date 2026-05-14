// Particle background (same as before)
function createParticles() {
    const container = document.getElementById('particles');
    if (!container) return;
    for (let i = 0; i < 60; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = `rgba(100, 150, 255, ${Math.random() * 0.3 + 0.1})`;
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `floatParticle ${Math.random() * 15 + 10}s linear infinite`;
        particle.style.filter = 'blur(1px)';
        container.appendChild(particle);
    }
}
const particleStyle = document.createElement('style');
particleStyle.textContent = `
    @keyframes floatParticle {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
        20% { opacity: 0.8; }
        80% { opacity: 0.6; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
`;
document.head.appendChild(particleStyle);

// ---------- Voice Assistant (Continuous, Wake Word "Hey Echo") ----------
let recognition = null;
let isListening = false;
let wakeWord = "hey echo";
let wakeDetected = false;
let waveInterval = null;

let chatHistory = [];
let apiKey = localStorage.getItem('gemini_api_key') || "";

const orb = document.getElementById('orb');
const statusDiv = document.getElementById('status');
const responseDiv = document.getElementById('responseText');
const enableBtn = document.getElementById('enableVoiceBtn');

function animateVoiceWaves(active) {
    const waves = document.querySelectorAll('.wave');
    if (active) {
        if (waveInterval) clearInterval(waveInterval);
        waveInterval = setInterval(() => {
            waves.forEach(w => w.style.height = Math.floor(Math.random() * 20 + 5) + 'px');
        }, 100);
    } else {
        clearInterval(waveInterval);
        waves.forEach(w => w.style.height = '10px');
    }
}

function startContinuousListening() {
    if (!recognition) return;
    try {
        recognition.start();
        isListening = true;
        orb.classList.add('listening');
        animateVoiceWaves(true);
        statusDiv.innerText = "🎤 Always listening for 'Hey Echo'...";
    } catch(e) {
        statusDiv.innerText = "Microphone error. Refresh page.";
    }
}

function stopListening() {
    if (recognition) recognition.stop();
    isListening = false;
    orb.classList.remove('listening');
    animateVoiceWaves(false);
}

function initSpeech() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        statusDiv.innerText = "Browser not supported. Use Chrome or Edge.";
        return false;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    recognition.onstart = () => {
        // Already handled in startContinuousListening
    };
    
    recognition.onresult = (event) => {
        let interim = "";
        let final = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript.toLowerCase();
            if (event.results[i].isFinal) final += transcript + " ";
            else interim += transcript;
        }
        if (interim) statusDiv.innerText = `👂 Hearing: ${interim.substring(0, 40)}...`;
        
        if (final.trim()) {
            statusDiv.innerText = `👂 Heard: ${final}`;
            sendCommand(final.trim());
        }
    };
    
    recognition.onerror = (event) => {
        console.error(event.error);
        statusDiv.innerText = `Error: ${event.error}. Try enabling again.`;
        isListening = false;
        orb.classList.remove('listening');
        animateVoiceWaves(false);
    };
    
    recognition.onend = () => {
        if (isListening) {
            // Restart automatically if still supposed to be listening
            recognition.start();
        }
    };
    return true;
}

async function sendCommand(text) {
    if (!text) return;
    statusDiv.innerText = "⚡ Processing command...";
    responseDiv.innerText = "🤔 Thinking...";
    orb.classList.add('processing');
    try {
        const res = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, api_key: apiKey, history: chatHistory })
        });
        const data = await res.json();
        
        chatHistory.push({ role: "user", text: text });
        chatHistory.push({ role: "model", text: data.response });
        if (chatHistory.length > 20) chatHistory = chatHistory.slice(-20);
        
        const widgetContainer = document.getElementById('widgetContainer');
        if (data.widget) {
            widgetContainer.innerHTML = data.widget;
            widgetContainer.classList.add('show-widget');
        } else {
            widgetContainer.innerHTML = "";
            widgetContainer.classList.remove('show-widget');
        }
        
        // Futuristic Typewriter Effect
        typeText(responseDiv, data.response);
        
        // Speak response
        const utterance = new SpeechSynthesisUtterance(data.response);
        utterance.lang = 'en-US';
        utterance.rate = 0.95;
        
        utterance.onend = () => {
            orb.classList.remove('processing');
            statusDiv.innerText = "🎤 Listening for next command...";
        };
        
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    } catch (err) {
        orb.classList.remove('processing');
        responseDiv.innerText = "Server error. Is backend running?";
        statusDiv.innerText = "Connection error";
    }
}

// Enable voice on button click (one time)
enableBtn.addEventListener('click', () => {
    if (!recognition) {
        if (!initSpeech()) return;
    }
    if (isListening) {
        stopListening();
        enableBtn.innerText = "🎤 Start Voice Listening";
    } else {
        startContinuousListening();
        enableBtn.innerText = "🔴 Listening...";
    }
});

// ---------- Futuristic Animations ----------

// 1. Typewriter Effect
let typeTimeout = null;
function typeText(element, text, speed = 25) {
    if (typeTimeout) clearTimeout(typeTimeout);
    let i = 0;
    element.innerHTML = '<span class="typed-text"></span><span class="cursor"></span>';
    const textSpan = element.querySelector('.typed-text');
    
    function type() {
        if (i < text.length) {
            textSpan.innerHTML += text.charAt(i);
            i++;
            typeTimeout = setTimeout(type, speed);
        }
    }
    type();
}

// 2. Dynamic Mouse Tracking Glow (Torch Effect)
const glow = document.createElement('div');
glow.className = 'mouse-glow';
document.body.appendChild(glow);

window.addEventListener('mousemove', (e) => {
    // using absolute page coordinates
    glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
});

// 3. 3D Tilt Hover Effect
function addTiltEffect(el) {
    el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const xPct = (x / rect.width - 0.5) * 2;
        const yPct = (y / rect.height - 0.5) * 2;
        el.style.transform = `perspective(500px) rotateX(${-yPct * 15}deg) rotateY(${xPct * 15}deg) scale(1.05)`;
        el.style.boxShadow = `${-xPct * 10}px ${-yPct * 10}px 15px rgba(76,140,255,0.4)`;
        el.style.background = `rgba(100, 150, 255, 0.4)`;
    });
    el.addEventListener('mouseleave', () => {
        el.style.transform = `perspective(500px) rotateX(0) rotateY(0) scale(1)`;
        el.style.boxShadow = `none`;
        el.style.background = `rgba(255, 255, 255, 0.08)`;
        el.style.transition = `0.3s all ease`;
    });
    el.addEventListener('mouseenter', () => {
        el.style.transition = `none`; 
    });
}

// ---------- Sidebar and Command Grid (same as before) ----------
const sidebar = document.getElementById('sidebar');
const openSidebarBtn = document.getElementById('openSidebarBtn');
const closeSidebarBtn = document.getElementById('closeSidebarBtn');
const cmdSearch = document.getElementById('cmdSearch');
const commandsListDiv = document.getElementById('commandsList');

const allCommands = {
    "Time & Date": ["What's the time?", "Today's date"],
    "Web & Search": ["Open YouTube", "Open Google", "Search Python tutorial", "Play songs on YouTube", "News headlines"],
    "Productivity": ["Set reminder call mom", "Take note buy milk", "Show reminders", "Read notes"],
    "System": ["Take screenshot", "Lock screen", "Shutdown computer", "Restart", "Cancel shutdown", "Volume up", "Volume down", "Mute", "Unmute", "Battery status", "CPU usage", "Memory usage"],
    "Apps": ["Open notepad", "Open calculator", "Open paint", "Open chrome", "Close chrome"],
    "Entertainment": ["Tell me a joke", "Give me a quote"],
    "AI & Utility": ["Calculate 144/12", "Weather in London", "Ask AI what is Python?"],
    "Exit": ["Exit"]
};

function buildCommandsList(filter = "") {
    commandsListDiv.innerHTML = "";
    for (const [category, cmds] of Object.entries(allCommands)) {
        const filtered = cmds.filter(cmd => cmd.toLowerCase().includes(filter.toLowerCase()));
        if (filtered.length === 0) continue;
        const catDiv = document.createElement('div');
        catDiv.className = 'command-category';
        catDiv.innerHTML = `<h4>${category}</h4>`;
        filtered.forEach(cmd => {
            const item = document.createElement('div');
            item.className = 'command-item';
            item.innerText = cmd;
            item.addEventListener('click', () => {
                sendCommand(cmd);
                if (window.innerWidth < 600) sidebar.classList.remove('open');
            });
            catDiv.appendChild(item);
        });
        commandsListDiv.appendChild(catDiv);
    }
}

openSidebarBtn.addEventListener('click', () => sidebar.classList.add('open'));
closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));
cmdSearch.addEventListener('input', (e) => buildCommandsList(e.target.value));

// Quick command chips
const quickGrid = document.getElementById('quickCmdGrid');
const quickSample = ["What's the time?", "Open YouTube", "Search Python", "Take note test", "Tell me a joke", "Lock screen", "Volume up", "Battery status"];
quickSample.forEach(cmd => {
    const chip = document.createElement('div');
    chip.className = 'cmd-chip';
    chip.innerText = cmd;
    chip.addEventListener('click', () => sendCommand(cmd));
    addTiltEffect(chip); // Apply 3D tilt animation to each chip
    quickGrid.appendChild(chip);
});

// Initialize
window.addEventListener('load', () => {
    createParticles();
    initSpeech(); // prepare recognition, but don't start yet
    buildCommandsList();
    statusDiv.innerText = "Click 'Start Voice Listening' and allow microphone, then speak a command.";
});

// Settings Modal Logic
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const saveApiBtn = document.getElementById('saveApiBtn');
const apiKeyInput = document.getElementById('apiKeyInput');

if (settingsBtn) {
    settingsBtn.addEventListener('click', () => {
        apiKeyInput.value = apiKey;
        settingsModal.style.display = 'flex';
    });
    closeModalBtn.addEventListener('click', () => settingsModal.style.display = 'none');
    saveApiBtn.addEventListener('click', () => {
        apiKey = apiKeyInput.value.trim();
        localStorage.setItem('gemini_api_key', apiKey);
        settingsModal.style.display = 'none';
        statusDiv.innerText = "API Key saved! AI memory activated.";
    });
}