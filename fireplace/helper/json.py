import collections
import pytz
from dataclasses import is_dataclass, asdict
from datetime import datetime
from ujson import dumps as ujson_dumps  # pylint: disable-msg=no-name-in-module


def convert_to_basic(o):
    if isinstance(o, dict):
        return {k: convert_to_basic(v) for k, v in o.items()}
    elif is_dataclass(o):
        return convert_to_basic(asdict(o))
    elif isinstance(o, list) or isinstance(o, collections.deque):
        return [convert_to_basic(e) for e in o]
    elif isinstance(o, datetime):
        return o.replace(tzinfo=pytz.utc).isoformat()
    else:
        return o


def dumps(obj): 
    """ Dumps json and formats datetime to isotime """
    return ujson_dumps(convert_to_basic(obj))