import json

def parse_json():
    with open('rules.json') as data_file:
        data = json.load(data_file)
    return data
