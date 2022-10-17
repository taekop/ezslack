# type: ignore
from datetime import date
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text


class Datepicker(BaseModel):
    type: Literal["datepicker"] = "datepicker"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    initial_date: Optional[date] = None
    confirm: Optional[ConfirmationDialog] = None
    focus_on_load: Optional[bool] = None
