# type: ignore
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text, Option


class ExternalSelect(BaseModel):
    type: Literal["external_select"] = "external_select"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    initial_option: Optional[Option] = None
    min_query_length: Optional[int] = None
    confirm: Optional[ConfirmationDialog] = None
    focus_on_load: Optional[bool] = None
