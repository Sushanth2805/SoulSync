import google.generativeai as genai
import streamlit as st
import time
import pyttsx3  # Text-to-speech
import speech_recognition as sr  # Speech-to-text

# Configure the Gemini API using st.secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech recognition service unavailable."

def analyze_hobbies(hobbies):
    """Use Gemini AI to analyze hobbies and generate insights."""
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Analyze the following hobbies and give insights on how they impact personality and interests: {hobbies}"
    response = model.generate_content(prompt)
    return response.text if response and hasattr(response, "text") else "Could not analyze hobbies."

def get_ai_response(user_input, chat_history, hobby_analysis):
    """Generate AI response using Gemini AI with hobby analysis."""
    model = genai.GenerativeModel("gemini-pro")
    conversation = "\n".join(chat_history + [f"User: {user_input}", f"Hobby Insights: {hobby_analysis}"])
    response = model.generate_content(conversation)
    return response.text if response and hasattr(response, "text") else "I'm here to listen." 

def main():
    st.title("🤖 Multi-Agent AI Chatbot")
    st.write("A chatbot that understands your hobbies, analyzes them, and chats with you.")
    
    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.hobbies = ""
        st.session_state.hobby_analysis = ""
        st.session_state.chat_history = []
    
    if st.session_state.step == 1:
        st.write("**Agent 1: Hobby Collector**")
        hobbies = st.text_area("Tell me about your hobbies:", "")
        if st.button("Submit Hobbies"):
            st.session_state.hobbies = hobbies
            st.session_state.step = 2
            st.rerun()
    
    elif st.session_state.step == 2:
        st.write("**Agent 2: Hobby Analyzer**")
        st.session_state.hobby_analysis = analyze_hobbies(st.session_state.hobbies)
        st.write("Hobby Analysis:", st.session_state.hobby_analysis)
        if st.button("Proceed to Chat"):
            st.session_state.step = 3
            st.rerun()
    
    elif st.session_state.step == 3:
        st.write("**Agent 3: Conversational Agent**")
        user_input = st.text_input("You:", "")
        
        if st.button("Speak"):
            spoken_text = speech_to_text()
            st.write(f"You (spoken): {spoken_text}")
            user_input = spoken_text
        
        if user_input:
            ai_response = get_ai_response(user_input, st.session_state.chat_history, st.session_state.hobby_analysis)
            st.session_state.chat_history.append(f"User: {user_input}")
            st.session_state.chat_history.append(f"Chatbot: {ai_response}")
            
            time.sleep(1)  # Simulating natural delay
            
            if st.checkbox("Read Response Aloud"):
                text_to_speech(ai_response)
        
        for message in st.session_state.chat_history[-5:]:
            st.write(message)

if __name__ == "__main__":
    main()
