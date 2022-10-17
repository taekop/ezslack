# type: ignore
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import constrained_text


class Header(BaseModel):
    type: Literal["header"] = "header"
    text: constrained_text(max_length=150, only_plain_text=True)
    block_id: Optional[constr(max_length=255)] = None
