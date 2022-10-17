# type: ignore
from pydantic import conlist, constr, validator
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, Option


class RadioButtons(BaseModel):
    type: Literal["radio_buttons"] = "radio_buttons"
    action_id: Optional[constr(max_length=255)] = None
    options: conlist(item_type=Option, max_items=10)
    initial_option: Optional[Option] = None
    confirm: Optional[ConfirmationDialog] = None
    focus_on_load: Optional[bool] = None

    @validator("initial_option")
    def initial_option_must_be_included_in_option(cls, v, values):
        if v is not None and v not in values["options"]:
            raise ValueError("must be included in options")
        return v
