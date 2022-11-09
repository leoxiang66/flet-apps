from ..utils import IO

class BaseModel(IO):
    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            self.__setattr__(key,value)

    def to_dict(self) -> dict:
        ret = {}
        for key,value in self.__dict__.items():
            if hasattr(value,'to_dict'):
                ret[key] = value.to_dict()
            else:
                ret[key] = value
        return ret

    def to_json(self, path:str):
        self.dict_to_json(self.to_dict(),path)

    @classmethod
    def from_dict(cls,dictobj: dict):
        return cls(**dictobj)


    @classmethod
    def from_json(cls,path:str):
        return cls.from_dict(cls.json_to_dict(path))


    def __eq__(self, other):
        if not isinstance(other,self.__class__):
            return False
        else:
            for k,v in other.__dict__.items():
                if not hasattr(self,k):
                    return False
                else:
                    if self.__getattribute__(k) != v:
                        return False

            return True


    def __copy__(self):
        return self.__class__(**self.to_dict())

    def __deepcopy__(self, memodict={}):
        return self.__copy__()