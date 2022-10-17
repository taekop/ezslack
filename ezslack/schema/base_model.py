from pydantic import BaseModel as PydanticBaseModel, ConstrainedList
from types import NoneType
from typing import Annotated, List, Literal, TypeVar, Union, get_args, get_origin

from .template import Expr, Template, TemplateList

AnyBaseModel = TypeVar("AnyBaseModel", bound="BaseModel")


class BaseModel(PydanticBaseModel):
    @classmethod
    def example(cls):
        def _example(outer_type, required: bool):
            if not required:
                return None
            if origin_type := get_origin(outer_type):
                inner_type = get_args(outer_type)[0]
                required = NoneType not in get_args(inner_type)
                if origin_type is list or origin_type is List:
                    return [_example(inner_type, required)]
                elif origin_type is Literal:
                    return inner_type
                elif origin_type is Union:
                    return _example(inner_type, required)
                elif origin_type is Annotated:
                    return _example(inner_type, required)
                else:
                    raise NotImplementedError
            else:
                if issubclass(outer_type, int):
                    return 1
                elif issubclass(outer_type, float):
                    return 1.0
                elif issubclass(outer_type, str):
                    return "string"
                elif isinstance(outer_type, type) and issubclass(
                    outer_type, ConstrainedList
                ):
                    return [_example(outer_type.item_type, True)]
                else:
                    return outer_type.example()  # type: ignore

        return cls(
            example=True,  # type: ignore
            **{
                field.name: _example(field.outer_type_, not field.allow_none)
                for field in cls.__fields__.values()
            },
        )

    @classmethod
    def template(cls: type[AnyBaseModel], **kwargs) -> Template[AnyBaseModel]:
        example = cls.example()
        sub_templates = {}
        for k, v in kwargs.items():
            if isinstance(v, Union[list, Expr, Template, TemplateList]):
                sub_templates[k] = v
            else:
                example.__setattr__(k, v)
        return Template(example, sub_templates)
