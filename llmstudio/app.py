from openai import OpenAI
import streamlit as st
import os
import toml
import json

from settings import get_system_prompt, update_system_prompt, load_settings
from settings import get_selected_model, update_selected_model
from settings import apply_style, set_page_title

st.set_page_config(layout="wide", initial_sidebar_state='collapsed', page_icon="💎")
set_page_title("llm-studio")
apply_style()


st.image("media/llworld.png", width=300)

# ============== Init settings ============== #

# Assuming this is run at the start of your app.py
# Check if the model has already been set in the session state
if "model" not in st.session_state:
    # Load the current model from TOML configuration only if not already set
    current_model = get_selected_model()
    st.session_state["model"] = current_model

# Use the current model from session state for display and selection
model_selection_popover = st.popover(f'Model: `{st.session_state["model"]}`')
selected_model = model_selection_popover.radio("Choose a model:", ["gpt-3.5-turbo","local-model",  "gpt-4"], index=0)

if selected_model != st.session_state["model"]:
    # Update session state and TOML file if a new model is selected
    st.session_state["model"] = selected_model
    update_selected_model(selected_model)  # This should correctly update the TOML file
    st.experimental_rerun()

# Use the selected model from session state to determine the client configuration
if st.session_state["model"] == "local-model":
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
else:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = get_system_prompt()

# ============== App ============== #

# Create a column layout


col1, col2 = st.columns([1, 2])

with col1:
    with st.expander(f"System Prompt Settings", expanded=True):
        system_content = st.text_area(f"Edit system prompt: `{st.session_state['model']}`", st.session_state.system_prompt["content"])
        if system_content != st.session_state.system_prompt["content"]:
            st.session_state.system_prompt["content"] = system_content
            update_system_prompt(system_content)


# Existing code for displaying messages and handling chat input
with col2:
    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input for new messages
    tester_str = """Player2, facing an assassination attempt, must weigh their options. With one influence already exposed, losing another influence would eliminate them from the game. Given Player2's previous cautious approach, it's likely they would attempt to block the assassination if they have the Contessa or decide to bluff claiming they have the Contessa to avoid being knocked out of the game.

Assuming Player2 claims to have the Contessa to block the assassination:

This claim can be challenged by Player1. If Player1 believes Player2 is bluffing and decides to challenge, Player2 would need to reveal their influence card. If Player2 does not actually have the Contessa, they would lose their remaining influence and be eliminated from the game.
If Player1 does not challenge the claim, the assassination attempt is blocked, and the game continues with Player1's turn ending and Player2 retaining their remaining influence."""
   
    if prompt := st.chat_input(f"{tester_str}"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # Here is where we add the buttons for selecting the next action
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Challenge Player2's claim of the Contessa"):
            prompted_ans = "Challenge Player2's claim of having the Contessa."
    with col2:
        if st.button("Do not challenge and end your turn"):
            dd = "Do not challenge Player2's claim and end your turn."

    with col3:
        if st.button("Attempt a different action instead of assassination"):
            ee = "Attempt a different action instead of assassination."


# ===================== Debug Menu =======================   
                    
#     __         __                       __              
# .--|  |.-----.|  |--.--.--.-----.-----.|__|.-----.-----.
# |  _  ||  -__||  _  |  |  |  _  |  _  ||  ||     |  _  |
# |_____||_____||_____|_____|___  |___  ||__||__|__|___  |
#                           |_____|_____|          |_____|


tab0, tab1, tab2, tab3, tab4 = st.tabs(["Toml", "System Prompt", "Response", "Messages", "Session State"])
with tab0: st.code(f'{toml.dumps(load_settings())}', language='toml')
with tab1: st.code(f'system prompt: {st.session_state.system_prompt["content"]}')
with tab2: 
    try: 
        st.code(f'response: {response}')  # Ensure 'response' is defined or fetched appropriately
    except NameError: st.code("No response yet")
with tab3: st.code(f'messages: {st.session_state.messages}')  # Assuming 'st.session_state.messages' is defined
with tab4: st.code(json.dumps(dict(st.session_state), indent=2), language="json")
    


