from __future__ import annotations

from dataclasses import dataclass
from pydantic import BaseModel as PydanticBaseModel, validate_model
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union


class Expr(str):
    def eval(self, globals: Optional[Dict[str, Any]], locals: Optional[Dict[str, Any]]):
        return eval(self, globals, locals)


T = TypeVar("T", bound=PydanticBaseModel)


@dataclass
class Template(Generic[T]):
    example: T
    sub_templates: Dict[str, Union[list, Expr, Template, TemplateList]]

    def render(self, **locals) -> T:
        def _render(obj, locals):
            if isinstance(obj, list):
                return [_render(item, locals) for item in obj]
            elif isinstance(obj, Expr):
                return obj.eval(None, locals)
            elif isinstance(obj, self.__class__):
                return obj.render(**locals)
            elif isinstance(obj, TemplateList):
                return obj.render(**locals)
            else:
                return obj

        output = self.example.copy(deep=True)
        for k, v in self.sub_templates.items():
            output.__setattr__(k, _render(v, locals))

        _, _, err = validate_model(output.__class__, output.__dict__)
        if err:
            raise err
        return output


@dataclass
class TemplateList(Generic[T]):
    iterable: Expr
    name: str
    template: Template[T]

    def render(self, **locals) -> List[T]:
        return [
            self.template.render(**locals, **{self.name: item})
            for item in self.iterable.eval(None, locals)
        ]
