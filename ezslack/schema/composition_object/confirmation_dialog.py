# type: ignore
from typing import Literal, Optional

from ..base_model import BaseModel
from .text import constrained_text, Text


class ConfirmationDialog(BaseModel):
    title: constrained_text(max_length=100, only_plain_text=True)
    text: constrained_text(max_length=300)
    confirm: constrained_text(max_length=30, only_plain_text=True)
    deny: constrained_text(max_length=30, only_plain_text=True)
    style: Optional[Literal["primary", "danger"]] = None
