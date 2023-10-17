# item.py
import utils
import json
from flask import abort

CONTEXT, USER = utils.open_files()


def create(item: dict) -> None | tuple:
    if item["Context"] in CONTEXT.keys():
        for i in item["itemIds"]:
            print(i)
            if i["itemId"] not in CONTEXT[item["Context"]]["items"].keys():
                CONTEXT[item["Context"]]["items"][i["itemId"]] = {}
            for key, value in i.items():
                CONTEXT[item["Context"]]["items"][i["itemId"]][key] = value

    utils.save_files("context", CONTEXT)


def delete(Context: str, userId: str, itemId: str) -> None | tuple:
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
    return (200, "Sucessfully deleted item")


def deleteHistory(Context: str, userId: str) -> None | tuple:
    for itemId in CONTEXT[Context]["items"]:
        delete(Context, userId, itemId)
    return (200, "Sucessfully deleted user history")
