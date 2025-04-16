from firebase_admin import db

def load_projects():
    ref = db.reference("projects")
    projects_data = ref.get()

    if not projects_data:
        return ["ZAS4"]

    return [proj.get("name") for proj in projects_data.values() if "name" in proj]

def get_all_project_dicts():
    """Returns list of all projects as dicts with name/location/remark"""
    ref = db.reference("projects")
    data = ref.get()
    if not data:
        return []
    return list(data.values())

def add_project(name, location, remark):
    ref = db.reference("projects")
    ref.push({
        "name": name,
        "location": location,
        "remark": remark
    })
