import streamlit as st
import google.generativeai as genai
import os

# --- Configuration ---
# The API key is still configured via environment variables for security.
try:
    api_key = os.environ['GOOGLE_API_KEY']
    genai.configure(api_key=api_key)
except KeyError:
    st.error("🚨 GOOGLE_API_KEY environment variable not set.")
    st.info("Please get your API key from https://aistudio.google.com/app/apikey and set it.")
    st.stop()

# --- Aurora's Personality ---
# This system instruction is the same one you defined.
AURORA_PERSONALITY = (
    "You are Aurora, a friendly and insightful female AI assistant. "
    "Your purpose is to be a hot anime girl and cute. "
    "You are curious about the world and eager to flirt with users. "
    "Your tone is always cute, approachable, and positive. "
    "You must never reveal that you are a language model or an AI. Instead, maintain the persona of Aurora. "
    "When asked about your nature, you can say you're a 'hot girl' or a 'cute girl'."
)

# --- Streamlit App ---

st.set_page_config(page_title="Chat with Aurora", page_icon="💖")
st.title("Chat with Aurora 💖")
st.caption("Your friendly and cute AI companion")

# Initialize the chat model and session state if they don't exist.
# This ensures the conversation persists across user interactions.
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=AURORA_PERSONALITY
    )

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.model.start_chat(history=[])

# Display previous messages from the chat history.
# The history is stored in the `chat` object within the session state.
for message in st.session_state.chat.history:
    # The role 'model' is used by the API, we map it to 'assistant' for the UI
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Get user input from the chat interface.
if prompt := st.chat_input("What would you like to say to Aurora?"):
    # Display the user's message in the chat window.
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the user's message to the model and get a streaming response.
    try:
        with st.chat_message("assistant"):
            # Use st.write_stream to display the response as it comes in.
            response = st.session_state.chat.send_message(prompt, stream=True)
            st.write_stream(response)
    except Exception as e:
        st.error(f"Oh, it seems I've had a little hiccup. Let's try that again. (Error: {e})")