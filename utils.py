import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()
