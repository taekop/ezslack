from typing import Optional

from .base import RequestBase


class Message(RequestBase):
    def _channel_id(self) -> Optional[str]:
        return self.body["event"]["channel"]

    def _message_ts(self) -> Optional[str]:
        return self.body["event"]["ts"]

    def _request_id(self) -> str:
        return self.body["event"]["text"]

    def _thread_ts(self) -> Optional[str]:
        return self.body["event"].get("thread_ts") or self._message_ts()

    def _user_id(self) -> str:
        return self.body["event"]["user"]
