# type: ignore
from pydantic import Field, constr
from typing import Annotated, Literal, Optional, Union

from ..base_model import BaseModel
from ..block_element import (
    Checkboxes,
    Datepicker,
    MultiSelectMenu,
    PlainTextInput,
    RadioButtons,
    SelectMenu,
    Timepicker,
)
from ..composition_object import constrained_text


class Input(BaseModel):
    type: Literal["input"] = "input"
    label: constrained_text(max_length=2000, only_plain_text=True)
    element: Annotated[
        Union[
            Checkboxes,
            Datepicker,
            MultiSelectMenu,
            PlainTextInput,
            RadioButtons,
            SelectMenu,
            Timepicker,
        ],
        Field(discriminator="type"),
    ]
    dispatch_action: Optional[bool] = None
    block_id: Optional[constr(max_length=255)] = None
    hint: Optional[constrained_text(max_length=2000, only_plain_text=True)] = None
    optional: Optional[bool] = None
