from fasthtml import *

app = FastHTML(hdrs=[picolink])
messages = ["This is a message, which will get rendered as a paragraph"]

@app.get("/")
def home():
    return  Title("Hello World"), \
            Main(Div(Button("Reload", onclick="window.location.reload();", style="position: absolute; top: 10px; right: 10px;"), cls="reload-button"),
            H1('Messages'), 
            Div(cls="grid", *[P(Mark(msg)) for msg in messages]),
            Div(A("Page 2 (to add messages)", href="/page2")),
            Div(A("Page 3 📄", href="/page3")),
            P(f"{messages}"),
            cls="container")

@app.get("/page2")
def page2():
    return Title("Add a message"), \
            Main(P("Add a message with the form below:"),
                Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/", method="post"),
                     A("Back to Home", href="/"))

@app.get("/page3")
def page3():
    return Title("Hello World"), Main(H1('Hello, World'), 
            P("This is a simple ", Code("FastHTML"), " web application yo."), 
            P("You can add messages to the list below and see them appear in the list."),
            P("You can also click on the links in the menu to navigate to other pages."),
            A("Back to Home", href="/"),
            cls="container")
            
@app.post("/")
def add_message(data:str):
    messages.append(data)
    return home()