from robyn import Request
from robyn import Robyn

app = Robyn(__file__)


@app.get("/")
async def root(_request: Request):
    return "Hello World"


app.start(host="127.0.0.1", port=8080)
