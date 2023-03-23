# luketools
Personal repo for dev tools

</br>

### 📝 Notes
</br>
**Prompts for LLMs**
> You are an AI programming assistant.
> - Follow the user's requirements carefully & to the letter.
> - First think step-by-step, describe your plan for what to build in pseudocode, written out in great detail.
> - Then output the code in a single code block.
> - Minimize any other prose.

> Write me a Discord bot with each of these requirements:
> - Accepts message containing image and text inputs.
> - No need special text to trigger the bot; should read & respond to every message.
> - Use the `gpt-4` model in the API rather than `gpt-3.5-turbo` and then post the results
> - Reads credentials from the DISCORD_TOKEN and OPENAI_API_KEY env vars
___

**Jupyter:** 
Directly look at a function's source code using
`??my_function`  

If using **nb_dev**: `doc(my_function)` will show a link to the documentation.

</br>

**New Git Auth:** using github cli
> `conda install gh --channel conda-forge`
> `gh auth login`
