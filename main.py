import json
import streamlit as st
from users import User
from devices import Device
from reservation import add_reservation, get_reservations
from maintenance import add_maintenance, get_maintenance, calculate_maintenance_costs
from tinydb import TinyDB

# Initialisierung der Datenbank
DB_PATH = "database.json"

def initialize_database():
    db = TinyDB(DB_PATH)

    if not db.table("devices").all():
        db.table("devices").insert_multiple([
            {"device_name": "Device1", "managed_by_user_id": "one@mci.edu", "is_active": True},
            {"device_name": "Device2", "managed_by_user_id": "two@mci.edu", "is_active": True}
        ])

    if not db.table("users").all():
        db.table("users").insert_multiple([
            {"id": "martina@mci.edu", "name": "Martina"}
        ])

    if not db.table("reservations").all():
        db.table("reservations").insert_multiple([
            {"user_id": "1", "device_id": "Device1", "reservation_date": "2025-01-29"}
        ])

    if not db.table("maintenance").all():
        db.table("maintenance").insert_multiple([])


initialize_database()

# Benutzerverwaltung
def user_management():
    st.write("## Benutzerverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen", "Löschen"], key="user_action")

    if action == "Anzeigen":
        users = User.find_all()
        if users:
            for user in users:
                st.write(user)
        else:
            st.info("Keine Benutzer vorhanden.")

    elif action == "Hinzufügen":
        name = st.text_input("Name")
        email = st.text_input("E-Mail")
        if st.button("Benutzer hinzufügen"):
            new_user = User(email, name)
            new_user.store_data()
            st.success(f"Benutzer {name} hinzugefügt.")

    elif action == "Löschen":
        email = st.text_input("E-Mail des zu löschenden Benutzers")
        if st.button("Benutzer löschen"):
            user = User.find_by_attribute("id", email)
            if user:
                user.delete()
                st.success(f"Benutzer {email} gelöscht.")
            else:
                st.error("Benutzer nicht gefunden.")

# Geräteverwaltung
def device_management():
    st.write("## Geräteverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen/ Bearbeiten", "Löschen"], key="device_action")


    if action == "Anzeigen":
        devices = Device.find_all()
        if devices:
            for device in devices:
                st.write(f"Gerät: {device.device_name}, Verantwortlich: {device.managed_by_user_id}")
        else:
            st.info("Keine Geräte vorhanden.")

    elif action == "Hinzufügen/ Bearbeiten":
        name = st.text_input("Gerätename")
        manager_email = st.text_input("E-Mail des Verantwortlichen")
        if st.button("Gerät speichern"):
            user = User.find_by_attribute("id", manager_email)
            if user:
                new_device = Device(name, manager_email)
                new_device.store_data()
                st.success(f"Gerät {name} gespeichert.")
            else:
                st.error("Verantwortlicher Benutzer nicht gefunden.")

    elif action == "Löschen":
        name = st.text_input("Name des zu löschenden Geräts")
        if st.button("Gerät löschen"):
            device = Device.find_by_attribute("device_name", name)
            if device:
                device.delete()
                st.success(f"Gerät {name} gelöscht.")
            else:
                st.error("Gerät nicht gefunden.")

# Wartungsverwaltung
def maintenance_management():
    st.write("## Wartungsverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen"], key="maintenance_action")


    devices = Device.find_all()
    device_options = {device.device_name: device for device in devices}

    if not device_options:
        st.warning("Keine Geräte verfügbar.")
        return

    selected_device_name = st.selectbox("Gerät auswählen", options=list(device_options.keys()))
    selected_device = device_options[selected_device_name]

    if action == "Anzeigen":
        maintenance_schedule = get_maintenance(selected_device.device_name)
        if maintenance_schedule:
            st.write("Wartungsplan:")
            for mnt in maintenance_schedule:
                st.write(f"Datum: {mnt['maintenance_date']}, Kosten: {mnt['cost']}, Notizen: {mnt['notes']}")
        else:
            st.info("Keine Wartungen vorhanden.")
    elif action == "Hinzufügen":
        maintenance_date = st.date_input("Wartungsdatum")
        cost = st.number_input("Kosten", min_value=0.0)
        notes = st.text_area("Notizen")
        if st.button("Wartung hinzufügen"):
            result = add_maintenance(selected_device.device_name, maintenance_date.strftime("%Y-%m-%d"), cost, notes)
            st.success(result)


