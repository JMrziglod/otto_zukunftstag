import streamlit as st
import random

st.title('Wie fühlst du dich heute?')

stimmungen = {
    'Glücklich': '😊',
    'Traurig': '😢',
    'Aufgeregt': '🤩',
    'Wütend': '😠',
}

stimmung = st.radio("Wähle deine Stimmung:", list(stimmungen.keys()))

st.write(f'Du fühlst dich {stimmungen[stimmung]}')

if stimmung == 'Glücklich':
    st.write('Bleib fröhlich und genieße deinen Tag!')
elif stimmung == 'Traurig':
    st.write('Es ist in Ordnung, sich traurig zu fühlen. Hier ist eine lustige Tatsache, um dich aufzuheitern:')
    st.write(random.choice(["Pinguine können 6 Fuß hoch springen!", "Delfine haben Namen für einander!"]))
elif stimmung == 'Aufgeregt':
    st.write('Das ist großartig! Nutze deine Energie für etwas Spaßiges oder Kreatives!')
elif stimmung == 'Wütend':
    st.write('Atme tief durch. Vielleicht hilft es dir, deine Gefühle zu zeichnen oder aufzuschreiben.')