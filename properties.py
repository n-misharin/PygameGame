import json
import os

file_name = os.path.join("", "resources", "properties.json") \
    if __name__ == '__main__' else os.path.join("resources", "properties.json")

with open(file_name, encoding='utf-8') as base_data:
    data = json.load(base_data)

RESOURCES = data['resources']
FIELDS = data['grounds']
UNITS = data['units']


if __name__ == '__main__':
    for element in RESOURCES:
        print(f"""RESOURCE_{element['name'].upper()} = {element['type']}""")
    print(FIELDS)
    for element in FIELDS:
        print(f"""FIELD_{element['name'].upper()} = {element['type']}""")
    print()
    for element in UNITS:
        print(f"""UNIT_{element['name'].upper()} = {element['type']}""")
    print()
