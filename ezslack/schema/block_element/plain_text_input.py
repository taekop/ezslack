# type: ignore
from pydantic import conint, constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import DispatchActionConfiguration, constrained_text


class PlainTextInput(BaseModel):
    type: Literal["plain_text_input"] = "plain_text_input"
    action_id: Optional[constr(max_length=255)] = None
    placeholder: Optional[constrained_text(max_length=150, only_plain_text=True)] = None
    initial_value: Optional[str] = None
    multiline: Optional[bool] = None
    min_length: Optional[conint(le=3000)] = None
    max_length: Optional[int] = None
    dispatch_action_config: Optional[DispatchActionConfiguration] = None
    focus_on_load: Optional[bool] = None
