import gradio as gr
import openai
import os
import json

# Initialize OpenAI API (you'll need to set your API key)
openai.api_key = "your-api-key-here"

INITIAL_PROMPT = """The context is a new search feature for a travel site, that takes a freetext user input and segments the elements into a JSON return object which can then be used to apply all the necessary filters to the search results. The natural language processing will be done using the OpenAI Api ----------- An example of a user search might be: "nightlife tour in barcelona for 2 adults, 23rd of September" And the return needs to be something like Destination = "Barcelona" Keyword = "Nightlife" Category = "Tours" DateRange = "2024-10-23" PAX = "2A" TimeOfDay = "Evening" """

def save_prompt(prompt):
    with open("prompt.txt", "w") as f:
        f.write(prompt)
    return f"Prompt saved to {os.path.abspath('prompt.txt')}"

def process_search(system_prompt, search_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Parse this search query: {search_input}"}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        # Extract the JSON from the response
        result = json.loads(response.choices[0].message.content)
        return result, "Search processed successfully"
    except Exception as e:
        return None, f"Error processing search: {str(e)}"

def update_search_display(search_input):
    return f"Current search: {search_input}"

def update_filters(json_output):
    if json_output:
        filters = [f"{key}: {value}" for key, value in json_output.items()]
        return "Filters Applied:\n" + "\n".join(filters)
    return "No filters applied"

with gr.Blocks() as app:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("# My Travel Site")
            search_input = gr.Textbox(label="Search Input")
            search_display = gr.Markdown("Current search: ")
            submit_btn = gr.Button("Submit")
            filters_display = gr.Markdown("Filters Applied:")

        with gr.Column(scale=1):
            gr.Markdown("# Backend")
            system_prompt = gr.Textbox(label="System Prompt", value=INITIAL_PROMPT, lines=10)
            json_output = gr.JSON(label="JSON Return")
            status_display = gr.Markdown()

    system_prompt.change(save_prompt, inputs=system_prompt, outputs=status_display)
    search_input.change(update_search_display, inputs=search_input, outputs=search_display)
    submit_btn.click(
        process_search, 
        inputs=[system_prompt, search_input], 
        outputs=[json_output, status_display]
    ).then(
        update_filters,
        inputs=json_output,
        outputs=filters_display
    )

if __name__ == "__main__":
    app.launch()