# type: ignore
from pydantic import constr
from typing import Literal, Optional

from ..base_model import BaseModel
from ..composition_object import constrained_text


class Video(BaseModel):
    type: Literal["video"] = "video"
    alt_text: str
    author_name: Optional[constr(max_length=49)] = None
    block_id: Optional[constr(max_length=255)] = None
    description: Optional[constrained_text(only_plain_text=True)] = None
    provider_icon_url: Optional[str] = None
    provider_name: Optional[str] = None
    title: constrained_text(max_length=200, only_plain_text=True)
    title_url: Optional[str] = None
    thumbnail_url: str
    video_url: str
