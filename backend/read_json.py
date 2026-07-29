import json
import os


def read_json(f_name: str, path=None):
    file_path = ""
    file_name = f_name.replace(".json", "")
    if path:
        file_path = os.path.join(path, f'{file_name}.json')
    else:
        file_path = f"{file_name}.json"

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Couldn't open {file_name}.json: {e}")
        f = open(file_path, "x")
