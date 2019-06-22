import collections
from dataclasses import is_dataclass, asdict
from datetime import datetime
from ujson import dumps as ujson_dumps


def dumps(obj): 

    def convert_to_basic(o):
        if isinstance(o, dict):
            return {k: convert_to_basic(v) for k, v in o.items()}
        elif is_dataclass(o):
            return convert_to_basic(asdict(o))
        elif isinstance(o, list) or isinstance(o, collections.deque):
            return [convert_to_basic(e) for e in o]
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return o

    """ Dumps json and formats datetime to isotime """
    return ujson_dumps(convert_to_basic(obj))