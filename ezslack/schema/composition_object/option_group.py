# type: ignore
from pydantic import conlist

from ..base_model import BaseModel
from .option import Option
from .text import constrained_text


class OptionGroup(BaseModel):
    label: constrained_text(max_length=75, only_plain_text=True)
    options: conlist(item_type=Option, max_items=100)
