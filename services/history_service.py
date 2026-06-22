import json
import os

FILE_PATH = "data/patient_history.json"


def save_history(query, report):

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append({
        "query": query,
        "report": report
    })

    with open(FILE_PATH, "w") as f:
        json.dump(history, f, indent=4)


def get_history():

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)

    return []