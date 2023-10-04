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
    if action["Context"] in CONTEXT.keys():
        if action["Action"] not in CONTEXT[action["Context"]]["actions"]:
            CONTEXT[action["Context"]]["actions"][action["Action"]] = {
                "itemID": [],
                "userID": [],
                "rating": [] 
                }
            for metric in CONTEXT[action["Context"]]["Metrics"]:
                print(metric)
                if metric["Unit"] == action["Unit"]:
                    CONTEXT[action["Context"]]["actions"][action["Action"]]["scale"] = (metric["minScale"], metric["maxScale"])

        for item in action["itemIds"][0]:
            for user, rate in action["itemIds"][0][item][0].items():
                print(item)
                print(rate)
                CONTEXT[action["Context"]]["actions"][action["Action"]][
                    "itemID"
                ].append(item)
                CONTEXT[action["Context"]]["actions"][action["Action"]][
                    "userID"
                ].append(user)
                CONTEXT[action["Context"]]["actions"][action["Action"]][
                    "rating"
                ].append(rate)

        utils.save_files("context", CONTEXT)

        # return (200, "Sucessfully created action")

    else:
        abort(422, f"Unprocessable Entity - Context dosen't exists")


def delete(
    Context: str, Action: str, userId: str, itemId: str, actionValue: int
) -> None | tuple:
    CONTEXT = utils.open_files(file="context")
    if Context in CONTEXT.keys():
        print(CONTEXT[Context]["actions"])
        if Action not in CONTEXT[Context]["actions"]:
            abort(422, f"Unprocessable Entity - Action {Action} dosen't exists")
        else:
            CONTEXT[Context]["actions"].remove(Action)

        utils.save_files("context", CONTEXT)
        return (200, "Sucessfully deleted action")

    else:
        abort(422, f"Unprocessable Entity - Context {Context} dosen't exists")
