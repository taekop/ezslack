from typing import List, Optional

from .base_model import BaseModel
from .block import Block


class Message(BaseModel):
    """legacy attachments not supported"""

    text: str
    blocks: Optional[List[Block]] = None
    thread_ts: Optional[str] = None
    mrkdwn: Optional[bool] = None
