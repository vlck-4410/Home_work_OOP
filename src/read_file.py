import json

#path = 'products.json'

def read_file_products(path_to_file):
    with open(path_to_file, encoding="utf8") as json_file:
        data = json.load(json_file)
        return data


