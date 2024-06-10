import streamlit as st
import openai
from openai import OpenAI

# --- Page Setup ---
st.set_page_config(page_title="Chat with OpenAI or Local LLM", layout="wide")
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

# --- State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "backend" not in st.session_state:
    st.session_state.backend = "openai"  # Default backend

# --- Backend Selection ---
st.radio("Select Backend:", ("OpenAI", "Local LLM"), key="backend")

# --- OpenAI Setup ---
if st.session_state.backend == "openai":
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Local LLM Setup ---
elif st.session_state.backend == "local_llm":
    local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    model_name = "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF"  # Replace with your model name

# --- Sidebar (Model Settings) ---
with st.sidebar:
    st.markdown("## Model Settings")
    if st.session_state.backend == "openai":
        temperature = st.slider("Temperature:", 0.0, 1.0, 0.5)
        max_tokens = st.slider("Max Tokens:", 100, 1000, 250)
    elif st.session_state.backend == "local_llm":
        st.write("Local LLM settings are not adjustable in this demo.")

# --- Chat Input ---
if prompt := st.chat_input("Your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# --- Model Interaction ---
if st.session_state.messages:
    if st.session_state.backend == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response:
                full_response += chunk["choices"][0]["delta"].get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    elif st.session_state.backend == "local_llm":
        response = local_client.chat.completions.create(
            model=model_name,
            messages=st.session_state.messages
        )

        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message.content)
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
