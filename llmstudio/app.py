from openai import OpenAI
import streamlit as st
import os

st.set_page_config(layout="wide", initial_sidebar_state='collapsed', page_icon="🧊")

# client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

if "model" not in st.session_state:
    # st.session_state["model"] = "local-model"
    st.session_state["model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

default_system_prompt = {"role": "system", "content": "Always answer in a riddle."}
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = default_system_prompt

# ============== Layout ==============

col1, col2 = st.columns([1, 2])

with col1:
    with st.expander("System Prompt Settings", expanded=True):
        system_content = st.text_area("Edit system prompt:", st.session_state.system_prompt["content"])
        if system_content != st.session_state.system_prompt["content"]:
            st.session_state.system_prompt["content"] = system_content
        

with col2:
    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input for new messages
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Include the system prompt in the messages for the completion request
            messages_for_completion = [st.session_state.system_prompt] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            stream = client.chat.completions.create(
                model=st.session_state["model"],
                messages=messages_for_completion,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# ============== Debugging ============== #
st.code(f'system prompt: {st.session_state.system_prompt["content"]}')