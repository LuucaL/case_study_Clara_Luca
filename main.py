import streamlit as st

# --- Login-System ---
def login():
    st.write("## Login")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Anmelden"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("Erfolgreich eingeloggt!")
        else:
            st.error("Falscher Benutzername oder Passwort.")

# --- Reservierungsverwaltung ---
def reservation_management():
    st.write("## Reservierungsverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen", "Löschen"])

    if action == "Anzeigen":
        st.info("Keine Reservierungen vorhanden. (Daten werden nicht gespeichert)")
    elif action == "Hinzufügen":
        device_name = st.text_input("Gerätename")
        user = st.text_input("Reserviert von")
        if st.button("Hinzufügen"):
            st.success(f"Reservierung für {device_name} von {user} hinzugefügt. (Nicht gespeichert)")
    elif action == "Löschen":
        st.warning("Keine Reservierungen zu löschen. (Daten werden nicht gespeichert)")

# --- Wartungsverwaltung ---
def maintenance_management():
    st.write("## Wartungsverwaltung")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen"])

    if action == "Anzeigen":
        st.info("Keine Wartungspläne vorhanden. (Daten werden nicht gespeichert)")
    elif action == "Hinzufügen":
        device_name = st.text_input("Gerätename")
        date = st.date_input("Wartungsdatum")
        notes = st.text_area("Notizen")
        if st.button("Hinzufügen"):
            st.success(f"Wartungsplan für {device_name} am {date} hinzugefügt. (Nicht gespeichert)")

# --- Haupt-App ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    st.write("# Gerätemanagement")
    section = st.radio("Bereich auswählen", ["Geräteauswahl", "Reservierungsverwaltung", "Wartungsverwaltung"])

    if section == "Geräteauswahl":
        current_device = st.selectbox(label='Gerät auswählen', options=["Gerät_A", "Gerät_B"])
        st.write(f"Das ausgewählte Gerät ist {current_device}")
    elif section == "Reservierungsverwaltung":
        reservation_management()
    elif section == "Wartungsverwaltung":
        maintenance_management()