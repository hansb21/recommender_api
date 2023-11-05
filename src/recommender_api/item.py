# item.py
import utils
import json
from flask import abort

CONTEXT, USER = utils.open_files()
ITEM = utils.open_files("item")


def register(item: dict) -> None | tuple:
    if item["Context"] in CONTEXT.keys():
        if item["Context"] not in ITEM.keys():
            ITEM[item["Context"]] = {}
            ITEM[item["Context"]]["items"] = {}

        for i in item["itemIds"]:
            if i["itemId"] not in ITEM[item["Context"]]["items"].keys():
                ITEM[item["Context"]]["items"][i["itemId"]] = {}
            for key, value in i.items():
                ITEM[item["Context"]]["items"][i["itemId"]][key] = value

    utils.save_files("item", ITEM)


# Necessário ser refeita e refatorada para seguir o padrão
def delete(Context: str, itemId: str) -> None | tuple:
    if Context in CONTEXT.keys() and Context in ITEM.keys():
        if itemId in ITEM[Context]["items"].keys():
            ITEM[Context]["items"].pop(itemId)
        else:
            abort(422, f"Unprocessable Entity - Item {itemId} dosen't exists")
    else:
        abort(422, f"Unprocessable Entity - Context {Context}dosen't exists")

    utils.save_files("action", ITEM)
    return (200, "Sucessfully deleted item")


# ef deleteHistory(Context: str, userId: str) -> None | tuple:
#   for itemId in CONTEXT[Context]["items"]:
#       delete(Context, itemId)
#   return (200, "Sucessfully deleted user history")
