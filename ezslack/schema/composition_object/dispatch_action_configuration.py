# type: ignore
from typing import List, Literal, Optional

from ..base_model import BaseModel


class DispatchActionConfiguration(BaseModel):
    trigger_actions_on: Optional[
        List[Literal["on_enter_pressed", "on_character_entered"]]
    ] = None
