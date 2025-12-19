from os import environ

data: list[dict] = []
CONNECTION_STRING: str | None = environ.get("CONNECTION_STRING")
