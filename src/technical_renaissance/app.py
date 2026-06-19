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


@app.get("/")
async def root(_request: Request):
    return "Hello World"


app.start(host="127.0.0.1", port=8080)
