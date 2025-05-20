import json
import hashlib
from datetime import datetime

# Chemin vers le fichier JSON
DB_PATH = "data/db.json"

def hash_password(password):
    """Hacher un mot de passe avec SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def read_db():
    """Lire la base de données JSON."""
    try:
        with open(DB_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def write_db(data):
    """Écrire dans la base de données JSON."""
    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4)

def get_user(username):
    """Récupérer les informations d'un utilisateur."""
    db = read_db()
    return db.get(username, None)

def set_user(username, password):
    """Créer ou mettre à jour un utilisateur."""
    db = read_db()
    if username not in db:
        db[username] = {
            "username": username,
            "password": hash_password(password),  # Stocker le mot de passe haché
            "highscore": 999999,
            "history": {}
        }
    write_db(db)

def update_highscore(username, score):
    """Mettre à jour le highscore d'un utilisateur."""
    db = read_db()
    if username in db:
        db[username]["highscore"] = score
        write_db(db)

def add_score_to_history(username, score, time, competitive=False):
    """Ajouter un score à l'historique d'un utilisateur."""
    db = read_db()
    if username in db:
        timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M")
        db[username]["history"][timestamp] = {
            "score": score,
            "time": time,
            "competitive": competitive
        }
        write_db(db)

def get_highscore(username):
    """Récupérer le highscore d'un utilisateur."""
    user = get_user(username)
    if user:
        return user.get("highscore", 0)
    return None

def get_history(username):
    """Récupérer l'historique des scores d'un utilisateur."""
    user = get_user(username)
    if user:
        return user.get("history", {})
    return None

def get_top_users(limit=10):
    """Récupérer les meilleurs utilisateurs par highscore."""
    db = read_db()
    sorted_users = sorted(db.items(), key=lambda x: x[1]["highscore"], reverse=True)
    return sorted_users[:limit]