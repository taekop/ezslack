import re
from typing import Any, Dict, Type
from slack_bolt import Ack, App as SlackBoltApp, Respond, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from .handler import REGISTRIES
from .request import Action, Message, Request, ViewClosed, ViewSubmission


def route(cls: Type[Request]):
    registry = REGISTRIES[cls.__name__]

    def handle(
        ack: Ack,
        body: Dict[str, Any],
        client: WebClient,
        respond: Respond,
        say: Say,
    ):
        request = cls(body)
        request_id = request._request_id()
        if handler_mtd_args := registry.get(request_id):
            handler, mtd, args, kwargs = handler_mtd_args
            handler_instance = handler(ack, client, respond, say, **request.data())
            getattr(handler_instance, mtd)(*args, **kwargs)

    return handle


class App:
    def __init__(self, *args, **kwargs):
        self.inner = SlackBoltApp(*args, **kwargs)

        any = re.compile(".*")
        self.inner.action(any)(route(Action))
        self.inner.message(any)(route(Message))
        self.inner.view_closed(any)(route(ViewClosed))
        self.inner.view_submission(any)(route(ViewSubmission))

    def start(self, *args, **kwargs):
        self.inner.start(*args, **kwargs)

    def start_socket_mode(self, *args, **kwargs):
        SocketModeHandler(self.inner, *args, **kwargs).start()
