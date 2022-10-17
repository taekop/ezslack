# type: ignore
from pydantic import conint, constr
from typing import List, Literal, Optional

from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text, Filter


class MultiConversationsSelect(BaseModel):
    type: Literal["multi_conversations_select"] = "multi_conversations_select"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    initial_conversations: Optional[List[str]] = None
    default_to_current_conversation: Optional[bool] = None
    confirm: Optional[ConfirmationDialog] = None
    max_selected_items: Optional[conint(ge=1)] = None
    filter: Optional[Filter] = None
    focus_on_load: Optional[bool] = None
