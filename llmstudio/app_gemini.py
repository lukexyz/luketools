import streamlit as st
import openai
import os

# --- Page Setup ---
st.set_page_config(page_title="Chat with OpenAI", layout="wide")
st.markdown(
    """
    <style>
        .stApp {
            background-color: #111111; /* Dark background */
            color: #CC66FF; /* Purple text */
        }

        .stTextInput {
            background-color: #222222; /* Darker input background */
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- OpenAI Setup ---
openai.api_key = os.environ.get("OPENAI_API_KEY")
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar (Model Settings) ---
with st.sidebar:
    st.markdown("## Model Settings")
    temperature = st.slider("Temperature:", 0.0, 1.0, 0.5)
    max_tokens = st.slider("Max Tokens:", 100, 1000, 250)

# --- Chat Input ---
if prompt := st.chat_input("Your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# --- OpenAI Chat Completion ---
if st.session_state.messages:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response:
            full_response += chunk['choices'][0]['delta'].get('content', '')
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
