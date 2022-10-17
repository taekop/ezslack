# type: ignore
from pydantic import conlist, constr, root_validator
from typing import Literal, Optional

from .base_model import BaseModel
from .block import Block, Input
from .composition_object import constrained_text


class View(BaseModel):
    type: Literal["modal", "home"]
    title: constrained_text(max_length=24, only_plain_text=True)
    blocks: conlist(item_type=Block, max_items=100)
    close: Optional[constrained_text(max_length=24, only_plain_text=True)] = None
    submit: Optional[constrained_text(max_length=24, only_plain_text=True)] = None
    private_metadata: Optional[constr(max_length=3000)] = None
    callback_id: Optional[constr(max_length=255)] = None
    clear_on_close: Optional[bool] = None
    notify_on_close: Optional[bool] = None
    external_id: Optional[str] = None
    submit_disabled: Optional[bool] = None

    @root_validator(pre=True)
    def submit_must_be_provided_if_input_block_is_provided(cls, values):
        if not values.get("submit"):
            for block in values["blocks"]:
                if isinstance(block, Input):
                    raise ValueError(
                        "submit must be provided if input block is provided"
                    )
        return values
