# type: ignore
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel


class Divider(BaseModel):
    type: Literal["divider"] = "divider"
    block_id: Optional[constr(max_length=255)] = None
