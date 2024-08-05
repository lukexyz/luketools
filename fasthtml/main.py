from fasthtml.common import *
from fh_altair import altair2fasthml, altair_headers
import numpy as np
import pandas as pd
import altair as alt

# pip install fh-altair

app = FastHTML(hdrs=[picolink, altair_headers])
count = 0
plotdata = []

# Custom CSS for centering
custom_css = Style("""
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 30vh;
        text-align: center;
    }
""")

def generate_chart():
    pltr = pd.DataFrame({'y': plotdata, 'x': range(len(plotdata))})
    chart = alt.Chart(pltr).mark_line().encode(x='x', y='y').properties(width=400, height=200)
    return altair2fasthml(chart)


@app.get("/")
def home():
    return (
        custom_css,
        Title("🎲 Count Demo with Chart"),
        Main(
            H1("🎲 The Great Counter Demo", id="header"),
            cls="center-container"
        ),
        Main(
            P(f"Count is set to {count}", id="count"),
            P(
                Button("Increment", hx_post="/increment", hx_target="#count"),
                Button("Decrement", hx_post="/decrement", hx_target="#count"),
                cls="button-group"
            ),
            Div(id="chart"),
            cls="center-container"
        )
    )

@app.post("/increment")
def increment():
    global count, plotdata
    count += 1
    plotdata.append(count+np.random.exponential(1))
    return (
        P(f"Count is set to {count}", id="count", hx_swap_oob="true"),
        Div(
            generate_chart(),
            P(f"x = {len(plotdata)}, y = {np.round(plotdata[-1], 4)}"),
            _id="chart",
            hx_swap_oob="true"
        )
    )

@app.post("/decrement")
def decrement():
    print("decrementing")
    global count, plotdata
    count -= 1
    plotdata.append(count-np.random.exponential(1))
    return (
        P(f"Count is set to {count}", id="count", hx_swap_oob="true"),
        Div(
            generate_chart(),
            P(f"x = {len(plotdata)}, y = {np.round(plotdata[-1], 4)}"),
            _id="chart",
            hx_swap_oob="true"
        )
    )

serve()