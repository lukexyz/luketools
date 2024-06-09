from fasthtml import *

app = FastHTML(hdrs=[picolink])
messages = ["This is a message, which will get rendered as a paragraph"]

@app.get("/")
def home():
    return  Main(H1('Messages'), 
                Div(cls="grid", *[P(Mark(msg)) for msg in messages]),
                *[P(msg) for msg in messages],
                Div(A("Page 2 (to add messages)", href="/page2")),
                Div(A("Page 3 📄", href="/page3")),
                cls="container")

@app.get("/page2")
def page2():
    return Main(P("Add a message with the form below:"),
                Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/", method="post"),
                     A("Back to Home", href="/"))

@app.get("/page3")
def page3():
    return Main(H1('Details of Page 3'), 
           P("This is Page 3 of our FastHTML web application."), 
           A("Return to Home", href="/"), cls="container")

@app.post("/")
def add_message(data:str):
    messages.append(data)
    return home()