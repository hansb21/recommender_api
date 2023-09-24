# item.py
import utils
import json
from flask import abort

CONTEXT, USER = utils.open_files()


def create(item):
    if item["Context"] in CONTEXT.keys():
        if (
            item["itemId"] not in CONTEXT[item["Context"]]["items"].keys()
        ):  # Create Item
            CONTEXT[item["Context"]]["items"][item["itemId"]] = {
                item["Action"]: {"users": [item["userId"]], "interactions": 1}
            }
        else:  # Update existing item
            CONTEXT[item["Context"]]["items"][item["itemId"]][item["Action"]][
                "users"
            ].append(item["userId"])
            CONTEXT[item["Context"]]["items"][item["itemId"]][item["Action"]][
                "interactions"
            ] += 1
        USER[item["userId"]] = {
            item["itemId"]: item["Action"],
            "Context": item["Context"],
        }
        utils.save_files("context", CONTEXT)
        utils.save_files("user", USER)
    else:
        abort(422, f"Unprocessable Entity - Context dosen't exists")


def delete(Context, userId, itemId):
    if Context in CONTEXT.keys():
        if itemId in CONTEXT[Context]["items"].keys():
            if userId in CONTEXT[Context]["items"][itemId]["action"]:
                CONTEXT[Context]["items"][itemId]["action"]["users"].pop(userId)
                CONTEXT[Context]["items"][itemId]["action"]["interactions"] -= 1

            else:
                abort(422, f"Unprocessable Entity - User {userId} dosen't exists")
        else:
            abort(422, f"Unprocessable Entity - Item {itemId} dosen't exists")
    else:
        abort(422, f"Unprocessable Entity - Context {Context}dosen't exists")

    if len(CONTEXT[Context]["items"][itemId]["action"]) == 0:
        CONTEXT[Context]["items"].remove(itemId)

    if userId in USER.keys():
        if itemId in USER[userId].keys() and USER[userId]["Context"] == Context:
            del USER[userId][itemId]
    else:
        abort(422, f"Unprocessable Entity - User {userId} dosen't exists")

    utils.save_files("context", CONTEXT)
    utils.save_files("user", USER)


def deleteHistory(Context, userId):
    if Context in CONTEXT.keys():
        for items in CONTEXT[Context]["items"].keys():
            if userId in CONTEXT[Context]["items"][items]["actions"]:
                CONTEXT[Context]["items"][items]["action"]["users"].pop(userId)
                CONTEXT[Context]["items"][items]["action"]["interactions"] -= 1
            else:
                abort(422, f"Unprocessable Entity - User {userId} dosen't exists")
    else:
        abort(422, f"Unprocessable Entity - Context {Context}dosen't exists")

    if userId in USER.keys():
        if USER[userId]["Context"] == Context:
            del USER[userId]
    else:
        abort(422, f"Unprocessable Entity - User {userId} dosen't exists")

    utils.save_files("context", CONTEXT)
    utils.save_files("user", USER)
