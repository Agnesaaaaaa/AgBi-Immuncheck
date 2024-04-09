import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

# Titel der App
st.title('Agbi-Immuncheck - Digitaler Impfpass')

# Datenframe für Impfdaten erstellen oder laden, falls vorhanden
@st.cache
def load_data():
    return pd.DataFrame(columns=['Datum der Impfung', 'Impfstoff'])

data = load_data()

# Benutzeroberfläche für Hinzufügen von Impfdaten
st.header('Impfdaten hinzufügen')
date_of_vaccination = st.date_input('Datum der Impfung', value=pd.Timestamp.today())
vaccine_type = st.text_input('Impfstoff')

if st.button('Impfdaten hinzufügen'):
    data = data.append({'Datum der Impfung': date_of_vaccination, 'Impfstoff': vaccine_type}, ignore_index=True)
    st.success('Impfdaten erfolgreich hinzugefügt!')

# Benutzeroberfläche für Anzeigen von Impfdaten
st.header('Gespeicherte Impfdaten')
st.dataframe(data)
