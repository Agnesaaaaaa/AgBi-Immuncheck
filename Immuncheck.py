import streamlit as st
import datetime
from datetime import date
import pandas as pd
from github_contents import GithubContents

# Set constants
DATA_FILE = "imuTable.csv"
DATA_COLUMNS = ["Datum der Impfung", "Informationen zur Impfung"]

# Set page configuration
st.set_page_config(page_title="AgBi-Immuncheck", layout="wide",  
                   initial_sidebar_state="expanded")


def init_github():
    """Initialisieren Sie das GithubContents-Objekt."""
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
        DATA_COLUMNS[0]:  st.sidebar.text_input(DATA_COLUMNS[0]),  # Datum der Impfung
        DATA_COLUMNS[1]:  st.sidebar.text_input(DATA_COLUMNS[1]),  # Informationen zur Impfung
        DATA_COLUMNS[2]:  st.sidebar.date_input(DATA_COLUMNS[2],
                                                min_value=date(1950, 1, 1),
                                                format="DD.MM.YYYY"),  # Geburtsdatum
    } 

    if len(DATA_COLUMNS) > 2:
        new_entry[DATA_COLUMNS[2]] = st.sidebar.date_input(
            DATA_COLUMNS[2],
            min_value=date(1950, 1, 1),
            format="DD.MM.YYYY"
        )
 


