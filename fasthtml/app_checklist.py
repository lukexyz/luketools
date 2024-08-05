# run with: uvicorn main:app --reload
# or: python main.py with serve()

from fasthtml.common import *

app, rt = fast_app(hdrs=(picolink))

@rt('/')
def get():
    return Container(
        H1("Interactive F Checklist"),
        Form(
            Input(type="number", name="count", placeholder="Enter a f number", min=1, max=20),
            Button("Generate a Checklist"),
            hx_post="/generate",
            hx_target="#checklist"
        ),
        Div(id="checklist")
    )

@rt('/generate')
def post(count: int):
    checkboxes = [
        Div(
            Input(type="checkbox", id=f"item-{i}", name=f"item-{i}"),
            Label(f"Item {i}", for_=f"item-{i}"),
            hx_post=f"/toggle/{i}",
            hx_trigger="click",
            hx_target=f"#item-{i}"
        )
        for i in range(1, count + 1)
    ]
    return Div(*checkboxes)

@rt('/toggle/{item_id}')
def post(item_id: int, _):
    checked = Input(type="checkbox", id=f"item-{item_id}", name=f"item-{item_id}", checked=True)
    return Div(
        checked,
        Label(f"Item {item_id} toggled!", for_=f"item-{item_id}"),
        hx_post=f"/toggle/{item_id}",
        hx_trigger="click",
        hx_target=f"#item-{item_id}"
    )
