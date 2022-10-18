import re
from typing import Optional, Tuple
from slack_bolt import App as SlackBoltApp
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .handler import HANDLER_REGISTRY
from .types import RequestType


def extract_request_id(request_type, action, message, view):
    match request_type:
        case RequestType.ACTION:
            return action["action_id"]
        case RequestType.MESSAGE:
            return message["text"]
        case _:
            return view["callback_id"]


def extract_body_fields(
    request_type, body
) -> Tuple[
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    str,
    Optional[str],
]:
    match request_type:
        case RequestType.ACTION:
            channel_id = body["channel"]["id"]
            channel_name = body["channel"]["name"]
            message_ts = body["container"]["message_ts"]
            thread_ts = body["container"].get("thread_ts") or body["container"]["ts"]
            trigger_id = body["trigger_id"]
            user_id = body["user"]["id"]
            user_name = body["user"]["name"]
        case RequestType.MESSAGE:
            channel_id = body["event"]["channel"]
            channel_name = None
            message_ts = body["event"]["ts"]
            thread_ts = body["event"].get("thread_ts") or message_ts
            trigger_id = None
            user_id = body["event"]["user"]
            user_name = None
        case _:
            channel_id = None
            channel_name = None
            message_ts = None
            thread_ts = None
            trigger_id = None
            user_id = body["user"]["id"]
            user_name = body["user"]["name"]
    return (
        channel_id,
        channel_name,
        message_ts,
        thread_ts,
        trigger_id,
        user_id,
        user_name,
    )


def route(request_type: RequestType):
    def handle(ack, body, client, respond, say, action, message, view):
        request_id = extract_request_id(request_type, action, message, view)
        if handler_mtd_args := HANDLER_REGISTRY.search_handler(
            request_type, request_id
        ):
            fields = extract_body_fields(request_type, body)

            handler, mtd, args, kwargs = handler_mtd_args
            handler_instance = handler(
                request_id, request_type, ack, body, client, respond, say, *fields
            )
            getattr(handler_instance, mtd)(*args, **kwargs)

    return handle


class App:
    def __init__(self, *args, **kwargs):
        self.inner = SlackBoltApp(*args, **kwargs)

        any = re.compile(".*")
        self.inner.action(any)(route(RequestType.ACTION))
        self.inner.message(any)(route(RequestType.MESSAGE))
        self.inner.view_submission(any)(route(RequestType.VIEW_SUBMISSION))
        self.inner.view_closed(any)(route(RequestType.VIEW_CLOSED))

    def start(self, *args, **kwargs):
        self.inner.start(*args, **kwargs)

    def start_socket_mode(self, *args, **kwargs):
        SocketModeHandler(self.inner, *args, **kwargs).start()
