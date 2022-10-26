from typing import Union

from .action import Action
from .message import Message
from .view_closed import ViewClosed
from .view_submission import ViewSubmission

Request = Union[Action, Message, ViewClosed, ViewSubmission]
