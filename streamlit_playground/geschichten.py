import streamlit as st
from openai import AzureOpenAI

AZURE_API_KEY = "HIER DEN AZURE API KEY EINFÜGEN"
AZURE_ENDPOINT = "HIER DEN AZURE ENDPOINT EINFÜGEN"

SYSTEM_PROMPT = """
Du sollst mir eine lustige, kurze Geschichte erzählen. 
Die Geschichte soll unter 100 Wörter bleiben. 
Die Geschichte soll gut ausgehen.
"""

aoai = AzureOpenAI(
    azure_deployment="gpt-4-turbo",
    api_version="2024-03-01-preview",
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
)


def generate_story(character: str, setting: str, goal: str) -> str:
    user_prompt = f"Es war einmal ein {character}, der in {setting} lebte. Sein Ziel war es, {goal}."
    for text in aoai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        stream=True
        ):
        yield text


st.title('Erstelle dein Abenteuer')

charakter = st.selectbox('Wähle deinen Charakter', ['Pirat', 'Zauberer', 'Roboter'])
umgebung = st.selectbox('Wähle die Umgebung', ['Auf hoher See', 'In einem magischen Land', 'In der Zukunft'])
ziel = st.text_input('Was ist dein Ziel?')

if st.button('Erzähle die Geschichte'):
    # try:
    with st.spinner('Die Geschichte wird generiert...'):
        st.write_stream(generate_story(character=charakter, setting=umgebung, goal=ziel))
    # except Exception as e:
    #     st.write(f'Leider konnte die Geschichte nicht generiert werden. Wende dich an die Betreuer.')
