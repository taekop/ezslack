from __future__ import annotations

from dataclasses import dataclass
import functools
import re
from slack_bolt import Ack, Respond, Say
from slack_sdk.web import WebClient
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from .types import RequestType


class HandlerRegistry:
    handlers: Dict[RequestType, List[Tuple[re.Pattern, Type[Handler], str]]] = {}

    def register_handler(self, handler: Type[Handler]):
        """Save handler methods"""
        for func in handler.__dict__.values():
            if callable(func) and (_handle := getattr(func, "_handle")):
                request_type, keyword = _handle
                self.handlers.setdefault(request_type, [])
                self.handlers[request_type].append((keyword, handler, func.__name__))

    def search_handler(
        self, request_type: RequestType, request_id: str
    ) -> Optional[Tuple[Type[Handler], str, List[str]]]:
        """Return matched handler class, method, and arguments"""
        if keyword_handler_methods := self.handlers.get(request_type):
            for keyword, handler, mtd in keyword_handler_methods:
                if match := keyword.match(request_id):
                    return (handler, mtd, list(match.groups()))
        return None


HANDLER_REGISTRY = HandlerRegistry()


@dataclass
class Handler:
    request_id: str
    request_type: RequestType
    ack: Ack
    body: Dict[str, Any]
    client: WebClient
    respond: Respond
    say: Say
    channel_id: Optional[str]
    channel_name: Optional[str]
    message_ts: Optional[str]
    thread_ts: Optional[str]
    trigger_id: Optional[str]
    user_id: str
    user_name: Optional[str]

    def __init_subclass__(cls):
        super().__init_subclass__()
        HANDLER_REGISTRY.register_handler(cls)


def handle(request_type: RequestType, keyword: Union[str, re.Pattern]):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        nonlocal keyword
        if isinstance(keyword, str):
            keyword = re.compile("^" + keyword + "$")
        wrapper._handle = (request_type, keyword)
        return wrapper

    return decorator


def action(keyword: Union[str, re.Pattern]):
    return handle(RequestType.ACTION, keyword)


def message(keyword: Union[str, re.Pattern]):
    return handle(RequestType.MESSAGE, keyword)


def view_submission(keyword: Union[str, re.Pattern]):
    return handle(RequestType.VIEW_SUBMISSION, keyword)


def view_closed(keyword: Union[str, re.Pattern]):
    return handle(RequestType.VIEW_CLOSED, keyword)
