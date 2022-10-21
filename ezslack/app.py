import re
from typing import Any, Dict, Optional, Tuple
from slack_bolt import Ack, App as SlackBoltApp, Respond, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.models.views import ViewState

from .handler import HANDLER_REGISTRY
from .types import RequestType


def extract_request_id(
    request_type: RequestType,
    action: Optional[Dict[str, Any]],
    message: Optional[Dict[str, Any]],
    view: Optional[Dict[str, Any]],
):
    match request_type:
        case RequestType.ACTION:
            assert action is not None
            return action["action_id"]
        case RequestType.MESSAGE:
            assert message is not None
            return message["text"]
        case _:
            assert view is not None
            return view["callback_id"]


def extract_body_fields(
    request_type: RequestType, body: Dict[str, Any]
) -> Tuple[
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    str,
    Optional[str],
    Optional[ViewState],
]:
    match request_type:
        case RequestType.ACTION:
            channel_id = body["channel"]["id"]
            channel_name = body["channel"]["name"]
            message_ts = body["container"]["message_ts"]
            private_metadata = None
            thread_ts = body["container"].get("thread_ts") or body["container"]["ts"]
            trigger_id = body["trigger_id"]
            user_id = body["user"]["id"]
            user_name = body["user"]["name"]
            view_state = None
        case RequestType.MESSAGE:
            channel_id = body["event"]["channel"]
            channel_name = None
            message_ts = body["event"]["ts"]
            private_metadata = None
            thread_ts = body["event"].get("thread_ts") or message_ts
            trigger_id = None
            user_id = body["event"]["user"]
            user_name = None
            view_state = None
        case _:
            channel_id = None
            channel_name = None
            message_ts = None
            private_metadata = body["view"]["private_metadata"]
            thread_ts = None
            trigger_id = None
            user_id = body["user"]["id"]
            user_name = body["user"]["name"]
            view_state = ViewState(**body["view"]["state"])
    return (
        channel_id,
        channel_name,
        message_ts,
        private_metadata,
        thread_ts,
        trigger_id,
        user_id,
        user_name,
        view_state,
    )


def route(request_type: RequestType):
    def handle(
        ack: Ack,
        body: Dict[str, Any],
        client: WebClient,
        respond: Respond,
        say: Say,
        action: Optional[Dict[str, Any]],
        message: Optional[Dict[str, Any]],
        view: Optional[Dict[str, Any]],
    ):
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
