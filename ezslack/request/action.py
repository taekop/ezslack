from slack_sdk.models.metadata import Metadata
from slack_sdk.models.views import ViewState
from typing import Optional

from .base import RequestBase


class Action(RequestBase):
    def _channel_id(self) -> Optional[str]:
        return self.body["channel"]["id"]

    def _channel_name(self) -> Optional[str]:
        return self.body["channel"]["name"]

    def _message_ts(self) -> Optional[str]:
        return self.body["container"]["message_ts"]

    def _metadata(self) -> Optional[Metadata]:
        metadata = self.body["message"].get("metadata")
        if metadata:
            return Metadata(**metadata)
        else:
            return None

    def _request_id(self) -> str:
        return self.body["actions"][0]["action_id"]

    def _thread_ts(self) -> Optional[str]:
        if "message" in self.body:
            return self.body["message"].get("thread_ts") or self.body["message"].get(
                "ts"
            )
        else:
            return None

    def _trigger_id(self) -> Optional[str]:
        return self.body["trigger_id"]

    def _user_id(self) -> str:
        return self.body["user"]["id"]

    def _user_name(self) -> Optional[str]:
        return self.body["user"]["name"]
