# type: ignore
from pydantic import conint, conlist, constr, root_validator, validator
from typing import List, Literal, Optional

from ..base_model import BaseModel
from ..composition_object import (
    ConfirmationDialog,
    constrained_text,
    Option,
    OptionGroup,
)


class MultiStaticSelect(BaseModel):
    type: Literal["multi_static_select"] = "multi_static_select"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    options: Optional[conlist(item_type=Option, max_items=100)] = None
    option_groups: Optional[conlist(item_type=OptionGroup, max_items=100)] = None
    initial_options: Optional[List[Option]] = None
    confirm: Optional[ConfirmationDialog] = None
    max_selected_items: Optional[conint(ge=1)] = None
    focus_on_load: Optional[bool] = None

    @root_validator(pre=True)
    def either_options_or_option_groups_must_be_provided(cls, values):
        if not values.get("example"):
            if not values.get("options") and not values.get("option_groups"):
                raise ValueError("either options or option groups must be provided")
        return values

    @validator("initial_options")
    def initial_options_must_be_included_in_options_or_options_groups(cls, v, values):
        if v is not None:
            if values["options"]:
                for initial_option in v:
                    if initial_option not in values["options"]:
                        raise ValueError("must be included in options")
            else:
                options = [
                    option
                    for option_group in values["options_groups"]
                    for option in option_group.options
                ]
                for initial_option in v:
                    if initial_option not in options:
                        raise ValueError("must be included in option groups")
        return v
