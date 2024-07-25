import streamlit as st
import openai
from streamlit_mic_recorder import mic_recorder
from pathlib import Path
import io

st.title("Voice Chat")

def setup():
    # Set up OpenAI API client
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Initialise voice prompt
    if "voice_prompt" not in st.session_state:
        st.session_state["voice_prompt"] = ""

    # Select GPT model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    # Initialise chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    return client


# Write chat history
def write_chat_history():
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

client = setup()

def listen():

    audio = mic_recorder(start_prompt = "Start",
                        stop_prompt = "Stop",
                        just_once = False,
                        use_container_width = True,
                        format = "webm",
                        key = "recordbtn")

    if audio:
        return audio
    else:
        return None


def process_audio(audio):
    
    if audio is not None:
        audio_bio = io.BytesIO(audio["bytes"])
        audio_bio.name = "audio.webm"
        transcription = client.audio.transcriptions.create(file = audio_bio,
                                                            model = "whisper-1",
                                                            language = "en",
                                                            response_format = "text")
            
        if transcription:
            st.session_state["voice_prompt"] = transcription
            return transcription
    
    else:
        return None


def get_response(messages):
    completion = client.chat.completions.create(
        model = st.session_state["openai_model"],
        messages = messages
    )
    response = completion.choices[0].message.content
    return response


def speak(response, voice):
    speech_file_path = Path("audio.mp3")
    response = client.audio.speech.create(
      model="tts-1",
      voice=voice,
      input=response
    )
    response.stream_to_file(speech_file_path)


def chat_logic():
    promptaudio = listen()
    transcription = process_audio(promptaudio)

    if transcription:
        st.session_state.chat_history.append({"role": "user", "content": transcription})
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
        
        # Get response to prompt
        response = get_response(messages)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        speak(response, "alloy")
        audio_file = open("audio.mp3", 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mpeg', autoplay=True)
        
    else:
        return None


chat_logic()


        




