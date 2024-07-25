import streamlit as st
from openai import OpenAI
from voice_chatbot.Voice_Chat import setup, write_chat_history

st.title("Written Chat Transcript")

client = setup()

write_chat_history()

if prompt := st.chat_input("Ask the supervisor questions"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]

        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = messages,
            stream = True,
        )
        response = st.write_stream(stream)

    st.session_state.chat_history.append({"role": "assistant", "content": response})