from pydantic import root_validator
from typing import List, Optional


from ezslack.schema import BaseModel


class Text(BaseModel):
    text: str


class Menu(BaseModel):
    options: List[Text]


class Either(BaseModel):
    left: Optional[str]
    right: Optional[str]

    @root_validator(pre=True)
    def either_left_or_right_must_be_provided(cls, values):
        if not values.get("example"):
            if not values.get("left") and not values.get("right"):
                raise ValueError("either left or right must be provided")
        return values
