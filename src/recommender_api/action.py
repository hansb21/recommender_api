# action.py

import utils
import json
from flask import abort


def read_all():
    pass
    # return list(ACTION.values())


def create(Context, Action, userId, itemId, actionValue, minScale=0, maxScale=1):
    CONTEXT = utils.open_files(file="context")
    if Action["Context"] in CONTEXT.keys():
        if Action["Action"] not in CONTEXT["Context"]["Action"]:
            CONTEXT[Action["Context"]][Action["Action"]] = {
                                    "itemID": [Action["itemId"]],
                                    "userID": [Action["userId"]],
                                    "rating": [Action["actionValue"]],
                                    "scale":  (Action["minScale"], Action["maxScale"])
                                    }
            CONTEXT[Context]["Scale"][Action] = (minScale, maxScale)
      
        else:

            CONTEXT[Context]["action"][Action]["itemID"].append(itemId)
            CONTEXT[Context]["action"][Action]["userID"].append(userId)
            CONTEXT[Context]["action"][Action]["rating"].append(actionValue)

        utils.save_files("context", CONTEXT)

    else:
        abort(422, f"Unprocessable Entity - Context {Context} dosen't exists")


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
