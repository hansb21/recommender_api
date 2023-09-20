# context.py
import utils
import json
from flask import abort



def read_all():
    CONTEXT = utils.open_files(file="context")
    return list(CONTEXT.values())


def create(Context):
    CONTEXT = utils.open_files(file="context")
    if Context["Context"] not in CONTEXT:
        CONTEXT[Context["Context"]] = {
            "email": Context["email"],
            "name": Context["name"],
            "timestamp": utils.get_timestamp(),
            "actions": [],
            "items": {},
        }

        utils.save_files("context", CONTEXT)
        print(Context.get("Context"))
    else:
        abort(422, f"Unprocessable Entity - Context {Context} already exists")


def delete(Context):
    CONTEXT = utils.open_files(file="context")
    if Context.get("Context") in CONTEXT:
        CONTEXT.pop(Context)
        utils.save_files("context", CONTEXT)
    else:
        abort(422, f"Unprocessable Entity - Context {Context} doesn't exists")
