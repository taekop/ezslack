from slack_sdk.models.views import ViewState
from typing import Optional

from .base import RequestBase


class ViewSubmission(RequestBase):
    def _private_metadata(self) -> Optional[str]:
        return self.body["view"]["private_metadata"]

    def _request_id(self) -> str:
        return self.body["view"]["callback_id"]

    def _user_id(self) -> str:
        return self.body["user"]["id"]

    def _user_name(self) -> Optional[str]:
        return self.body["user"]["name"]

    def _view_state(self) -> Optional[ViewState]:
        return ViewState(**self.body["view"]["state"])
