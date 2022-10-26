from abc import ABC, abstractmethod
from slack_sdk.models.metadata import Metadata
from slack_sdk.models.views import ViewState
from typing import Any, Dict, Optional


class RequestBase(ABC):
    body: Dict[str, Any]

    def __init__(self, body: Dict[str, Any]):
        self.body = body

    def data(self) -> Dict[str, Any]:
        return {
            "channel_id": self._channel_id(),
            "channel_name": self._channel_name(),
            "message_ts": self._message_ts(),
            "metadata": self._metadata(),
            "private_metadata": self._private_metadata(),
            "request_id": self._request_id(),
            "thread_ts": self._thread_ts(),
            "trigger_id": self._trigger_id(),
            "user_id": self._user_id(),
            "user_name": self._user_name(),
            "view_state": self._view_state(),
        }

    def _channel_id(self) -> Optional[str]:
        return None

    def _channel_name(self) -> Optional[str]:
        return None

    def _message_ts(self) -> Optional[str]:
        return None

    def _metadata(self) -> Optional[Metadata]:
        return None

    def _private_metadata(self) -> Optional[str]:
        return None

    @abstractmethod
    def _request_id(self) -> str:
        pass

    def _thread_ts(self) -> Optional[str]:
        return None

    def _trigger_id(self) -> Optional[str]:
        return None

    @abstractmethod
    def _user_id(self) -> str:
        pass

    def _user_name(self) -> Optional[str]:
        return None

    def _view_state(self) -> Optional[ViewState]:
        return None
