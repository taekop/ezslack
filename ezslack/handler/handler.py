from dataclasses import dataclass
from slack_bolt import Ack, Respond, Say
from slack_sdk.web import WebClient
from slack_sdk.models.metadata import Metadata
from slack_sdk.models.views import ViewState
from typing import Optional


@dataclass
class Handler:
    # interaction
    ack: Ack
    client: WebClient
    respond: Respond
    say: Say

    # data
    channel_id: Optional[str]
    channel_name: Optional[str]
    message_ts: Optional[str]
    metadata: Optional[Metadata]
    private_metadata: Optional[str]
    request_id: str
    thread_ts: Optional[str]
    trigger_id: Optional[str]
    user_id: str
    user_name: Optional[str]
    view_state: Optional[ViewState]

    def __init_subclass__(cls):
        super().__init_subclass__()
        for mtd in cls.__dict__.values():
            if callable(mtd) and (_handle := getattr(mtd, "_handle", None)):
                for registry, keyword in _handle:
                    registry.set(cls, mtd.__name__, keyword)
