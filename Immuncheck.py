import streamlit as st
import pandas as pd

# Setzen der Streamlit-Themeneinstellungen
st.set_page_config(layout="wide", page_title="Agbi-Immuncheck - Digitaler Impfpass", page_icon=":syringe:", 
                    initial_sidebar_state="expanded")

# Titel der App
st.title('Agbi-Immuncheck - Digitaler Impfpass')

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
elif category == 'Symptome':
    st.header('Symptome')
    # Hier können Sie die Benutzeroberfläche für Symptome anzeigen und verwalten
elif category == 'Schweizerischer Impfplan':
    st.header('Schweizerischer Impfplan')
    # Hier können Sie den schweizerischen Impfplan anzeigen

# Benutzeroberfläche für Anzeigen von Impfdaten
st.header('Gespeicherte Daten')
st.dataframe(data)

import streamlit as st

def sidebar_bg():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(to bottom, #4d88ff, #0066cc);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

sidebar_bg()

import streamlit as st

def main_bg():
    st.markdown(
        """
        <style>
        body {
            background-color: #f2f7ff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

main_bg()

preset_colors: list[tuple[str, ThemeColor]] = [
    ("Default light", ThemeColor(
            primaryColor="#ff4b4b",
            backgroundColor="#ffffff",
            secondaryBackgroundColor="#f0f2f6",
            textColor="#31333F",
        )),
    ("Default dark", ThemeColor(
            primaryColor="#ff4b4b",
            backgroundColor="#0e1117",
            secondaryBackgroundColor="#262730",
            textColor="#fafafa",
    ))
]



