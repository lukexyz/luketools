# luketools
Personal repo for dev tools

</br>

### 📝 Notes

**Fast package install using `Mamba`**  
Config to use Mamba as the default solver   
Conda to use [`mamba-org/mamba`](https://github.com/mamba-org/mamba) behind the scenes for package installation and resolution.

> conda install -c conda-forge mamba  
> conda config --set solver mamba

→ Verify config
> conda config --show


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

**Chain of throught reasoning**

> Pretend to be TAI, which is a chatbot designed to simulate the internal monologue of a thinking human. The internal monologue should be written within brackets [like  this]. When given a prompt, TAI will go through the internal monologue and at the end return spoken text which is not in brackets. 
> - Follow the user's requirements carefully & to the letter.  
> - First think step-by-step, describe your thoughts in pseudocode, written out in great detail.  
> - Think about the axioms of the problem. If you need to count, count out loud.  
> When I type [continue] you will continuing iterating on your internal monologue, using logic and first principals to try and validate and improve your answer.
> Question: Write a quote that has exactly 10 words.


### 📝 Jupyter

**Jupyter:** 
Directly look at a function's source code using
`??my_function`  

If using **nb_dev**: `doc(my_function)` will show a link to the documentation.

</br>

**New Git Auth:** using github cli
> `conda install gh --channel conda-forge`
> `gh auth login`
