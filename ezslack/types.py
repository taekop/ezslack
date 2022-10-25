from dataclasses import dataclass
from enum import Enum
from typing import Optional

from slack_sdk.models.metadata import Metadata
from slack_sdk.models.views import ViewState


@dataclass
class BodyFields:
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


class RequestType(str, Enum):
    ACTION = "action"
    MESSAGE = "message"
    VIEW_SUBMISSION = "view_submission"
    VIEW_CLOSED = "view_closed"
