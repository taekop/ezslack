# type: ignore
from pydantic import conlist, constr, root_validator, validator
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import (
    ConfirmationDialog,
    constrained_text,
    Option,
    OptionGroup,
)


class StaticSelect(BaseModel):
    type: Literal["static_select"] = "static_select"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    options: Optional[conlist(item_type=Option, max_items=100)] = None
    option_groups: Optional[conlist(item_type=OptionGroup, max_items=100)] = None
    initial_option: Optional[Option] = None
    confirm: Optional[ConfirmationDialog] = None
    focus_on_load: Optional[bool] = None

    @root_validator(pre=True)
    def either_options_or_option_groups_must_be_provided(cls, values):
        if not values.get("example"):
            if not values.get("options") and not values.get("option_groups"):
                raise ValueError("either options or option groups must be provided")
        return values

    @validator("initial_option")
    def initial_option_must_be_included_in_options_or_options_groups(cls, v, values):
        if v is not None:
            if values["options"]:
                if v not in values["options"]:
                    raise ValueError("must be included in options")
            else:
                options = [
                    option
                    for option_group in values["options_groups"]
                    for option in option_group.options
                ]
                if v not in options:
                    raise ValueError("must be included in option groups")
        return v
