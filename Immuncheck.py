import streamlit as st
import pandas as pd

# Titel der App
st.title('Agbi-Immuncheck - Digitaler Impfpass')

# Datenframe für Impfdaten erstellen oder laden, falls vorhanden
@st.cache
def load_data():
    return pd.DataFrame(columns=['Kategorie', 'Datum', 'Information'])

data = load_data()

# Benutzeroberfläche für Hinzufügen von Impfdaten
st.header('Impfdaten hinzufügen')

category = st.selectbox('Kategorie wählen', ['Meine Impfungen', 'Symptome', 'Schweizerischer Impfplan'])
date_of_event = st.date_input('Datum', value=pd.Timestamp.today())
information = st.text_input('Information')

if st.button('Eintrag hinzufügen'):
    data = data.append({'Kategorie': category, 'Datum': date_of_event, 'Information': information}, ignore_index=True)
    st.success('Eintrag erfolgreich hinzugefügt!')

# Benutzeroberfläche für Anzeigen von Impfdaten
st.header('Gespeicherte Daten')
st.dataframe(data)

