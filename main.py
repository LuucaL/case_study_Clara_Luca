import streamlit as st

# --- Login-System ---
def login():
    st.write("## Login")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Anmelden"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("Eingeloggt als " + username)
        else:
            st.error("Falscher Benutzername oder Passwort.")

# --- Reservierungsverwaltung ---
def reservation_management(device_name):
    st.write(f"## Reservierungsverwaltung für {device_name}")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen", "Löschen"])

    if action == "Anzeigen":
        st.info("Keine Reservierungen vorhanden.")
    elif action == "Hinzufügen":
        user = st.text_input("Reserviert von")
        if st.button("Hinzufügen"):
            date = st.date_input("Reservierungsdatum")
            st.success(f"Reservierung für {device_name} von {user} hinzugefügt.")
    elif action == "Löschen":
        st.warning("Keine Reservierungen zu löschen.")

# --- Wartungsverwaltung ---
def maintenance_management(device_name):
    st.write(f"## Wartungsverwaltung für {device_name}")
    action = st.radio("Aktion auswählen", ["Anzeigen", "Hinzufügen"])

    if action == "Anzeigen":
        st.info("Keine Wartungspläne vorhanden.")
    elif action == "Hinzufügen":
        date = st.date_input("Wartungsdatum")
        notes = st.text_area("Notizen")
        if st.button("Hinzufügen"):
            st.success(f"Wartungsplan für {device_name} am {date} hinzugefügt.")

def logout():
    if st.button("Logout", type="primary"):
        st.session_state["logged_in"] = False

# --- Haupt-App ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "selected_device" not in st.session_state:
    st.session_state["selected_device"] = None

if not st.session_state["logged_in"]:
    login()
else:
    st.write("# Gerätemanagement")

    if st.session_state["selected_device"] is None:
        st.write("## Geräteauswahl")
        # Lokale Variable zum Auswählen des Geräts
        selected = st.selectbox('Gerät auswählen', ["Gerät_A", "Gerät_B"])
        if st.button("Gerät bestätigen"):
            st.session_state["selected_device"] = selected
            st.success(f"Gerät {st.session_state['selected_device']} ausgewählt.")
        logout()
    else:
        st.write(f"Das ausgewählte Gerät ist {st.session_state['selected_device']}")

        # Button für Gerätewechsel
        if st.button("Gerät wechseln"):
            st.session_state["selected_device"] = None
            st.info("Gerät wurde zurückgesetzt. Bitte wählen Sie ein neues Gerät aus.")
            # Ändere die Query-Parameter, um einen Reload anzustoßen
            st.experimental_set_query_params(reset="true")
            st.stop()  # Stoppt den aktuellen Durchlauf hier

        # Bereichsauswahl ohne Gerätewechsel
        section = st.radio("Bereich auswählen", ["Reservierungsverwaltung", "Wartungsverwaltung"])
        
        if section == "Reservierungsverwaltung":
            reservation_management(st.session_state["selected_device"])
        elif section == "Wartungsverwaltung":
            maintenance_management(st.session_state["selected_device"])
        
        logout()
