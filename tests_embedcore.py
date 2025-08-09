from embedcore_v2 import embed_message, generate_embedding
from obfuscator import obfuscate, deobfuscate
from keystore import get_key

def test_same_key_same_output():
    msg = input("enter a message: ")
    uid = input("Enter your user id: ")
    platform = input("Platform: ")
    key = get_key(uid, platform)
    e1 = obfuscate(generate_embedding(msg), key)
    e2 = obfuscate(generate_embedding(msg), key)
    assert e1 == e2

def test_different_keys():
    msg = "Secure test"
    e1 = obfuscate(generate_embedding(msg), get_key("userA", "email"))
    e2 = obfuscate(generate_embedding(msg), get_key("userB", "chat"))
    assert e1 != e2

def test_reverse():
    msg = "Hello"
    uid = "user123"
    platform = "web"
    key = get_key(uid, platform)
    original = generate_embedding(msg)
    obf = obfuscate(original, key)
    rev = deobfuscate(obf, key)
    assert all(abs(a - b) < 1e-5 for a, b in zip(original, rev))

if __name__ == "__main__":
    test_same_key_same_output()
    test_different_keys()
    test_reverse()
    print("All tests passed ✅")
