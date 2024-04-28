import streamlit as st
import pandas as pd
 
st.set_page_config(layout="wide", page_title="Agbi-Immuncheck - Digitaler Impfpass", page_icon=":syringe:", 
                    initial_sidebar_state="expanded")
 

st.markdown(
    """
<h1 style='color: black;'>Agbi-Immuncheck - Digitaler Impfpass</h1>
    """
    , unsafe_allow_html=True)
 
@st.cache
def load_data():
    return pd.DataFrame(columns=['Kategorie', 'Datum', 'Information'])
 
data = load_data()
 
# Benutzeroberfläche für Hinzufügen von Impfdaten
category = st.sidebar.selectbox('Kategorie wählen', ['Impfungen', 'Symptome', 'Schweizerischer Impfplan, Profil'])


if category == 'Impfungen':
    st.header('Impfungen')
    # Hier können Sie die Benutzeroberfläche für Impfungen anzeigen und verwalten
    date = st.date_input('Datum der Impfung')
    info = st.text_input('Informationen zur Impfung')
    if st.button('Impfung hinzufügen'):
        data = data.append({'Kategorie': category, 'Datum': date, 'Information': info}, ignore_index=True)
        st.success('Impfung erfolgreich hinzugefügt!')
 
elif category == 'Symptome':
    st.header('Symptome')
 
elif category == 'Schweizerischer Impfplan':
    st.header('Schweizerischer Impfplan')
    
 




