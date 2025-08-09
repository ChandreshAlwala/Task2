import sqlite3
import hashlib
import os
import json
import datetime

DB_PATH = "keystore.db"
JSON_PATH = "keystore.json"

# === DB INITIALIZATION ===
def init_keystore():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS keys (
        user_id TEXT PRIMARY KEY,
        key TEXT,
        platform TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

init_keystore()

# === JSON SUPPORT ===
def load_json_keystore():
    if not os.path.exists(JSON_PATH):
        return {}
    with open(JSON_PATH, "r") as f:
        return json.load(f)

def save_json_keystore(keystore):
    with open(JSON_PATH, "w") as f:
        json.dump(keystore, f, indent=4)

# === KEY GENERATION ===
def generate_key(user_id, platform):
    salt = os.urandom(16)
    key_bytes = hashlib.sha256(user_id.encode() + salt).digest()
    key_hex = key_bytes.hex()
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # Store in SQLite DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO keys (user_id, key, platform, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, key_hex, platform, timestamp))
    conn.commit()
    conn.close()

    # Store in JSON
    keystore = load_json_keystore()
    keystore[user_id] = {
        "key": key_hex,
        "platform": platform,
        "timestamp": timestamp
    }
    save_json_keystore(keystore)

    print(f"[INFO] Generated and stored key for {user_id} (Platform: {platform}, Timestamp: {timestamp})")
    return key_hex

# === KEY RETRIEVAL ===
def get_key(user_id, platform=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT key, platform, timestamp FROM keys WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        print(f"[INFO] Retrieved key for {user_id} from DB (Platform: {row[1]}, Timestamp: {row[2]})")
        return row[0]

    keystore = load_json_keystore()
    if user_id in keystore:
        key_info = keystore[user_id]
        print(f"[INFO] Retrieved key for {user_id} from JSON. Syncing to DB...")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO keys (user_id, key, platform, timestamp) VALUES (?, ?, ?, ?)",
                  (user_id, key_info["key"], key_info["platform"], key_info["timestamp"]))
        conn.commit()
        conn.close()
        return key_info["key"]

    if not platform:
        raise ValueError("Platform must be provided for new key generation.")
    print(f"[WARN] Key not found for {user_id}. Generating new key...")
    return generate_key(user_id, platform)

