# type: ignore
from pydantic import conlist, constr, validator
from typing import List, Literal, Optional


from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, Option


class Checkboxes(BaseModel):
    type: Literal["checkboxes"] = "checkboxes"
    action_id: Optional[constr(max_length=255)] = None
    options: conlist(item_type=Option, max_items=10)
    initial_options: Optional[List[Option]] = None
    confirm: Optional[ConfirmationDialog] = None
    focus_on_load: Optional[bool] = None

    @validator("initial_options")
    def initial_options_must_be_included_in_options(cls, v, values):
        if v is not None:
            for initial_option in v:
                if initial_option not in values["options"]:
                    raise ValueError("must be included in options")
        return v
