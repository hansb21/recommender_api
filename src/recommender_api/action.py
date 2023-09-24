# action.py

import utils
import json
from flask import abort


def read_all():
    return utils.open_files(file="context")
    # return list(ACTION.values())


def create(action):
    CONTEXT = utils.open_files(file="context")
    if action["Context"] in CONTEXT.keys():
        if action["Action"] not in CONTEXT[action["Context"]]["actions"]:
            CONTEXT[action["Context"]]["actions"][action["Action"]] = {
                "itemID": [action["itemId"]],
                "userID": [action["userId"]],
                "rating": [action["actionValue"]],
                "scale": (action["minScale"], action["maxScale"]),
            }

        else:
            CONTEXT[action["Context"]]["actions"][action["Action"]]["itemID"].append(
                action["itemId"]
            )
            CONTEXT[action["Context"]]["actions"][action["Action"]]["userID"].append(
                action["userId"]
            )
            CONTEXT[action["Context"]]["actions"][action["Action"]]["rating"].append(
                action["actionValue"]
            )

        utils.save_files("context", CONTEXT)

    else:
        abort(422, f"Unprocessable Entity - Context dosen't exists")


def delete(Context, Action):
    CONTEXT = utils.open_files(file="context")
    if Context in CONTEXT.keys():
        print(CONTEXT[Context]["actions"])
        if Action not in CONTEXT[Context]["actions"]:
            abort(422, f"Unprocessable Entity - Action {Action} dosen't exists")
        else:
            CONTEXT[Context]["actions"].remove(Action)

        utils.save_files("context", CONTEXT)

    else:
        abort(422, f"Unprocessable Entity - Context {Context} dosen't exists")
