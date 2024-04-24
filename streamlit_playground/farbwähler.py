import streamlit as st
import webcolors

st.title('Farbwähler-App')
mode = st.radio('Wähle einen Modus', ['Farbe aus Liste auswählen', 'Farbe per Maus auswählen'])
if mode == 'Farbe aus Liste auswählen':
    color = st.selectbox('Wähle eine Farbe', ["rot", "grün", "blau", "gelb", "schwarz", "weiß", "lila", "orange", "pink", "türkis", "braun", "grau"])
    color = {
        "rot": "#ff0000",
        "grün": "#00ff00",
        "blau": "#0000ff",
        "gelb": "#ffff00",
        "schwarz": "#000000",
        "weiß": "#ffffff",
        "lila": "#800080",
        "orange": "#ffa500",
        "pink": "#ffc0cb",
        "türkis": "#40e0d0",
        "braun": "#a52a2a",
        "grau": "#808080"
    }[color]
else:
    color = st.color_picker('Wähle eine Farbe', '#00f900')
st.markdown(f"Die ausgewählte Farbe hat den Hexcode: {color}")
try:
    st.markdown(f"Die Farbe hat den Namen: {webcolors.hex_to_name(color)}")
except ValueError:
    st.markdown("Der Name der Farbe konnte nicht gefunden werden.")
st.markdown(f"Deine ausgewählte Farbe: ![Farbe](https://via.placeholder.com/100x100/{color.strip('#')}/000000?text=+)")
