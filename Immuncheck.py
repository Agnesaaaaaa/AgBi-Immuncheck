import streamlit as st
import pandas as pd

# Setzen der Streamlit-Themeneinstellungen
st.set_page_config(layout="wide", page_title="Agbi-Immuncheck - Digitaler Impfpass", page_icon=":syringe:", 
                    initial_sidebar_state="expanded")

# Titel der App
st.markdown(
    """
    <h1 style='color: black;'>Agbi-Immuncheck - Digitaler Impfpass</h1>
    """
    , unsafe_allow_html=True)

# Datenframe für Impfdaten erstellen oder laden, falls vorhanden
@st.cache
def load_data():
    return pd.DataFrame(columns=['Kategorie', 'Datum', 'Information'])

data = load_data()

# Benutzeroberfläche für Hinzufügen von Impfdaten
category = st.sidebar.selectbox('Kategorie wählen', ['Meine Impfungen', 'Symptome', 'Schweizerischer Impfplan'])

if category == 'Meine Impfungen':
    st.header('Meine Impfungen')
    # Hier können Sie die Benutzeroberfläche für Impfungen anzeigen und verwalten
    date = st.date_input('Datum der Impfung')
    info = st.text_input('Informationen zur Impfung')
    if st.button('Impfung hinzufügen'):
        data = data.append({'Kategorie': category, 'Datum': date, 'Information': info}, ignore_index=True)
        st.success('Impfung erfolgreich hinzugefügt!')

elif category == 'Symptome':
    st.header('Symptome')
    # Hier können Sie die Benutzeroberfläche für Symptome anzeigen und verwalten

elif category == 'Schweizerischer Impfplan':
    st.header('Schweizerischer Impfplan')
    # Hier können Sie den schweizerischen Impfplan anzeigen

# Benutzeroberfläche für Anzeigen von Impfdaten
st.header('Gespeicherte Daten')
st.dataframe(data)

def main_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f2f7ff !important;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

main_bg()

def sidebar_bg():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: white !important;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

sidebar_bg()

try:
    if st.button('Impfung hinzufügen'):
        data = data.append({'Kategorie': category, 'Datum': date, 'Information': info}, ignore_index=True)
        st.success('Impfung erfolgreich hinzugefügt!')
except Exception as e:
    st.error(f"Fehler beim Hinzufügen der Impfung: {e}")


# Set constants
DATA_FILE = "MyContactsTable.csv"
DATA_COLUMNS = ["Name", "Strasse", "PLZ", "Ort", "Geburtsdatum"]
 
# Set page configuration
st.set_page_config(page_title="My Contacts", page_icon="🎂", layout="wide",  
                   initial_sidebar_state="expanded")
 
def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
 
def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)
 
def add_entry_in_sidebar():
    """Add a new entry to the DataFrame using pd.concat and calculate age."""
    new_entry = {
        DATA_COLUMNS[0]:  st.sidebar.text_input(DATA_COLUMNS[0]),  # Name
        DATA_COLUMNS[1]:  st.sidebar.text_input(DATA_COLUMNS[1]),  # Strasse
        DATA_COLUMNS[2]:  st.sidebar.text_input(DATA_COLUMNS[2]),  # PLZ
        DATA_COLUMNS[3]:  st.sidebar.text_input(DATA_COLUMNS[3]),  # Ort
        DATA_COLUMNS[4]:  st.sidebar.date_input(DATA_COLUMNS[4],
                                                min_value=date(1950, 1, 1),
                                                format="DD.MM.YYYY"),  # Geburtsdatum
    }
 
    # check wether all data is defined, otherwise show an error message
    for key, value in new_entry.items():
        if value == "":
            st.sidebar.error(f"Bitte ergänze das Feld '{key}'")
            return
 
    if st.sidebar.button("Add"):
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)
 
        # Save the updated DataFrame to GitHub
        name = new_entry[DATA_COLUMNS[0]]
        msg = f"Add contact '{name}' to the file {DATA_FILE}"
        st.session_state.github.write_df(DATA_FILE, st.session_state.df, msg)
 
def display_dataframe():
    """Display the DataFrame in the app."""
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("No data to display.")
 

