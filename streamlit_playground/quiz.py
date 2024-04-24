import streamlit as st

st.title('Tier-Quiz!')

fragen = [
    {
        'frage': 'Was sagt eine Katze?',
        'optionen': ['Miau', 'Wuff', 'Muh', 'Zwitscher'],
        'antwort': 'Miau'
    },
    {
        'frage': 'Welche Farbe haben Bananen?',
        'optionen': ['Rot', 'Gelb', 'Blau', 'Grün'],
        'antwort': 'Gelb'
    },
    {
        'frage': 'Was ist ein Hund?',
        'optionen': ['Fish', 'Reptil', 'Säugetier', 'Insekt'],
        'antwort': 'Säugetier'
    },
    {
        'frage': 'Welches Tier kann fliegen?',
        'optionen': ['Elefant', 'Hund', 'Fledermaus', 'Pferd'],
        'antwort': 'Fledermaus'
    },
    {
        'frage': 'Was ist ein Pinguin?',
        'optionen': ['Vogel', 'Fisch', 'Insekt', 'Säugetier'],
        'antwort': 'Vogel'
    },
]

punktestand = 0
for frage in fragen:
    antwort = st.radio(frage["frage"], frage['optionen'])
    if antwort.lower().strip() == frage['antwort'].lower().strip():
        punktestand += 1

st.write(f'Dein Punktestand: {punktestand}/{len(fragen)}')