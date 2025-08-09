from cryptography.fernet import Fernet
import os

KEY_FILE = "aes_key.key"

def generate_aes_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_aes_key():
    if not os.path.exists(KEY_FILE):
        return generate_aes_key()
    with open(KEY_FILE, 'rb') as f:
        return f.read()

def encrypt_data(data: bytes) -> bytes:
    key = load_aes_key()
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    key = load_aes_key()
    f = Fernet(key)
    return f.decrypt(token)
