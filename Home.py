import streamlit as st
from openai import OpenAI


def setup():
    st.write("Setting up")
    # Set up OpenAI API client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Select GPT model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialise chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
setup()


# Write chat history
def write_chat_history():
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


with st.container():
    left, right = st.columns([0.9, 0.1])
    with left:
        text_from_chat_input_widget = st.chat_input("Type here", key="chat1")
    with right:
        text2 = st.chat_input("type here instead", key="chat2")


def app_start():
    st.write("App start")
    write_chat_history()