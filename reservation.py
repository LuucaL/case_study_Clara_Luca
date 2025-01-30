import json
from datetime import datetime

DB_PATH = "database.json"

# Reservierungsklasse
def add_reservation(user_id, device_id, reservation_date):
    with open(DB_PATH, "r") as file:
        database = json.load(file)

    if "reservations" not in database:
        database["reservations"] = []
    
    # Prüfen, ob das Gerät bereits reserviert ist
    for res in database["reservations"]:
        if res["device_id"] == device_id and res["reservation_date"] == reservation_date:
            return "Gerät ist bereits für dieses Datum reserviert."
    
    # Neue Reservierung hinzufügen
    database["reservations"].append({
        "user_id": user_id,
        "device_id": device_id,
        "reservation_date": reservation_date
    })
    
    with open(DB_PATH, "w") as file:
        json.dump(database, file, indent=4)
    
    return "Reservierung erfolgreich hinzugefügt."

# Anzeigen der Reservierungen
def get_reservations(device_id):
    with open(DB_PATH, "r") as file:
        database = json.load(file)

    # Sicherstellen, dass "reservations" als Liste gespeichert wird
    if not isinstance(database.get("reservations"), list):
        database["reservations"] = list(database["reservations"].values())

    return [res for res in database["reservations"] if res["device_id"] == device_id]
