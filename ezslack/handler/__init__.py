import functools
import re

from .handler import Handler
from .registry import HandlerRegistry, REGISTRIES


def handle(registry: HandlerRegistry, *args):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        keywords = []
        for keyword in args:
            if isinstance(keyword, str):
                keyword = re.compile("^" + keyword + "$")
            keywords.append(keyword)

        wrapper._handle = [(registry, keyword) for keyword in keywords]
        if _handle := getattr(function, "_handle", None):
            wrapper._handle += _handle

        return wrapper

    return decorator


def action(*args):
    return handle(REGISTRIES["Action"], *args)


def message(*args):
    return handle(REGISTRIES["Message"], *args)


def view_closed(*args):
    return handle(REGISTRIES["ViewClosed"], *args)


def view_submission(*args):
    return handle(REGISTRIES["ViewSubmission"], *args)
