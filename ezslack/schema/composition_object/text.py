# type: ignore
from pydantic import constr, validator
from pydantic.errors import AnyStrMaxLengthError, WrongConstantError
from typing import Literal, Optional

from ..base_model import BaseModel


class Text(BaseModel):
    type: Literal["plain_text", "mrkdwn"]
    text: constr(max_length=3000)
    emoji: Optional[bool] = None
    veratim: Optional[bool] = None

    @validator("emoji")
    def emoji_is_not_allowed_in_mrkdwn(cls, v, values):
        if values["type"] == "mrkdwn" and v is not None:
            raise ValueError("is not allowed in mrkdwn")
        return v

    @validator("veratim")
    def veratim_is_not_allowed_in_plain_text(cls, v, values):
        if values["type"] == "plain_text" and v is not None:
            raise ValueError("is not allowed in plain_text")
        return v

    @classmethod
    def example(cls):
        return cls(type="plain_text", text="text")


class ConstrainedText(Text):
    _max_length = None
    _only_plain_text = False

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, dict):
            v = Text(**v)
        if getattr(cls, "_only_plain_text", None):
            if v.type != "plain_text":
                raise WrongConstantError(given=v.type, permitted=["plain_text"])
        if max_length := getattr(cls, "_max_length", None):
            if len(v.text) > max_length:
                raise AnyStrMaxLengthError(limit_value=max_length)
        return v


def constrained_text(
    *, max_length: Optional[int] = None, only_plain_text: bool = False
):
    return type(
        "ConstrainedTextValue",
        (ConstrainedText,),
        {"_max_length": max_length, "_only_plain_text": only_plain_text},
    )
