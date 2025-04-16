from firebase_admin import db

def get_all_users():
    ref = db.reference("users")
    users = ref.get()
    if not users:
        return []
    return [{**data, "uid": uid} for uid, data in users.items()]

def get_pending_users():
    return [u for u in get_all_users() if u.get("status") == "pending"]

def approve_user(uid):
    ref = db.reference(f"users/{uid}")
    ref.update({"status": "approved"})

def reject_user(uid):
    ref = db.reference(f"users/{uid}")
    ref.update({"status": "rejected"})

def update_user(uid, updates: dict):
    ref = db.reference(f"users/{uid}")
    ref.update(updates)
