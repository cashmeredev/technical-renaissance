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


def return_config(path: Path) -> Config:
    with path.open("rb") as config:
        return cast(Config, tomllib.load(config))


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


app.start(host="127.0.0.1", port=8080)
