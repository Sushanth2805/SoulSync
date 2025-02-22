import google.generativeai as genai
import streamlit as st
import time

# Configure the Gemini API using secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def analyze_sentiment(user_input):
    """Basic sentiment analysis using keyword matching."""
    positive_words = ["happy", "excited", "grateful", "hopeful", "good"]
    negative_words = ["sad", "stressed", "anxious", "depressed", "bad"]
    
    user_words = user_input.lower().split()
    
    if any(word in user_words for word in positive_words):
        return "positive"
    elif any(word in user_words for word in negative_words):
        return "negative"
    else:
        return "neutral"

def get_ai_response(user_input, chat_history):
    """Generate an AI response using Gemini API with chat history and comforting tone."""
    model = genai.GenerativeModel("gemini-pro")
    conversation = "\n".join(chat_history + [f"User: {user_input}"])
    response = model.generate_content(conversation)

    # Ensure response.text exists before using it
    if response and hasattr(response, "text"):
        ai_reply = response.text
    else:
        ai_reply = "I'm here to listen. If you're feeling overwhelmed, consider seeking professional support."

    # Additional logic for breakup or love failure
    if any(word in user_input.lower() for word in ["relationship", "love", "breakup", "heartbreak", "lost love"]):
        ai_reply += "\n\nRemember, seeking professional guidance from a counselor or therapist can be very helpful in handling these emotions."
    
    return ai_reply

def main():
    st.title("🌿 AI Mental Health Chatbot 🌿")
    st.write("I'm here to support you. You're not alone. Let's talk.")
    
    if "username" not in st.session_state:
        st.session_state.username = ""
        st.session_state.chat_started = False
    
    if not st.session_state.username:
        st.session_state.username = st.text_input("Please enter your name:", "")
    
    if st.session_state.username and not st.session_state.chat_started:
        st.write(f"Welcome, {st.session_state.username}! 😊 I want you to know that your feelings matter, and I'm here to listen.")
        if st.button("Start Chatting"):
            st.session_state.chat_started = True
            st.session_state.chat_history = [f"Chatbot: Hello, {st.session_state.username}. How are you feeling today? Remember, I'm here for you."]
    
    if st.session_state.chat_started:
        user_input = st.text_input(f"{st.session_state.username}:", "")
        if user_input:
            sentiment = analyze_sentiment(user_input)
            if sentiment == "negative":
                st.session_state.chat_history.append("I'm really sorry you're feeling this way. You're not alone, and I'm here to support you. Would you like to talk more about it or try some relaxation exercises?")
            elif sentiment == "positive":
                st.session_state.chat_history.append("That’s wonderful to hear! Keep embracing the positivity. If there's anything on your mind, I'm always here to chat. 😊")
            else:
                st.session_state.chat_history.append("Thank you for sharing. I'm here to listen whenever you need me.")
            
            ai_response = get_ai_response(user_input, st.session_state.chat_history)
            st.session_state.chat_history.append(f"{st.session_state.username}: {user_input}")
            time.sleep(1)  # Simulating a more natural delay
            st.session_state.chat_history.append(f"Chatbot: {ai_response}")
        
        # Display only the last few messages to keep it conversational
        for message in st.session_state.chat_history[-5:]:
            st.write(message)

if __name__ == "__main__":
    main()
