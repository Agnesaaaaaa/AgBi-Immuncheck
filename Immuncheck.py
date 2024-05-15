import streamlit as st
import pandas as pd
from datetime import date
from github_contents import GithubContents
import binascii
import streamlit as st
import pandas as pd
from github_contents import GithubContents
import bcrypt


st.markdown(
    """
<h1 style='color: white;'>AgBi-Immuncheck - Digitaler Impfpass</h1>
    """
    , unsafe_allow_html=True)

category = st.sidebar.selectbox('Kategorie wählen', ['Impfungen','Schweizerischer Impfplan'])

DATA_FILE = "Immucheck.csv"
DATA_COLUMNS = ["Datum der Impfung", "Impfstoff/Wirkstoff", "Symptome"]

DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS_LOGIN = ['username', 'name', 'password']
def add_entry():
    """Fügt einen neuen Eintrag in den DataFrame hinzu und ermöglicht die Verwaltung der Benutzeroberfläche für Impfungen."""
    st.header('Impfungen')
    
    with st.form(key="entry_form"):
        impfdatum = st.date_input("Datum der Impfung", format="DD.MM.YYYY")
        impfstoff = st.text_input("Impfstoff/Wirkstoff", placeholder="Art der Impfung oder Impfstoff")
        symptome = st.text_input("Symptome", placeholder="Beschreiben Sie die Symptome")
        
        submit_button = st.form_submit_button("Eintrag hinzufügen")
        
        if submit_button:
           
            if impfdatum and impfstoff and symptome:
                new_entry = {
                    DATA_COLUMNS[0]: impfdatum,
                    DATA_COLUMNS[1]: impfstoff,
                    DATA_COLUMNS[2]: symptome,
                }
                
               
                if 'df' in st.session_state:
                   
                    new_df = pd.DataFrame([new_entry])
                    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                    try:
                        st.session_state.df.to_csv(DATA_FILE, index=False)
                        st.success("Neuer Eintrag erfolgreich hinzugefügt!")
                    except Exception as e:
                        st.error(f"Fehler beim Speichern der Daten: {e}")
                else:
                    st.error("DataFrame ist nicht initialisiert.")
            else:
                st.warning("Bitte füllen Sie alle Felder aus, bevor Sie einen Eintrag hinzufügen.")
                
  
    display_dataframe()

def display_dataframe():
    """Zeigt den aktuellen DataFrame in der Streamlit-Anwendung an."""
    if 'df' in st.session_state and not st.session_state.df.empty:
        st.subheader("Aktuelle Impfungen:")
        st.dataframe(st.session_state.df)
    else:
        st.warning("Es sind keine Einträge vorhanden.")


def init_data():
    if 'df' not in st.session_state:
        try:
            st.session_state.df = pd.read_csv(DATA_FILE)
        except FileNotFoundError:
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)


def login_page():
    """ Login an existing user. """
    st.title("Login")
    with st.form(key='login_form'):
        st.session_state['username'] = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(st.session_state.username, password)

def register_page():
    """ Register a new user. """
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()) # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode() # Convert hash to hexadecimal string
            
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS_LOGIN)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """ 
    Initialize the authentication status.

    Parameters:
    username (str): The username to authenticate.
    password (str): The password to authenticate.    
    """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password) # convert hex to bytes
        
        # Check the input password
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.success('Login successful')
            st.rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        print("github initialized")
    
def init_credentials():
    """Initialize or load the dataframe."""
    if 'df_users' in st.session_state:
        pass

    if st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS_LOGIN)


def main():
    init_github() # Initialize the GithubContents object
    init_credentials() # Loads the credentials from the Github data repositor

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()

    else:
        #replace the code bellow with your own code or switch to another page
        # Rufen Sie die Initialisierungsfunktion auf, bevor Sie den Eintrag hinzufügen

        init_data()
        add_entry()
        st.sidebar.header("Profil")

        st.sidebar.write("Verwalten Sie Ihr persönliches Profil, einschließlich Name, Geburtsdatum und medizinischer Vorgeschichte.")


        profile_image = st.sidebar.file_uploader("Profilfoto hochladen", type=["jpg", "jpeg", "png"])
        name = st.sidebar.text_input("Name", placeholder="Ihr Name")
        birthdate = st.sidebar.date_input("Geburtsdatum")


        if profile_image:
            st.sidebar.image(profile_image, caption="Profilfoto")



        st.markdown("""
            <style>
                /* Hintergrundfarbe der Sidebar auf Babyblau setzen */
                [data-testid="stSidebar"] {
                    background-color: LightBlue;
                }
                
                /* Textfarbe in der Sidebar auf Schwarz setzen */
                [data-testid="stSidebar"] * {
                    color: black;
                }
            </style>
        """, unsafe_allow_html=True)

        logout_button = st.button("Logout")
        if logout_button:
            st.session_state['authentication'] = False
            st.rerun()

if __name__ == "__main__":
    main()


