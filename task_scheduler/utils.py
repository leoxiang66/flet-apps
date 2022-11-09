import json

class IO:
    @classmethod
    def dict_to_json(cls, dictObj: dict, file_path:str):
        jsObj = json.dumps(dictObj)
        with open(file_path, 'w') as f:
            f.write(jsObj)


    @classmethod
    def json_to_dict(cls, file_path:str) -> dict:
        with open(file_path, 'r', encoding='UTF-8') as f:
            load_dict = json.load(f)
        return load_dict