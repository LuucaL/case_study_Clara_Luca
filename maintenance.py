import json
from datetime import datetime

DB_PATH = "database.json"

# Wartungsmanagement
def add_maintenance(device_id, maintenance_date, cost, notes=""):
    with open(DB_PATH, "r") as file:
        database = json.load(file)
    
    # Neue Wartung hinzufügen
    database["maintenance"].append({
        "device_id": device_id,
        "maintenance_date": maintenance_date,
        "cost": cost,
        "notes": notes
    })
    
    with open(DB_PATH, "w") as file:
        json.dump(database, file, indent=4)
    
    return "Wartung erfolgreich hinzugefügt."

# Anzeigen der Wartungen
def get_maintenance(device_id):
    with open(DB_PATH, "r") as file:
        database = json.load(file)
    
    return [mnt for mnt in database["maintenance"] if mnt["device_id"] == device_id]

# Berechnung der Wartungskosten pro Quartal
def calculate_maintenance_costs():
    with open(DB_PATH, "r") as file:
        database = json.load(file)
    
    maintenance_costs = {}
    for entry in database["maintenance"]:
        quarter = (datetime.strptime(entry["maintenance_date"], "%Y-%m-%d").month - 1) // 3 + 1
        year = datetime.strptime(entry["maintenance_date"], "%Y-%m-%d").year
        key = f"Q{quarter}-{year}"
        maintenance_costs[key] = maintenance_costs.get(key, 0) + entry["cost"]
    
    return maintenance_costs
