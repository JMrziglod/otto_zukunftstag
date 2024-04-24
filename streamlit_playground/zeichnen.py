from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title('Zeichne auf der Leinwand')
brush_color = st.color_picker("Wähle eine Pinsel-Farbe:", "#000000")
brush_width = st.slider("Pinselbreite: ", min_value=1, max_value=50, value=10)

background_image = st.file_uploader("Hintergrundbild hochladen", type=["png", "jpg", "jpeg"])
# convert to image
if background_image is not None:
    background_image = Image.open(background_image)

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Feste Füllfarbe mit etwas Transparenz
    stroke_width=brush_width,
    stroke_color=brush_color,
    background_color="#eee",
    background_image=background_image,
    drawing_mode="freedraw",
    key="canvas",
)