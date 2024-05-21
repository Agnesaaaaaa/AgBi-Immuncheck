import streamlit as st
import pandas as pd
from datetime import date
from github_contents import GithubContents
import binascii
import bcrypt


st.markdown(
    """
<h1 style='color: white;'>AgBi-Immuncheck - Digitaler Impfpass</h1>
    """,
    unsafe_allow_html=True
)

DATA_FILE = "Immucheck.csv"
DATA_COLUMNS = ["username", "Datum der Impfung", "Impfstoff/Wirkstoff", "Symptome", "Nachimpfungsdatum"]

LOGIN_DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS_LOGIN = ['username', 'name', 'password']

def eintrag_hinzufuegen():
    st.header('Impfungen')
    with st.form(key="entry_form"):
        impfdatum = st.date_input("Datum der Impfung", format="DD.MM.YYYY")
        impfstoff = st.text_input("Impfstoff/Wirkstoff", placeholder="Art der Impfung oder Impfstoff")
        symptome = st.text_input("Symptome", placeholder="Beschreiben Sie die Symptome")
        nachimpfungsdatum = st.date_input("Nachimpfungsdatum", format="DD.MM.YYYY")
        submit_button = st.form_submit_button("Eintrag hinzufügen")
        if submit_button:
            if impfdatum and impfstoff and symptome and nachimpfungsdatum:
                new_entry = {
                    DATA_COLUMNS[0]: st.session_state['username'],
                    DATA_COLUMNS[1]: impfdatum,
                    DATA_COLUMNS[2]: impfstoff,
                    DATA_COLUMNS[3]: symptome,
                    DATA_COLUMNS[4]: nachimpfungsdatum
                }
                if 'df' in st.session_state:
                    new_df = pd.DataFrame([new_entry])
                    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                    try:
                        st.session_state.df.to_csv(DATA_FILE, index=False)
                        st.success("Neuer Eintrag erfolgreich hinzugefügt!")
                    except Exception as e:
                        st.error(f"Fehler beim Speichern der Daten: {e}")
                else:
                    st.error("DataFrame ist nicht initialisiert.")
            else:
                st.warning("Bitte füllen Sie alle Felder aus, bevor Sie einen Eintrag hinzufügen.")
    datenausgabe()

def datenausgabe():
    if 'df' in st.session_state and not st.session_state.df.empty:
        if 'username' not in st.session_state.df.columns:
            st.error("DataFrame hat keine Spalte 'username'.")
            return
        user_df = st.session_state.df[st.session_state.df['username'] == st.session_state['username']]
        if not user_df.empty:
            st.subheader("Ihre aktuellen Impfungen:")
            st.dataframe(user_df.drop(columns=['username']))
        else:
            st.warning("Es sind keine Einträge vorhanden.")
    else:
        st.warning("Es sind keine Einträge vorhanden.")

def daten_initialisieren():
    if 'df' not in st.session_state:
        try:
            df = pd.read_csv(DATA_FILE)
            if 'username' not in df.columns:
                df['username'] = ""
            st.session_state.df = df
        except FileNotFoundError:
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def login_seite():
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authentifizieren(username, password)

def registrierung_seite():
    st.title("Registrieren")
    with st.form(key='register_form'):
        new_username = st.text_input("Neuer Benutzername")
        new_name = st.text_input("Name")
        new_password = st.text_input("Neues Passwort", type="password")
        if st.form_submit_button("Registrieren"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
            hashed_password_hex = binascii.hexlify(hashed_password).decode()
            if new_username in st.session_state.df_users['username'].values:
                st.error("Benutzername existiert bereits. Bitte wählen Sie einen anderen.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS_LOGIN)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                st.session_state.github.write_df(LOGIN_DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registrierung erfolgreich! Sie können sich jetzt einloggen.")

def authentifizieren(username, password):
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)
    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['username'] = username
            st.session_state['authentication'] = True
            st.success('Login erfolgreich')
            st.experimental_rerun()
        else:
            st.error('Falsches Passwort')
    else:
        st.error('Benutzername nicht gefunden')

def github_initialisieren():
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"]
        )
        print("github initialisiert")


def main():
    github_initialisieren()
    # Weitere Logik hier...

if __name__ == "__main__":
    main()






    
