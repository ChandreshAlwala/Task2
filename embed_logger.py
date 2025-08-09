import json
import uuid
import os
from utils import encrypt_data, decrypt_data

LOG_FILE = "embedding_log.secure"

def log_embedding(data):
    log_entry = {
        "session_id": str(uuid.uuid4()),
        "user_id": data["user_id"],
        "platform": data["platform"],
        "timestamp": data["timestamp"],
        "embedding": data["embedding"]
    }
    encrypted = encrypt_data(json.dumps(log_entry).encode())

    with open(LOG_FILE, "ab") as f:
        f.write(encrypted + b"\n")

def read_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'rb') as f:
        lines = f.readlines()
        return [json.loads(decrypt_data(line.strip()).decode()) for line in lines]

def secure_delete():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
