# type: ignore
from pydantic import constr
from typing import Literal, Optional


from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text, Filter


class ConversationsSelect(BaseModel):
    type: Literal["conversations_select"] = "conversations_select"
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    action_id: Optional[constr(max_length=255)] = None
    initial_conversation: Optional[str] = None
    default_to_current_conversation: Optional[bool] = None
    confirm: Optional[ConfirmationDialog] = None
    response_url_enabled: Optional[bool] = None
    filter: Optional[Filter] = None
    focus_on_load: Optional[bool] = None
