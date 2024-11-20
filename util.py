import json
def createJson(name:str,content:dict):
    with open(f'{name}.json', 'w') as fp:
        json.dump(content, fp)