from typing import Annotated, Union

from pydantic import Field

from .actions import Actions
from .context import Context
from .divider import Divider
from .file import File
from .header import Header
from .image import Image
from .input import Input
from .section import Section
from .video import Video

Block = Annotated[
    Union[Actions, Context, Divider, File, Header, Image, Input, Section, Video],
    Field(discriminator="type"),
]
