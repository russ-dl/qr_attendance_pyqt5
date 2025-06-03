import os
import json
import hashlib

USER_DB = "data/users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, 'w') as f:
            json.dump({}, f)
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f, indent=4)

def login_user(username, password):
    users = load_users()
    user = users.get(username)
    if user and user["password"] == hash_password(password):
        return user
    return None

def signup_user(username, password, role):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    save_users(users)
    return True
