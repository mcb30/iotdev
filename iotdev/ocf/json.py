"""JSON encoding"""

from collections.abc import Iterable
from datetime import date, time
import json
from uuid import UUID


class JSONEncoder(json.JSONEncoder):
    """JSON encoder"""

    def default(self, o):
        # pylint: disable=method-hidden
        if isinstance(o, (date, time)):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, Iterable):
            return list(o)
        return super().default(o)


class JSONDecoder(json.JSONDecoder):
    """JSON decoder"""
    pass
