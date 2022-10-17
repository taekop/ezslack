# type: ignore
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import constrained_text


class Image(BaseModel):
    type: Literal["image"] = "image"
    image_url: constr(max_length=3000)
    alt_text: constr(max_length=2000)
    title: Optional[constrained_text(max_length=2000, only_plain_text=True)] = None
    block_id: Optional[constr(max_length=255)] = None
