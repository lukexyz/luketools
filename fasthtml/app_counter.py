from fasthtml import *
from fasthtml.fastapp import *

app = FastHTML(hdrs=[picolink])

count = 0

@app.get("/")
def home():
    return Title("🎲 Count Demo"), Main(
        H1("🎲 The Great Counter Demo"),
        P(f"Count is set to {count}", id="count"),
        Button("Increment", hx_post="/increment", hx_target="#count", hx_swap="innerHTML"),
        Button("Decrement", hx_post="/decrement", hx_target="#count", hx_swap="innerHTML")
    )

@app.post("/increment")
def increment():
    print("incrementing")
    global count
    count += 1
    return f"Count is set to {count}"

@app.post("/decrement")
def decrement():
    print("decrementing")
    global count
    count -= 1
    return f"Count is set to {count}"

serve()