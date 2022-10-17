# type: ignore
from pydantic import conint, constr
from typing import List, Literal, Optional

from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text, Option


class MultiExternalSelect(BaseModel):
    type: Literal["multi_external_select"] = "multi_external_select"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    min_query_length: Optional[int] = None
    initial_options: Optional[List[Option]] = None
    confirm: Optional[ConfirmationDialog] = None
    max_selected_items: Optional[conint(ge=1)] = None
    focus_on_load: Optional[bool] = None
