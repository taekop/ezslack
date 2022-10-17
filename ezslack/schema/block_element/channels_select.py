# type: ignore
from pydantic import constr
from typing import Literal, Optional


from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text


class ChannelsSelect(BaseModel):
    type: Literal["channels_select"] = "channels_select"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    initial_channel: Optional[str] = None
    confirm: Optional[ConfirmationDialog] = None
    response_url_enabled: Optional[bool] = None
    focus_on_load: Optional[bool] = None
