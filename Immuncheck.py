
import streamlit as st
import datetime
from datetime import date
import pandas as pd
from github_contents import GithubContents

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

st.set_page_config(layout="wide", page_title="Agbi-Immuncheck - Digitaler Impfpass", page_icon=":syringe:", 
                    initial_sidebar_state="expanded")
 
st.markdown(
    """
<h1 style='color: white;'>AgBi-Immuncheck - Digitaler Impfpass</h1>
    """
    , unsafe_allow_html=True)

category = st.sidebar.selectbox('Kategorie wählen', ['Impfungen','Schweizerischer Impfplan'])

DATA_FILE = "Immucheck.csv"
DATA_COLUMNS = ["Datum der Impfung", "Impfstoff/Wirkstoff", "Symptome"]

def add_entry():
    """Fügt einen neuen Eintrag in den DataFrame hinzu und ermöglicht die Verwaltung der Benutzeroberfläche für Impfungen."""
    st.header('Impfungen')
    
    with st.form(key="entry_form"):
        impfdatum = st.date_input("Datum der Impfung", format="DD.MM.YYYY")
        impfstoff = st.text_input("Impfstoff/Wirkstoff", placeholder="Art der Impfung oder Impfstoff")
        symptome = st.text_input("Symptome", placeholder="Beschreiben Sie die Symptome")
        
        submit_button = st.form_submit_button("Eintrag hinzufügen")
        
        if submit_button:
            # Überprüfen, ob alle Felder ausgefüllt sind
            if impfdatum and impfstoff and symptome:
                new_entry = {
                    DATA_COLUMNS[0]: impfdatum,
                    DATA_COLUMNS[1]: impfstoff,
                    DATA_COLUMNS[2]: symptome,
                }
                
                # Überprüfen Sie, ob der DataFrame in der Sitzung vorhanden ist
                if 'df' in st.session_state:
                    # Erstellen Sie einen DataFrame für den neuen Eintrag
                    new_df = pd.DataFrame([new_entry])
                    
                    # Fügen Sie den neuen Eintrag zum vorhandenen DataFrame hinzu
                    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                    
                    # Speichern Sie den aktualisierten DataFrame in der CSV-Datei
                    try:
                        st.session_state.df.to_csv(DATA_FILE, index=False)
                        st.success("Neuer Eintrag erfolgreich hinzugefügt!")
                    except Exception as e:
                        st.error(f"Fehler beim Speichern der Daten: {e}")
                else:
                    st.error("DataFrame ist nicht initialisiert.")
            else:
                st.warning("Bitte füllen Sie alle Felder aus, bevor Sie einen Eintrag hinzufügen.")
                
    # Anzeige des DataFrame
    display_dataframe()

def display_dataframe():
    """Zeigt den aktuellen DataFrame in der Streamlit-Anwendung an."""
    if 'df' in st.session_state and not st.session_state.df.empty:
        st.subheader("Aktuelle Impfungen:")
        st.dataframe(st.session_state.df)
    else:
        st.warning("Es sind keine Einträge vorhanden.")

# Initialisieren Sie die Daten (DataFrame) in der Sitzung
def init_data():
    if 'df' not in st.session_state:
        try:
            st.session_state.df = pd.read_csv(DATA_FILE)
        except FileNotFoundError:
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

# Rufen Sie die Initialisierungsfunktion auf, bevor Sie den Eintrag hinzufügen
init_data()
add_entry()





