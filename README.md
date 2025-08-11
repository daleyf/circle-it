# circle-it
CircleQ — circle → answer (MVP)
Seamless, no-chat UI for instant explanations. Hit a hotkey, draw a quick circle around anything on screen, and get a crisp answer bubble powered by your LLM (OpenAI/Ollama/etc). Logs include the exact prompt/response for full transparency.


Why
Chat windows slow you down. CircleQ is a “point & ask” overlay for frictionless Q/A—perfect for docs, code, PDFs, dashboards.

Features
Hotkey summon: overlay pops up anywhere.

Circle capture: lasso a region; we OCR it automatically.

Instant answer bubble: short, on-screen response (no chat thread).

Transparency: saves prompt/response, tokens, model & cost (JSONL).

Private by default: works with local models via Ollama; cloud via API key.

Quickstart
Requirements
macOS (Apple Silicon) or Linux (Wayland/X11). Windows experimental.

Python 3.10+

Tesseract OCR

macOS: brew install tesseract

Ubuntu: sudo apt-get install tesseract-ocr

(Optional) Ollama for local models: curl -fsSL https://ollama.com/install.sh | sh

Install
bash
Copy
Edit
git clone https://github.com/yourname/circleq.git
cd circleq
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
Configure .env
bash
Copy
Edit
# choose one provider
PROVIDER=openai          # or: ollama
MODEL_NAME=gpt-4o-mini   # or: llama3.2:3b-instruct (ollama), etc.

# openai-style keys (only needed for cloud use)
OPENAI_API_KEY=sk-...

# behavior
HOTKEY=ctrl+alt+c
ANSWER_MAX_TOKENS=256
LOG_DIR=./logs
Run
bash
Copy
Edit
python app.py
You’ll see a tray icon. Press your hotkey (default Ctrl+Alt+C / macOS ⌘⌥C) to summon the overlay.

Usage
Press the hotkey → greyed overlay appears.

Click–drag a circle around text/UI you want explained.

CircleQ screenshots + OCRs the region, builds a prompt, and queries your model.

An answer bubble appears next to your circle.

Enter to copy text.

Esc to dismiss.

Hold hotkey again and re-circle to ask a follow-up on a new region.

Tip: If OCR misses math/code, zoom in before circling.

Transparency & Privacy
Every interaction logs a JSONL entry with:

region hash, extracted text, system/user prompt, model, tokens, latency, (cost if cloud).

No screenshots are persisted by default (configurable TTL).

With Ollama, nothing leaves your device.

How it works (brief)
scss
Copy
Edit
Hotkey → Overlay → Region Screenshot → OCR (Tesseract)
     → Prompt Builder (system + extracted text + brief instructions)
     → LLM Provider (OpenAI or Ollama)
     → On-screen Answer Bubble
     → JSONL audit log (fully reproducible)
Keyboard Shortcuts
Summon overlay: Ctrl+Alt+C (Linux/Win) / ⌘⌥C (macOS)

Confirm circle: release mouse

Copy answer: Enter

Dismiss: Esc

Example logs (redacted)
json
Copy
Edit
{"ts":"2025-08-11T23:02:12Z","provider":"ollama","model":"llama3.2:3b-instruct",
 "text":"NumPy broadcasting: shapes (3,1) vs (1,4)...",
 "system":"You are a concise explainer. Prefer step-by-step, max 6 lines.",
 "user":"Explain the selected snippet clearly and briefly.",
 "tokens_in":274,"tokens_out":142,"latency_ms":812,"cost_usd":0.0000}
Roadmap
 Better math/code OCR (Vision APIs)

 Inline citations from source page

 Multi-region capture (sequence of circles)

 Small tooltip follow-ups (no chat thread)

 Windows overlay polish

Troubleshooting
No text extracted → Ensure Tesseract installed; zoom in; increase contrast.

Hotkey conflict → Change HOTKEY in .env.

Slow answers → Use a smaller model or local Ollama model.

Nothing happens on hotkey → App must be focused once after launch (OS security).

Dev Notes
Minimal stack: Python + PySide6 (overlay), pynput (hotkeys), mss (screenshot), pytesseract (OCR).

Providers: tiny shim with two drivers (openai, ollama). Easy to add others.

License
MIT. Build cool, respectful things.

Credits
Built with love for frictionless learning. PRs welcome.
