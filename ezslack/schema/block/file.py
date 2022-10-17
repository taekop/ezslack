# type: ignore
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel


class File(BaseModel):
    type: Literal["file"] = "file"
    external_id: str
    source: str
    block_id: Optional[constr(max_length=255)] = None
