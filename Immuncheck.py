import streamlit as st
import pandas as pd

# Setzen der Streamlit-Themeneinstellungen
st.set_page_config(layout="wide", page_title="Agbi-Immuncheck - Digitaler Impfpass", page_icon=":syringe:", 
                    initial_sidebar_state="expanded")

# Titel der App
st.markdown("""
    <style>
        .css-17eq0hr {
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

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

