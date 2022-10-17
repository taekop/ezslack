# type: ignore
from datetime import time
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, constrained_text


class Timepicker(BaseModel):
    type: Literal["timepicker"] = "timepicker"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    initial_time: Optional[time] = None
    confirm: Optional[ConfirmationDialog] = None
    focus_on_load: Optional[bool] = None
