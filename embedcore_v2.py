import hashlib
import datetime
from keystore import get_key
from obfuscator import obfuscate

def generate_embedding(message):
    h = hashlib.sha256(message.encode()).digest()
    return [b / 255.0 for b in h[:32]]

def embed_message(message, user_id, platform):
    original = generate_embedding(message)
    key = get_key(user_id, platform)
    obf = obfuscate(original, key)
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "embedding": obf,
        "user_id": user_id,
        "platform": platform,
        "timestamp": timestamp
    }
