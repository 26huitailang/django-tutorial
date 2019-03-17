#!/usr/bin/env python
# coding=utf-8

from mzitu.runtimes.redis import PicJsonRedis

# Dictionary mapping names to known classes
_classes = {
    'PicJsonRedis': PicJsonRedis,
}


def serialize_instance(obj) -> dict:
    """将一个cls对象变为dict

    json.dumps(obj, default=serialize_instance)
    """
    d = {'__classname__': type(obj).__name__}
    d.update(vars(obj))
    return d


def unserialize_object(d):
    """将一个包含__classname__的dict转为cls对象

    json.loads(d, object_hook=unserialize_object)
    """
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = _classes[clsname]
        obj = cls.__new__(cls)  # Make instance without calling __init__
        for key, value in d.items():
            setattr(obj, key, value)
        return obj
    else:
        return d
