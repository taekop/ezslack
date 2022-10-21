from __future__ import annotations

from dataclasses import dataclass
import functools
import re
from slack_bolt import Ack, Respond, Say
from slack_sdk.web import WebClient
from slack_sdk.models.metadata import Metadata
from slack_sdk.models.views import ViewState
from typing import Any, Dict, List, Optional, Tuple, Type

from .types import RequestType


class HandlerRegistry:
    handlers: Dict[RequestType, List[Tuple[re.Pattern, Type[Handler], str]]] = {}

    def register_handler(self, handler: Type[Handler]):
        """Save handler methods"""
        for func in handler.__dict__.values():
            if callable(func) and (_handle := getattr(func, "_handle", None)):
                request_type, keywords = _handle
                self.handlers.setdefault(request_type, [])
                for keyword in keywords:
                    self.handlers[request_type].append(
                        (keyword, handler, func.__name__)
                    )

    def search_handler(
        self, request_type: RequestType, request_id: str
    ) -> Optional[Tuple[Type[Handler], str, List[str], Dict[str, str]]]:
        """Return matched handler class, method, and arguments"""
        if keyword_handler_methods := self.handlers.get(request_type):
            for keyword, handler, mtd in keyword_handler_methods:
                if match := keyword.match(request_id):
                    kwargs = match.groupdict()
                    args = [
                        group
                        for i, group in enumerate(match.groups(), 1)
                        if i not in keyword.groupindex.values()
                    ]
                    return (handler, mtd, args, kwargs)
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
    metadata: Optional[Metadata]
    private_metadata: Optional[str]
    thread_ts: Optional[str]
    trigger_id: Optional[str]
    user_id: str
    user_name: Optional[str]
    view_state: Optional[ViewState]

    def __init_subclass__(cls):
        super().__init_subclass__()
        HANDLER_REGISTRY.register_handler(cls)


def handle(request_type: RequestType, *args):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        nonlocal args
        keywords = []
        for keyword in args:
            if isinstance(keyword, str):
                keyword = re.compile("^" + keyword + "$")
            keywords.append(keyword)
        wrapper._handle = (request_type, keywords)
        return wrapper

    return decorator


def action(*args):
    return handle(RequestType.ACTION, *args)


def message(*args):
    return handle(RequestType.MESSAGE, *args)


def view_submission(*args):
    return handle(RequestType.VIEW_SUBMISSION, *args)


def view_closed(*args):
    return handle(RequestType.VIEW_CLOSED, *args)
