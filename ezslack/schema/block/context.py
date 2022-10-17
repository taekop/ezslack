# type: ignore
from pydantic import Field, conlist, constr
from typing import Annotated, Literal, Optional, Union

from ..base_model import BaseModel
from ..block_element import Image
from ..composition_object import Text


class Context(BaseModel):
    type: Literal["context"] = "context"
    elements: conlist(
        item_type=Annotated[Union[Image, Text], Field(discriminator="type")],
        max_items=10,
    )
    block_id: Optional[constr(max_length=255)] = None
