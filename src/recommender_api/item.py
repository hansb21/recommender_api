# item.py
import utils
import json
from flask import abort

CONTEXT, USER = utils.open_files()
ITEM = utils.open_files("item")


def get_Itemschema() -> None | dict:
    return {
        "Movie": {
            "itemId": 0000,
            "title": "title",
            "description": "description",
            "year": 0000,
            "tags": "tags",
            "director": "director",
            "actors": "actors",
        },
        "Book": {
            "itemId": 0000,
            "title": "title",
            "description": "description",
            "year": 0000,
            "tags": "tags",
            "author": "author",
        },
        "Item": {
            "itemId": 0000,
            "title": "title",
            "price": "price",
            "dateAdded": "00/00/0000",
        },
    }


def register(item: dict) -> None | tuple:
    if item["Context"] in CONTEXT.keys():
        if item["Context"] not in ITEM.keys():
            ITEM[item["Context"]] = {}
            ITEM[item["Context"]]["items"] = {}
            ITEM[item["Context"]]["item_schema"] = CONTEXT[item["Context"]][
                "item_schema"
            ]
        schema = get_Itemschema()
        if CONTEXT[item["Context"]]["item_schema"] == "Movie":
            for i in item["itemIds"]:
                if i["itemId"] not in ITEM[item["Context"]]["items"].keys():
                    ITEM[item["Context"]]["items"][i["itemId"]] = {}
                for key, value in i.items():
                    if key in schema["Movie"].keys():
                        if key == "tags" and type(value) == list:
                            tags = " "
                            for i in value:
                                tags += " " + i

                            ITEM[item["Context"]]["items"][i["itemId"]]["tags"] = tags
                        else:
                            ITEM[item["Context"]]["items"][i["itemId"]][key] = value
        if CONTEXT[item["Context"]]["item_schema"] == "Book":
            for i in item["itemIds"]:
                if i["itemId"] not in ITEM[item["Context"]]["items"].keys():
                    ITEM[item["Context"]]["items"][i["itemId"]] = {}
                for key, value in i.items():
                    if key in schema["Book"].keys():
                        if key == "tags" and type(value) == list:
                            tags = ""
                            for v in value:
                                tags += v + ","

                            tags = tags[:-1]

                            ITEM[item["Context"]]["items"][i["itemId"]]["tags"] = tags

                        else:
                            ITEM[item["Context"]]["items"][i["itemId"]][key] = value
        if CONTEXT[item["Context"]]["item_schema"] == "Item":
            for i in item["itemIds"]:
                if i["itemId"] not in ITEM[item["Context"]]["items"].keys():
                    ITEM[item["Context"]]["items"][i["itemId"]] = {}
                for key, value in i.items():
                    if key in schema["Item"].keys():
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
