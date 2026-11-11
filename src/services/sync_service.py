import os
import json

PENDING_SYNC_FILE = "data/pending_sync.json"

def _ensure_valid_json():
    os.makedirs(os.path.dirname(PENDING_SYNC_FILE), exist_ok=True)
    if not os.path.exists(PENDING_SYNC_FILE) or os.path.getsize(PENDING_SYNC_FILE) == 0:
        with open(PENDING_SYNC_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def add_offline_queue(transaccion):
    _ensure_valid_json()
    try:
        with open(PENDING_SYNC_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []
        
    data.append(transaccion)
    with open(PENDING_SYNC_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def sync_pending_transactions():
    _ensure_valid_json()
    try:
        with open(PENDING_SYNC_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []
        
    count = len(data)
    # Sobrescribir siempre con una lista vacía válida tras sincronizar
    with open(PENDING_SYNC_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)
        
    return (count > 0), count