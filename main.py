import streamlit as st
from users import User
from devices import Device

# --- User Management ---
def user_management():
    st.write("## Benutzerverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen", "Löschen"])

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

# --- Device Management ---
def device_management():
    st.write("## Geräteverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen/ Bearbeiten", "Löschen"])

    if action == "Anzeigen":
        devices = Device.find_all()
        if devices:
            for device in devices:
                st.write(device)
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

# --- Main Application ---
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
    st.write("# Verwaltungssystem")
    section = st.radio("Bereich auswählen", ["Benutzerverwaltung", "Geräteverwaltung"])
    if section == "Benutzerverwaltung":
        user_management()
    elif section == "Geräteverwaltung":
        device_management()

    if st.button("Logout"):
        st.session_state["logged_in"] = False

