import google.generativeai as genai
import streamlit as st

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def list_models():
    """Lists available models and their supported methods."""
    try:
        for model in genai.client.list_models():
            st.write(f"**Model:** {model.name}")
            st.write(f"  **Description:** {model.description}")
            st.write(f"  **Supported methods:** {model.supported_generation_methods}")
            st.write("-" * 20)
    except Exception as e:
        st.error(f"Error listing models: {e}")

def main():
    st.title("Available Gemini Models")
    list_models()

if __name__ == "__main__":
    main()
