from datetime import datetime
import json
from os import write


def open_files(file="all"):
    if file == "context":
        with open("json/context.json", "r") as read_file:
            return json.load(read_file)
    elif file == "user":
        with open("json/user.json", "r") as read_file:
            return json.load(read_file)
    elif file == "recommendation":
        with open("json/recommendation.json", "r") as read_file:
            return json.load(read_file)
    elif file == "security":
        with open("json/auth.json", "r") as read_file:
            return json.load(read_file)
    else:
        with open("json/context.json", "r") as read_file:
            CONTEXT = json.load(read_file)

        with open("json/user.json", "r") as read_file:
            USER = json.load(read_file)

        return CONTEXT, USER


def save_files(file, content):
    if file == "context":
        with open("json/context.json", "w") as write_file:
            json.dump(content, write_file)
    elif file == "user":
        with open("json/user.json", "w") as write_file:
            json.dump(content, write_file)
    elif file == "recommendation":
        with open("json/recommendation.json", "w") as write_file:
            json.dump(content, write_file)


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
