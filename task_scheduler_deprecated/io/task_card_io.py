import json
from .base import IO

class TaskCardIO(IO):
    def to_json(self,file_path:str):
        dict = self.getDict()
        self.dict_to_json(dict,file_path)

    @classmethod
    def load_from_json(cls,file_path:str, cls_):
        dict_obj = cls.json_to_dict(file_path)
        return cls_(**dict_obj)

