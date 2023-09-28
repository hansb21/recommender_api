# context.py
import utils
import json
from flask import abort


def read_all() -> list:
    CONTEXT = utils.open_files(file="context")
    return list(CONTEXT.values())


def create(Context: dict) -> None | tuple:
    CONTEXT = utils.open_files(file="context")
    if Context["Context"] not in CONTEXT:
        CONTEXT[Context["Context"]] = {
            "email": Context["email"],
            "name": Context["name"],
            "timestamp": utils.get_timestamp(),
            "actions": {},
            "items": {},
        }

        utils.save_files("context", CONTEXT)
        return (200, "Sucessfully created context")
    else:
        abort(422, f"Unprocessable Entity - Context {Context} already exists")


def delete(Context: str) -> None | tuple:
    CONTEXT = utils.open_files(file="context")
    if Context in CONTEXT:
        CONTEXT.pop(Context)
        utils.save_files("context", CONTEXT)
        return (200, "Sucessfully deleted context")
    else:
        abort(422, f"Unprocessable Entity - Context {Context} doesn't exists")
