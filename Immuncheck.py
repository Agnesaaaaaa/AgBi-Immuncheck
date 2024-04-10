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


def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )








