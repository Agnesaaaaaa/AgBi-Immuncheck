import streamlit as st

# Lade das CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Rufe die Funktion auf
load_css("styles.css")

# Dein restlicher Streamlit Code
st.title("# AgBi-Immuncheck")

st.markdown("""
Hi there 👋

Willkommen bei AgBi-Immuncheck! Unsere App bietet eine benutzerfreundliche Plattform zur Erfassung und Verwaltung von Impfungen sowie zur Überwachung von Symptomen im Zusammenhang mit den Impfungen. Entwickelt für Einzelpersonen, ermöglicht unsere Anwendung eine einfache und sichere Verwaltung von Impfdaten und Gesundheitsinformationen.

## Features

- **Erfassung von Impfungen**: Benutzer können ihre Impfungen in der App erfassen, einschließlich des Impfstoffs und des Datums. Dies bietet eine zentrale und leicht zugängliche Aufzeichnung aller erhaltenen Impfungen.
- **Profilverwaltung**: Die App ermöglicht es den Benutzern, Profile anzulegen und personenbezogene Informationen wie Name, Geburtsdatum und medizinische Vorgeschichte zu speichern. Dies ermöglicht eine individuelle Anpassung der Impf- und Gesundheitsverwaltung.
- **Überwachung von Symptomen**: Verfolgen Sie Symptome im Zusammenhang mit den Impfungen, um Ihre Gesundheit im Blick zu behalten.


## Mitwirkende

- Blertaaaaa

## Danksagungen

- Danke an alle Mitwirkenden und Tester, die dieses Projekt möglich gemacht haben.✔️

[AgBi-Immuncheck](https://agbi-immuncheck.streamlit.app/#agbi-immuncheck-digitaler-impfpass)
""")
