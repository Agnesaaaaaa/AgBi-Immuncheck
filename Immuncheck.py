import streamlit as st
import pandas as pd
from datetime import date
from github_contents import GithubContents
import binascii
import bcrypt
import os


st.markdown(
    """
    <h1 style='color: white;'>AgBi-Immuncheck - Digital Vaccination Passport</h1>
    """,
    unsafe_allow_html=True
)

# Constants
DATA_FILE = "Immucheck.csv"
DATA_COLUMNS = ["username", "Vaccination Date", "Vaccine/Drug", "Symptoms", "Follow-up Date"]

LOGIN_DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS_LOGIN = ['username', 'name', 'password']

PROFILE_DATA_FILE = "profile_data.csv"
DATA_COLUMNS_PROFILE = ['username', 'name', 'birth_date', 'general_practitioner', 'allergies', 'medications', 'profile_image']

def add_entry():
    st.header('Vaccinations')
    with st.form(key="entry_form"):
        vaccination_date = st.date_input("Vaccination Date", format="DD.MM.YYYY")
        vaccine_drug = st.text_input("Vaccine/Drug", placeholder="Type of vaccination or drug")
        symptoms = st.text_input("Symptoms", placeholder="Describe the symptoms")
        follow_up_date = st.date_input("Follow-up Date", format="DD.MM.YYYY")
        submit_button = st.form_submit_button("Add Entry")
        if submit_button:
            if vaccination_date and vaccine_drug and symptoms and follow_up_date:
                new_entry = {
                    DATA_COLUMNS[0]: st.session_state['username'],
                    DATA_COLUMNS[1]: vaccination_date,
                    DATA_COLUMNS[2]: vaccine_drug,
                    DATA_COLUMNS[3]: symptoms,
                    DATA_COLUMNS[4]: follow_up_date
                }
                if 'df' in st.session_state:
                    new_df = pd.DataFrame([new_entry])
                    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                    try:
                        st.session_state.df.to_csv(DATA_FILE, index=False)
                        st.success("New entry added successfully!")
                        
                        # Save data to GitHub
                        st.session_state.github.write_df(DATA_FILE, st.session_state.df, "added new entry")
                    except Exception as e:
                        st.error(f"Error saving data: {e}")
                else:
                    st.error("DataFrame is not initialized.")
            else:
                st.warning("Please fill in all fields before adding an entry.")
    show_data()

def show_data():
    if 'df' in st.session_state and not st.session_state.df.empty:
        if 'username' not in st.session_state.df.columns:
            st.error("DataFrame does not have a 'username' column.")
            return
        user_df = st.session_state.df[st.session_state.df['username'] == st.session_state['username']]
        if not user_df.empty:
            st.subheader("Your current vaccinations:")
            st.dataframe(user_df.drop(columns=['username']))
        else:
            st.warning("No entries found.")
    else:
        st.warning("No entries found.")

def initialize_data():
    if 'df' not in st.session_state:
        try:
            df = pd.read_csv(DATA_FILE)
            if 'username' not in df.columns:
                df['username'] = ""
            st.session_state.df = df
        except FileNotFoundError:
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def login_page():
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def registration_page():
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
            hashed_password_hex = binascii.hexlify(hashed_password).decode()
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose another one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS_LOGIN)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                st.session_state.github.write_df(LOGIN_DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)
    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes):
            st.session_state['username'] = username
            st.session_state['authentication'] = True
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Wrong password')
    else:
        st.error('Username not found')

def initialize_github():
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"]
        )
        st.write("GitHub initialized")

def initialize_login_information():
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(LOGIN_DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(LOGIN_DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS_LOGIN)

def main_page():
    st.header("Welcome to AgBi-Immuncheck")
    st.write("""
    Our app AgBi-Immuncheck offers a user-friendly platform for recording and managing vaccinations and monitoring related symptoms. Designed for individuals, our application allows easy and secure management of vaccination data and health information.

    Users can record their vaccinations in the app, including the vaccine, date, and location. This provides a central and easily accessible record of all received vaccinations. The app allows users to create profiles and store personal information such as name, birthdate, and medical history. This enables individual customization of vaccination and health management.
    """)
    st.write("Share your experiences with us!")
    
    # Feedback form
    feedback_text = st.text_area("Enter your feedback", height=150)
    rating = st.slider("Rate your experience", min_value=1, max_value=5, step=1)
    submit_button = st.button("Submit Feedback")
    
    # Submit feedback
    if submit_button:
        # Save feedback to a CSV file or database
        save_feedback(feedback_text, rating)
        st.success("Thank you for your feedback!")

def save_feedback(feedback_text, rating):
    feedback_df = pd.DataFrame({"Feedback": [feedback_text], "Rating": [rating]})
    feedback_df.to_csv("feedback.csv", mode='a', header=not os.path.exists("feedback.csv"), index=False)

def profile_page():
    st.title("My Profile")

    if 'profile' not in st.session_state:
        st.session_state.profile = {}

    if 'profile_image' not in st.session_state:
        st.session_state.profile_image = None

    if st.session_state.github.file_exists(PROFILE_DATA_FILE):
        profile_df = st.session_state.github.read_df(PROFILE_DATA_FILE)
        profile_dict = profile_df.set_index('username').T.to_dict()
        st.session_state.profile = profile_dict.get(st.session_state['username'], {})
    else:
        profile_df = pd.DataFrame(columns=DATA_COLUMNS_PROFILE)

    # Display profile information
    if st.session_state.profile:
        st.subheader("Saved Profile Information")
        for key, value in st.session_state.profile.items():
            st.write(f"{key.capitalize()}: {value}")
    else:
        st.info("No profile information found.")

    # Upload profile picture
    uploaded_image = st.file_uploader("Upload profile picture", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        st.session_state.profile_image = uploaded_image.read()
        st.image(st.session_state.profile_image, caption="Profile Picture", use_column_width=True)

    with st.form(key='profile_form'):
        name = st.text_input("Name", value=st.session_state.profile.get('name', ''))
        birth_date = st.date_input("Birth Date", value=st.session_state.profile.get('birth_date', date(2000, 1, 1)))
        general_practitioner = st.text_input("General Practitioner", value=st.session_state.profile.get('general_practitioner', ''))
        allergies = st.text_input("Allergies", value=st.session_state.profile.get('allergies', ''))
        medications = st.text_input("Medications", value=st.session_state.profile.get('medications', ''))

        if st.form_submit_button("Save Profile"):
            st.session_state.profile.update({
                'username': st.session_state['username'],
                'name': name,
                'birth_date': birth_date,
                'general_practitioner':general_practitioner,
                'allergies': allergies,
                'medications': medications,
                'profile_image': st.session_state.profile_image
            })

            profile_df = pd.DataFrame([st.session_state.profile])
            st.session_state.github.write_df(PROFILE_DATA_FILE, profile_df, "updated profile")
            st.success("Profile saved!")

def main():
    initialize_github()
    initialize_login_information()

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select Page", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            registration_page()
    else:
        initialize_data()
        pages = {
            "Dashboard": main_page,
            "Profile": profile_page,
            "Vaccinations": add_entry
        }
        st.sidebar.header("Navigation")
        page = st.sidebar.selectbox("Select Page", list(pages.keys()))
        pages[page]()

        st.sidebar.header("Profile")
        if st.sidebar.button("Logout"):
            st.session_state['authentication'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
