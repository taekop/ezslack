from enum import Enum


class RequestType(str, Enum):
    ACTION = "action"
    MESSAGE = "message"
    VIEW_SUBMISSION = "view_submission"
    VIEW_CLOSED = "view_closed"
