from typing import Annotated, Union

from pydantic import Field

from .button import Button
from .channels_select import ChannelsSelect
from .checkboxes import Checkboxes
from .conversations_select import ConversationsSelect
from .datepicker import Datepicker
from .external_select import ExternalSelect
from .image import Image
from .multi_channels_select import MultiChannelsSelect
from .multi_conversations_select import MultiConversationsSelect
from .multi_external_select import MultiExternalSelect
from .multi_static_select import MultiStaticSelect
from .multi_users_select import MultiUsersSelect
from .overflow import Overflow
from .plain_text_input import PlainTextInput
from .radio_buttons import RadioButtons
from .static_select import StaticSelect
from .timepicker import Timepicker
from .users_select import UsersSelect

SelectMenu = Annotated[
    Union[
        StaticSelect,
        ExternalSelect,
        UsersSelect,
        ConversationsSelect,
        ChannelsSelect,
    ],
    Field(discriminator="type"),
]

MultiSelectMenu = Annotated[
    Union[
        MultiStaticSelect,
        MultiExternalSelect,
        MultiUsersSelect,
        MultiConversationsSelect,
        MultiChannelsSelect,
    ],
    Field(discriminator="type"),
]
BlockElement = Annotated[
    Union[
        Button,
        Checkboxes,
        Datepicker,
        Image,
        Overflow,
        PlainTextInput,
        RadioButtons,
        Timepicker,
        SelectMenu,
        MultiSelectMenu,
    ],
    Field(discriminator="type"),
]
