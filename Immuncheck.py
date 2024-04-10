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


<div class="waveWrapper waveAnimation">
  <div class="waveWrapperInner bgTop">
    <div class="wave waveTop" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-top.png')"></div>
  </div>
  <div class="waveWrapperInner bgMiddle">
    <div class="wave waveMiddle" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-mid.png')"></div>
  </div>
  <div class="waveWrapperInner bgBottom">
    <div class="wave waveBottom" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-bot.png')"></div>
  </div>
</div>




