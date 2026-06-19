import os
import pathlib
import random
import tomllib
from pathlib import Path
from typing import TypedDict

from robyn import Request, Response, Robyn
from robyn.templating import JinjaTemplate


User = TypedDict("User", {"name": str, "url": str, "description": str})


def load_users(path: Path) -> list[User]:
    with path.open("rb") as f:
        return tomllib.load(f)["user"]


current_file_path = pathlib.Path(__file__).parent.resolve()
users = load_users(current_file_path / "config.toml")

app = Robyn(__file__)

app.serve_directory(
    route="/static",
    directory_path=os.path.join(current_file_path, "static"),
)
JINJA_TEMPLATE = JinjaTemplate(os.path.join(current_file_path, "templates"))


def index_of(request: Request) -> int:
    name = request.query_params.get("from", "")
    for i, user in enumerate(users):
        if user["name"] == name:
            return i
    return 0


def redirect(url: str) -> Response:
    return Response(status_code=302, headers={"Location": url}, description="")


@app.get("/")
async def index(_request: Request):
    return JINJA_TEMPLATE.render_template("index.html", users=users)


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
