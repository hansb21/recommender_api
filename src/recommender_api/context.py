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
            "Metrics": [],
            "Recommenders": {},
            "item_schema": Context["item_schema"],
        }

        for i in Context["recommenders"][0]:
            CONTEXT[Context["Context"]]["Recommenders"][
                Context["recommenders"][0][i]["id"]
            ] = Context["recommenders"][0][i]["updateTime"]

        utils.save_files("context", CONTEXT)
    else:
        abort(422, f"Unprocessable Entity - Context {Context} already exists")


def delete(Context: str) -> None | tuple:
    CONTEXT = utils.open_files(file="context")
    if Context in CONTEXT:
        CONTEXT.pop(Context)
        utils.save_files("context", CONTEXT)
    else:
        abort(422, f"Unprocessable Entity - Context {Context} doesn't exists")


def createScale(Context: dict) -> None | tuple:
    CONTEXT = utils.open_files(file="context")
    if Context["Context"] in CONTEXT:
        for i in Context["Units"]:
            CONTEXT[Context["Context"]]["Metrics"].append(i)

    print(CONTEXT[Context["Context"]]["Metrics"])
    utils.save_files("context", CONTEXT)
