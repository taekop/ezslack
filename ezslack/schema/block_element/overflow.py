# type: ignore
from pydantic import conlist, constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import ConfirmationDialog, Option


class Overflow(BaseModel):
    type: Literal["overflow"] = "overflow"
    action_id: Optional[constr(max_length=255)] = None
    options: conlist(item_type=Option, max_items=5)
    confirm: Optional[ConfirmationDialog] = None