# Reservierungsverwaltung
def reservation_management():
    st.write("## Reservierungsverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen"], key="reservation_action")



    devices = Device.find_all()
    device_options = {device.device_name: device for device in devices}

    if not device_options:
        st.warning("Keine Geräte verfügbar.")
        return

    selected_device_name = st.selectbox("Gerät auswählen", options=list(device_options.keys()))
    selected_device = device_options[selected_device_name]

    if action == "Anzeigen":
        reservations = get_reservations(selected_device.device_name)
        if reservations:
            st.write("Reservierungen:")
            for res in reservations:
                st.write(f"Nutzer: {res['user_id']}, Datum: {res['reservation_date']}")
        else:
            st.info("Keine Reservierungen vorhanden.")
    elif action == "Hinzufügen":
        user_id = st.text_input("Nutzer-ID")
        reservation_date = st.date_input("Reservierungsdatum")
        if st.button("Reservierung hinzufügen"):
            result = add_reservation(user_id, selected_device.device_name, reservation_date.strftime("%Y-%m-%d"))
            st.success(result)

# Wartungsverwaltung
    st.write("## Wartungsverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen"])

    devices = Device.find_all()
    device_options = {device.device_name: device for device in devices}

    if not device_options:
        st.warning("Keine Geräte verfügbar.")
        return

    selected_device_name = st.selectbox("Gerät auswählen", options=list(device_options.keys()))
    selected_device = device_options[selected_device_name]

    if action == "Anzeigen":
        maintenance_schedule = get_maintenance(selected_device.device_name)
        if maintenance_schedule:
            st.write("Wartungsplan:")
            for mnt in maintenance_schedule:
                st.write(f"Datum: {mnt['maintenance_date']}, Kosten: {mnt['cost']}, Notizen: {mnt['notes']}")
        else:
            st.info("Keine Wartungen vorhanden.")
    elif action == "Hinzufügen":
        maintenance_date = st.date_input("Wartungsdatum")
        cost = st.number_input("Kosten", min_value=0.0)
        notes = st.text_area("Notizen")
        if st.button("Wartung hinzufügen"):
            result = add_maintenance(selected_device.device_name, maintenance_date.strftime("%Y-%m-%d"), cost, notes)
            st.success(result)
    st.write("## Wartungsverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen"])

    devices = Device.find_all()
    device_options = {device.device_name: device for device in devices}

    if not device_options:
        st.warning("Keine Geräte verfügbar.")
        return

    selected_device_name = st.selectbox("Gerät auswählen", options=list(device_options.keys()))
    selected_device = device_options[selected_device_name]

    if action == "Anzeigen":
        maintenance_schedule = get_maintenance(selected_device.device_name)
        if maintenance_schedule:
            st.write("Wartungsplan:")
            for mnt in maintenance_schedule:
                st.write(f"Datum: {mnt['maintenance_date']}, Kosten: {mnt['cost']}, Notizen: {mnt['notes']}")
        else:
            st.info("Keine Wartungen vorhanden.")
    elif action == "Hinzufügen":
        maintenance_date = st.date_input("Wartungsdatum")
        cost = st.number_input("Kosten", min_value=0.0)
        notes = st.text_area("Notizen")
        if st.button("Wartung hinzufügen"):
            result = add_maintenance(selected_device.device_name, maintenance_date.strftime("%Y-%m-%d"), cost, notes)
            st.success(result)


# Haupt-App
st.title("Verwaltungssystem")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.write("## Login")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    if st.button("Anmelden"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("Erfolgreich eingeloggt.")
        else:
            st.error("Falscher Benutzername oder Passwort.")
else:
    section = st.radio("Bereich auswählen", ["Benutzerverwaltung", "Geräteverwaltung", "Reservierungsverwaltung", "Wartungsverwaltung"])
    
    if section == "Benutzerverwaltung":
        user_management()
    elif section == "Geräteverwaltung":
        device_management()
    elif section == "Reservierungsverwaltung":
        reservation_management()
    elif section == "Wartungsverwaltung":
        maintenance_management()
    
    if st.button("Logout"):
        st.session_state["logged_in"] = False
