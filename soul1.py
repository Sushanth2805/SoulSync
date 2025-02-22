import google.generativeai as genai
import streamlit as st
import time
from gtts import gTTS
import io
import sounddevice as sd
import numpy as np
import vosk
import queue

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def text_to_speech(text):
    """Convert text to speech using gTTS."""
    tts = gTTS(text=text, lang="en")
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    st.audio(audio_data, format="audio/mp3")

def analyze_hobbies(hobbies):
    """Use Gemini AI to analyze hobbies and generate insights."""
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Analyze these hobbies and explain their impact on personality: {hobbies}"
    response = model.generate_content(prompt)
    return response.text if response and hasattr(response, "text") else "Could not analyze hobbies."

def get_ai_response(user_input, chat_history, hobby_analysis):
    """Generate AI response using Gemini AI with hobby analysis."""
    model = genai.GenerativeModel("gemini-pro")
    conversation = "\n".join(chat_history + [f"User: {user_input}", f"User's Hobbies: {st.session_state.hobbies}", f"Hobby Insights: {hobby_analysis}"])
    response = model.generate_content(conversation)
    return response.text if response and hasattr(response, "text") else "I'm here to listen."

def recognize_speech():
    """Capture voice input using sounddevice and recognize with Vosk."""
    model = vosk.Model("model")  # Ensure you have a Vosk model downloaded
    recognizer = vosk.KaldiRecognizer(model, 16000)
    q = queue.Queue()
    
    def callback(indata, frames, time, status):
        if status:
            st.write(status)
        q.put(bytes(indata))
    
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        st.write("Listening...")
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            return result["text"]
        else:
            return "Sorry, I couldn't understand that."

def main():
    st.title("🎙️ AI Chatbot with Hobby Analysis")
    
    # Session state setup
    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.hobbies = ""
        st.session_state.hobby_analysis = ""
        st.session_state.chat_history = []

    # Step 1: Collect hobbies
    if st.session_state.step == 1:
        st.write("**Agent 1: Hobby Collector**")
        hobbies = st.text_area("Tell me about your hobbies:")
        if st.button("Submit Hobbies"):
            st.session_state.hobbies = hobbies
            st.session_state.step = 2
            st.rerun()

    # Step 2: Analyze hobbies
    elif st.session_state.step == 2:
        st.write("**Agent 2: Hobby Analyzer**")
        st.session_state.hobby_analysis = analyze_hobbies(st.session_state.hobbies)
        st.write("**Hobby Analysis:**", st.session_state.hobby_analysis)
        if st.button("Proceed to Chat"):
            st.session_state.step = 3
            st.rerun()

    # Step 3: Conversational Agent
    elif st.session_state.step == 3:
        st.write("**Agent 3: Conversational Chatbot**")

        # Speech-to-text toggle
        use_voice_input = st.checkbox("Use Live Voice Input")

        # Initialize user_input to avoid UnboundLocalError
        user_input = ""

        if use_voice_input:
            if st.button("Start Listening"):
                user_input = recognize_speech()
                st.text_input("You:", value=user_input, key="voice_input")
        else:
            user_input = st.text_input("You:")

        if user_input.strip():  # Ensure user_input is not empty
            ai_response = get_ai_response(user_input, st.session_state.chat_history, st.session_state.hobby_analysis)
            st.session_state.chat_history.append(f"User: {user_input}")
            st.session_state.chat_history.append(f"Chatbot: {ai_response}")

            time.sleep(1)  # Simulate natural delay
            st.write("**Chatbot:**", ai_response)

            if st.button("Read Response Aloud"):
                text_to_speech(ai_response)

        for message in st.session_state.chat_history[-5:]:
            st.write(message)

if __name__ == "__main__":
    main()
