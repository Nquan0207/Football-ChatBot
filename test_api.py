# test_api.py
# -------------
# Single‑file Gemini 2.5 Pro chat test.
#
# 1) pip install --upgrade google-genai
# 2) Replace YOUR_KEY_HERE below
# 3) python test_api.py

import os
from google import genai

# ── 1) Set your key here ───────────────────────────────────────────────────────
os.environ["GEMINI_API_KEY"] = "AIzaSyBu5OFcTMhqZ9LI2HpgW7OuC_ws2Wxe6v8"
# ──────────────────────────────────────────────────────────────────────────────

def main():
    # ── 2) Initialize client (auto‑reads GEMINI_API_KEY) ─────────────────────────
    client = genai.Client()
    # ────────────────────────────────────────────────────────────────────────────

    # ── 3A) One‑shot text generation ─────────────────────────────────────────────
    one_shot = client.models.generate_content(
        model="gemini-2.5-pro",
        contents="Say hello in Spanish."
    )
    print("One‑shot response:", one_shot.text)
    # ────────────────────────────────────────────────────────────────────────────

    # ── 3B) Multi‑turn chat session ──────────────────────────────────────────────
    chat = client.chats.create(model="gemini-2.5-pro")
    chat_response = chat.send_message("Say hello in French.")
    print("Chat response:", chat_response.text)
    # ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
