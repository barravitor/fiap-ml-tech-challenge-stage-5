import json

def load_json_file(file_path: str):
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    return data
