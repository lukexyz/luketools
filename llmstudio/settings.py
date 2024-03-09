import toml
import os

# Path to your TOML file
toml_file_path = 'settings.toml'

def load_settings():
    """
    Loads settings from a TOML file. If the file does not exist, returns None.
    """
    if os.path.exists(toml_file_path):
        with open(toml_file_path, 'r') as toml_file:
            return toml.load(toml_file)
    else:
        return None

def save_settings(settings):
    """
    Saves the given settings to a TOML file.
    """
    with open(toml_file_path, 'w') as toml_file:
        toml.dump(settings, toml_file)

def get_system_prompt():
    """
    Returns the system prompt from the settings. If it's not set, initializes it with a default value,
    saves it, and then returns it.
    """
    settings = load_settings()
    if settings and "system_prompt" in settings:
        return settings["system_prompt"]
    else:
        # Default system prompt if not in TOML
        default_system_prompt = {"role": "system", "content": "Always answer in a riddle."}
        # Save the default to the TOML file
        save_settings({"system_prompt": default_system_prompt})
        return default_system_prompt

def update_system_prompt(new_prompt_content):
    """
    Updates the system prompt content in the settings and saves the settings to the TOML file.
    """
    # Load current settings or initialize with an empty dictionary if none exist
    settings = load_settings() or {}
    # Update the system prompt content
    settings["system_prompt"] = {"role": "system", "content": new_prompt_content}
    # Save the updated settings
    save_settings(settings)

# New function to get the selected model
def get_selected_model():
    settings = load_settings()
    if settings and "selected_model" in settings:
        return settings["selected_model"]
    else:
        # Default model if not set in TOML
        default_model = "gpt-3.5-turbo"
        save_settings({"selected_model": default_model})
        return default_model

# New function to update the selected model
def update_selected_model(new_model):
    settings = load_settings() or {}
    settings["selected_model"] = new_model
    save_settings(settings)