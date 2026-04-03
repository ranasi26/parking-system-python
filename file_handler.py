# file_handler.py
import json

FILE_NAME = "parking_data.json"


def save_data(slots):
    with open(FILE_NAME, "w") as file:
        json.dump(slots, file)


def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return None