def anmeldeinformationen_initialisieren():
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(LOGIN_DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(LOGIN_DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS_LOGIN)







def hauptseite():
    st.header("Willkommen zu AgBi-Immuncheck")
    st.write("""
    Unsere App AgBi- Immuncheck bietet eine benutzerfreundliche Plattform zur Erfassung und Verwaltung von Impfungen sowie zur Überwachung von Symptomen im Zusammenhang mit den Impfungen. Entwickelt für Einzelpersonen, ermöglicht unsere Anwendung eine einfache und sichere Verwaltung von Impfdaten und Gesundheitsinformationen.

    Benutzer können ihre Impfungen in der App erfassen, einschließlich des Impfstoffs, des Datums und des Impforts. Dies bietet eine zentrale und leicht zugängliche Aufzeichnung aller erhaltenen Impfungen. Die App ermöglicht es den Benutzern, Profile anzulegen und personenbezogene Informationen wie Name, Geburtsdatum und medizinische Vorgeschichte zu speichern. Dies ermöglicht eine individuelle Anpassung der Impf- und Gesundheitsverwaltung.
    """)
    st.write("Teilen Sie uns Ihre Erfahrungen mit!")
    
    # Feedback-Formular
    feedback_text = st.text_area("Geben Sie Ihr Feedback ein", height=150)
    rating = st.slider("Bewerten Sie Ihre Erfahrung", min_value=1, max_value=5, step=1)
    submit_button = st.button("Feedback absenden")
    
    # Feedback absenden
    if submit_button:
        # Speichern des Feedbacks in einer CSV-Datei oder Datenbank
        save_feedback(feedback_text, rating)
        st.success("Vielen Dank für Ihr Feedback!")
        
import pandas as pd
import os

# Funktion zum Speichern des Feedbacks
def save_feedback(feedback_text, rating):
    feedback_df = pd.DataFrame({"Feedback": [feedback_text], "Bewertung": [rating]})
    feedback_df.to_csv("feedback.csv", mode='a', header=not os.path.exists("feedback.csv"), index=False)

import streamlit as st
import pandas as pd
import os
import binascii

PROFILE_DATA_FILE = "profile_data.csv"

def profil_seite():
    st.title("Mein Profil")

    
    if 'profile' not in st.session_state:
        st.session_state.profile = {}

    
    if 'profile_image' not in st.session_state:
        st.session_state.profile_image = None

    # Daten aus CSV-Datei laden
    if os.path.exists(PROFILE_DATA_FILE):
        profile_df = pd.read_csv(PROFILE_DATA_FILE)
        profile_dict = profile_df.set_index('username').T.to_dict()
        st.session_state.profile = profile_dict.get(st.session_state['username'], {})
    else:
        profile_df = pd.DataFrame(columns=['username', 'name', 'geburtsdatum', 'hausarzt', 'allergien', 'medikamente', 'profile_image'])

    # Profilinformationen anzeigen
    if st.session_state.profile:
        st.subheader("Gespeicherte Profilinformationen")
        for key, value in st.session_state.profile.items():
            if key != 'profile_image':
                st.write(f"**{key.capitalize()}:** {value}")



    # Expander für Profil bearbeiten
    with st.expander("Profil bearbeiten", expanded=True):
        # Profilbild hochladen oder anzeigen
        profilbild = st.file_uploader("Profilfoto hochladen", type=["jpg", "jpeg", "png"], key="profile_image_upload")
        if profilbild:
            st.session_state.profile_image = profilbild.getvalue()
        elif 'profile_image' in st.session_state.profile:
            st.session_state.profile_image = binascii.unhexlify(st.session_state.profile['profile_image'])

        if st.session_state.profile_image:
            st.image(st.session_state.profile_image, caption="Profilfoto", width=200)

        # Name eingeben
        name = st.text_input("Name", value=st.session_state.profile.get('name', ''), key="profile_name")

        # Geburtsdatum eingeben
        geburtsdatum = st.text_input("Geburtsdatum (TT.MM.JJJJ)", value=st.session_state.profile.get('geburtsdatum', ''), key="profile_birthdate")
        if geburtsdatum:
            try:
                geburtsjahr = int(geburtsdatum.split(".")[2])
                if geburtsjahr > 2014:
                    st.warning("Das Geburtsjahr muss vor 2014 liegen.")
            except (IndexError, ValueError):
                st.error("Bitte geben Sie das Geburtsdatum im Format TT.MM.JJJJ ein.")

        # Hausarzt eingeben
        hausarzt = st.text_input("Hausarzt", value=st.session_state.profile.get('hausarzt', ''), key="profile_doctor")

        # Allergien eingeben
        allergien = st.text_area("Allergien", value=st.session_state.profile.get('allergien', ''), key="profile_allergies")

        # Medikamente eingeben
        medikamente = st.text_area("Medikamente", value=st.session_state.profile.get('medikamente', ''), key="profile_medications")

        # Speichern-Button
        if st.button("Speichern"):
            st.session_state.profile = {
                "username": st.session_state['username'],
                "name": name,
                "geburtsdatum": geburtsdatum,
                "hausarzt": hausarzt,
                "allergien": allergien,
                "medikamente": medikamente,
                "profile_image": binascii.hexlify(st.session_state.profile_image).decode() if st.session_state.profile_image else ''
            }

            # Überprüfen, ob der Benutzer bereits im DataFrame existiert
            if st.session_state['username'] in profile_df['username'].values:
                # Aktualisieren Sie die vorhandenen Daten
                profile_df.loc[profile_df['username'] == st.session_state['username']] = st.session_state.profile
            else:
                # Fügen Sie neue Daten hinzu
                profile_df = pd.concat([profile_df, pd.DataFrame([st.session_state.profile])], ignore_index=True)

            profile_df.to_csv(PROFILE_DATA_FILE, index=False)
            st.success("Profil erfolgreich aktualisiert")


def impfungen_seite():
    eintrag_hinzufuegen()

# Empfehlungslink
    st.markdown("[Weitere Informationen zu Impfstoffen nach Krankheiten geordnet](https://www.infovac.ch/de/impfungen/impfstoffe-nach-krankheiten-geordnet)")



def main():
    github_initialisieren()
    anmeldeinformationen_initialisieren()

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        optionen = st.sidebar.selectbox("Seite auswählen", ["Login", "Registrieren"])
        if optionen == "Login":
            login_seite()
        elif optionen == "Registrieren":
            registrierung_seite()
    else:
        daten_initialisieren()
        seiten = {
            "Dashboard": hauptseite,
            "Profil": profil_seite,
            "Impfungen": impfungen_seite
        }
        st.sidebar.header("Navigation")
        seite = st.sidebar.selectbox("Seite auswählen", list(seiten.keys()))
        seiten[seite]()

        st.sidebar.header("Profil")
        if st.sidebar.button("Logout"):
            st.session_state['authentication'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()

def feedback_form():
    st.write("Teilen Sie uns Ihre Erfahrungen mit!")

    import matplotlib.pyplot as plt
