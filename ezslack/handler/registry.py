import re
from typing import Dict, List, Optional, Tuple, Type, get_args

from ..request import Request
from .handler import Handler


class HandlerRegistry:
    handlers: List[Tuple[Type[Handler], str, re.Pattern]]

    def __init__(self):
        self.handlers = []

    def set(self, cls: Type[Handler], mtd: str, keyword: re.Pattern):
        self.handlers.append((cls, mtd, keyword))

    def get(
        self, request_id: str
    ) -> Optional[Tuple[Type[Handler], str, List[str], Dict[str, str]]]:
        """Return matched handler class, method, and arguments"""
        for cls, mtd, keyword in self.handlers:
            if match := keyword.match(request_id):
                kwargs = match.groupdict()
                args = [
                    group
                    for i, group in enumerate(match.groups(), 1)
                    if i not in keyword.groupindex.values()
                ]
                return (cls, mtd, args, kwargs)
        return None


REGISTRIES = {cls.__name__: HandlerRegistry() for cls in get_args(Request)}
