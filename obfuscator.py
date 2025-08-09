import numpy as np
import hashlib

def seed_from_key(key):
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % (10**8)

def obfuscate(embedding, key):
    rng = np.random.default_rng(seed_from_key(key))
    noise = rng.normal(0, 0.01, size=len(embedding))
    return np.round(np.array(embedding) + noise, 6).tolist()

def deobfuscate(obf_embedding, key):
    rng = np.random.default_rng(seed_from_key(key))
    noise = rng.normal(0, 0.01, size=len(obf_embedding))
    return np.round(np.array(obf_embedding) - noise, 6).tolist()
