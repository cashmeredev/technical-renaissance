import os
import pathlib
from robyn.templating import JinjaTemplate
from typing import cast
import tomllib
from pathlib import Path
from robyn import Request
from robyn import Robyn
from typing import TypedDict


User = TypedDict("User", {"name": str, "url": str, "description": str})
Config = TypedDict("Config", {"user": list[User]})


def load_users(path: Path) -> list[User]:
    with path.open("rb") as f:
        return tomllib.load(f)["user"]


current_file_path = pathlib.Path(__file__).parent.resolve()
users = load_users(current_file_path / "config.toml")
app = Robyn(__file__)

app.serve_directory(
    route="/static",
    directory_path="./static",
)
current_file_path = pathlib.Path(__file__).parent.resolve()
JINJA_TEMPLATE = JinjaTemplate(os.path.join(current_file_path, "templates"))


@app.get("/")
async def root(_request: Request):
    return "Hello World"
@app.get("/next")
async def next_user(request: Request):
    current = index_of(request)
    next_index = (current + 1) % len(users)
    return redirect(users[next_index]["url"])


@app.get("/prev")
async def prev_user(request: Request):
    current = index_of(request)
    prev_index = (current - 1) % len(users)
    return redirect(users[prev_index]["url"])


@app.get("/random")
async def random_user(_request: Request):
    return redirect(random.choice(users)["url"])


app.start(host="127.0.0.1", port=8080)
