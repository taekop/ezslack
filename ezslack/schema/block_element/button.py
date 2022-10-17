# type: ignore
from pydantic import constr
from typing import Literal, Optional


from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text


class Button(BaseModel):
    type: Literal["button"] = "button"
    text: constrained_text(max_length=75, only_plain_text=True)
    action_id: Optional[constr(max_length=255)] = None
    url: Optional[constr(max_length=3000)] = None
    value: Optional[constr(max_length=2000)] = None
    style: Optional[Literal["primary", "danger"]] = None
    confirm: Optional[ConfirmationDialog] = None
    accessibility_label: Optional[constr(max_length=75)] = None
