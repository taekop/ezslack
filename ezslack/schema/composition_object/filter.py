# type: ignore
from pydantic import conlist
from typing import Literal, Optional

from ..base_model import BaseModel


class Filter(BaseModel):
    include: Optional[
        conlist(item_type=Literal["im", "mpim", "private", "public"], min_items=1)
    ] = None
    exclude_external_shared_channels: Optional[bool] = None
    exclude_bot_users: Optional[bool] = None
