# # test_api.py

# import os

# from google import genai


# # ── 1) Set your key here ───────────────────────────────────────────────────────
# os.environ["GEMINI_API_KEY"] = "AIzaSyBu5OFcTMhqZ9LI2HpgW7OuC_ws2Wxe6v8"
# # ──────────────────────────────────────────────────────────────────────────────

# def main():
#     # ── 2) Initialize client ────────────────────────────────────────────────────
#     client = genai.Client()
#     # ───────────────────────────────────────────────────────────────────────────

#     # ── 3A) One-shot text generation ────────────────────────────────────────────
#     one_shot = client.models.generate_content(
#         model="gemini-2.5-pro",
#         contents="Say hello in Vietnamese."
#     )
#     print("One‑shot response:", one_shot.text)

#     # ── 3B) Multi-turn chat session ─────────────────────────────────────────────
#     chat = client.chats.create(model="gemini-2.5-pro")
#     chat_response = chat.send_message("Say hello in Vietnamese.")
#     print("Chat response:", chat_response.text)
#     # ───────────────────────────────────────────────────────────────────────────

# if __name__ == "__main__":
#     main()
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone

# Load .env from current directory
load_dotenv()

# Primary values
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB")
# Optional separate user/pass override (handles special characters safely)
mongo_user = os.getenv("MONGO_USER")
mongo_pass = os.getenv("MONGO_PASS")

if not mongo_uri:
    raise RuntimeError("MONGO_URI not set in .env")

# Connect
client = MongoClient(mongo_uri, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas successfully.")
    db = client[mongo_db_name]
    coll = db["test_chat"]

    # Insert a test document
    doc = {
        "session_id": "test_session",
        "role": "userr",
        "content": "Testing .env connection",
        "timestamp": datetime.now(timezone.utc)
    }
    result = coll.insert_one(doc)
    print("Inserted document ID:", result.inserted_id)

    # Read it back
    fetched = coll.find_one({"session_id": "env_test_session"})
    print("Fetched document:", fetched)

except Exception as e:
    print("Connection or operation failed:", e)
