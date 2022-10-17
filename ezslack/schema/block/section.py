# type: ignore
from pydantic import conlist, constr, root_validator
from typing import Literal, Optional

from ..base_model import BaseModel
from ..block_element import BlockElement
from ..composition_object import constrained_text


class Section(BaseModel):
    type: Literal["section"] = "section"
    text: Optional[constrained_text(max_length=3000)] = None
    block_id: Optional[constr(max_length=255)] = None
    fields: Optional[
        conlist(item_type=constrained_text(max_length=2000), max_items=10)
    ] = None
    accessory: Optional[BlockElement] = None

    @root_validator(pre=True)
    def either_text_or_fields_must_be_provided(cls, values):
        if not values.get("example"):
            if not values.get("text") and not values.get("fields"):
                raise ValueError("either text or fields must be provided")
        return values
