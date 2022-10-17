# type: ignore
from pydantic import Field, conlist, constr
from typing import Annotated, Literal, Optional, Union

from ..base_model import BaseModel
from ..block_element import Button, Datepicker, Overflow, SelectMenu


class Actions(BaseModel):
    type: Literal["actions"] = "actions"
    elements: conlist(
        item_type=Annotated[
            Union[Button, Datepicker, Overflow, SelectMenu], Field(discriminator="type")
        ],
        max_items=25,
    )
    block_id: Optional[constr(max_length=255)] = None
