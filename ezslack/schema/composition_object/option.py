# type: ignore
from pydantic import constr
from typing import Optional

from ..base_model import BaseModel
from .text import constrained_text


class Option(BaseModel):
    text: constrained_text(only_plain_text=True)
    value: constr(max_length=75)
    description: Optional[constrained_text(max_length=75, only_plain_text=True)] = None
    url: Optional[constr(max_length=3000)] = None
