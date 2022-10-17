from typing import Literal

from ..base_model import BaseModel


class Image(BaseModel):
    type: Literal["image"] = "image"
    image_url: str
    alt_text: str
