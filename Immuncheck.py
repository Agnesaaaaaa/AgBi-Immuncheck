import streamlit as st
import pandas as pd
from datetime import date
import bcrypt
import binascii
from github_contents import GithubContents  # Stellen Sie sicher, dass dieses Modul in requirements.txt ist

st.markdown(
    """
<h1 style='color: white;'>AgBi-Immuncheck - Digitaler Impfpass</h1>
    """,
    unsafe_allow_html=True
)

DATA_FILE = "Immucheck.csv"
DATA_COLUMNS = ["username", "Datum der Impfung", "Impfstoff/Wirkstoff", "Symptome"]

LOGIN_DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS_LOGIN = ['username', 'name', 'password']

def add_entry():
    """Fügt einen neuen Eintrag in den DataFrame hinzu und ermöglicht die Verwaltung der Benutzeroberfläche für Impfungen."""
    st.header('Impfungen')
    
    with st.form(key="entry_form"):
        impfdatum = st.date_input("Datum der Impfung", format="DD.MM.YYYY")
        impfstoff = st.text_input("Impfstoff/Wirkstoff", placeholder="Art der Impfung oder Impfstoff")
        symptome = st.text_input("Symptome", placeholder="Beschreiben Sie die Symptome")
        
        submit_button = st.form_submit_button("Eintrag hinzufügen")
        
        if submit_button:
            if impfdatum and impfstoff and symptome:
                new_entry = {
                    DATA_COLUMNS[0]: st.session_state['username'],  # Eintrag mit dem angemeldeten Benutzer verknüpfen
                    DATA_COLUMNS[1]: impfdatum,
                    DATA_COLUMNS[2]: impfstoff,
                    DATA_COLUMNS[3]: symptome,
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
                
    display_dataframe()

def display_dataframe():
    """Zeigt den aktuellen DataFrame in der Streamlit-Anwendung an."""
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

def init_data():
    if 'df' not in st.session_state:
        try:
            df = pd.read_csv(DATA_FILE)
            if 'username' not in df.columns:
                df['username'] = ""  # Füge die Spalte 'username' hinzu, falls sie nicht existiert
            st.session_state.df = df
        except FileNotFoundError:
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def login_page():
    """Login für bestehende Benutzer."""
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def register_page():
    """Registrierung eines neuen Benutzers."""
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())  # Passwort hashen
            hashed_password_hex = binascii.hexlify(hashed_password).decode()  # Hash in hexadezimale Zeichenfolge umwandeln
            
            # Überprüfen, ob der Benutzername bereits existiert
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS_LOGIN)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Aktualisierten DataFrame in das GitHub-Datenrepository schreiben
                st.session_state.github.write_df(LOGIN_DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """Authentifizierungsstatus initialisieren."""
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)  # Hex in Bytes umwandeln
        
        # Überprüfen des eingegebenen Passworts
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['username'] = username
            st.session_state['authentication'] = True
            st.success('Login erfolgreich')
            st.experimental_rerun()
        else:
            st.error('Falsches Passwort')
    else:
        st.error('Benutzername nicht gefunden')

def init_github():
    """Initialisiert das GithubContents-Objekt."""
    if 'github' not in st.session_state:
        try:
            st.session_state.github = GithubContents(
                st.secrets["github"]["owner"],
                st.secrets["github"]["repo"],
                st.secrets["github"]["token"]
            )
            print("github initialized")
        except KeyError as e:
            st.error(f"Fehlende Geheimnisse: {e}")
            return
    
def init_credentials():
    """Initialisiert oder lädt den DataFrame."""
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(LOGIN_DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(LOGIN_DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS_LOGIN)

def main():
    init_github()  # Initialisiert das GithubContents-Objekt
    init_credentials()  # Lädt die Anmeldedaten aus dem GitHub-Datenrepository

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Seite auswählen", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()
    else:
        init_data()  # Initialisiert die Daten für angemeldete Benutzer
        add_entry()

        st.sidebar.header("Profil")
        st.sidebar.write("Verwalten Sie Ihr persönliches Profil, einschließlich Name, Geburtsdatum und medizinischer Vorgeschichte.")

        profile_image = st.sidebar.file_uploader("Profilfoto hochladen", type=["jpg", "jpeg", "png"])
        name = st.sidebar.text_input("Name", placeholder="Ihr Name")
        birthdate = st.sidebar


