# action.py

import utils
import json
from flask import abort


def read_all() -> dict:
    """Return the list of all existing actions

    Returns
    -------
    dict
        A dict containing all the existings actions per context
    """
    return utils.open_files(file="context")
    # return list(ACTION.values())


def create(action: dict) -> None | tuple:
    print(action)
    CONTEXT = utils.open_files(file="context")
    ACTION = utils.open_files(file="action")
    if action["Context"] in CONTEXT.keys():
        if action["Context"] not in ACTION.keys():
            ACTION[action["Context"]] = {} 
            ACTION[action["Context"]]["actions"] = {}
        if action["Action"] not in CONTEXT[action["Context"]]["actions"]:
            CONTEXT[action["Context"]]["actions"] = action["Action"]
            ACTION[action["Context"]]["actions"][action["Action"]] = {
                "itemID": [],
                "userID": [],
                "rating": [],
            }
            for metric in CONTEXT[action["Context"]]["Metrics"]:
                if metric["Unit"] == action["Unit"]:
                    ACTION[action["Context"]]["actions"][action["Action"]]["scale"] = (
                        metric["minScale"],
                        metric["maxScale"],
                    )

        for item in action["itemIds"][0]:
            for user, rate in action["itemIds"][0][item][0].items():
                ACTION[action["Context"]]["actions"][action["Action"]][
                    "itemID"
                ].append(item)
                ACTION[action["Context"]]["actions"][action["Action"]][
                    "userID"
                ].append(user)
                ACTION[action["Context"]]["actions"][action["Action"]][
                    "rating"
                ].append(rate)

        utils.save_files("context", CONTEXT)
        utils.save_files("action", ACTION)

        # return (200, "Sucessfully created action")

    else:
        abort(422, f"Unprocessable Entity - Context dosen't exists")


def delete(
    Context: str, Action: str, userId: str, itemId: str, actionValue: int
) -> None | tuple:
    CONTEXT = utils.open_files(file="context")
    ACTION = utils.open_files(file="action")
    if Context in CONTEXT.keys():
        if Action not in ACTION[Context]["actions"]:
            abort(422, f"Unprocessable Entity - Action {Action} dosen't exists")
        else:
            ACTION[Context]["actions"].remove(Action)

        utils.save_files("context", CONTEXT)
        utils.save_files("action", ACTION)
        return (200, "Sucessfully deleted action")

    else:
        abort(422, f"Unprocessable Entity - Context {Context} dosen't exists")
