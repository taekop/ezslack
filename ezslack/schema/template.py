from __future__ import annotations

from dataclasses import dataclass
from pydantic import BaseModel as PydanticBaseModel, validate_model
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union


class Expr(str):
    def eval(self, globals: Optional[Dict[str, Any]], locals: Optional[Dict[str, Any]]):
        return eval(self, globals, locals)


def _render(obj, **locals) -> Tuple[Any, bool]:
    if isinstance(obj, list):
        return (_render_list(obj, **locals), False)
    elif isinstance(obj, Expr):
        return (obj.eval(None, locals), False)
    elif isinstance(obj, Template):
        return (obj.render(**locals), False)
    elif isinstance(obj, CompositeTemplate):
        return (obj.render(**locals), True)
    elif isinstance(obj, IterableTemplate):
        return (obj.render(**locals), obj.flat)
    else:
        return (obj, False)


def _render_list(items, **locals) -> List[Any]:
    output = []
    for item in items:
        _output, flat = _render(item, **locals)
        if flat:
            output += _output
        else:
            output.append(_output)
    return output


T = TypeVar("T", bound=PydanticBaseModel)


@dataclass
class Template(Generic[T]):
    example: T
    locals: Dict[str, Any]
    sub_templates: Dict[str, Any]

    def render(self, **locals) -> T:
        locals.update(self.locals)

        output = self.example.copy(deep=True)
        for k, v in self.sub_templates.items():
            output.__setattr__(k, _render(v, **locals)[0])

        _, _, err = validate_model(output.__class__, output.__dict__)
        if err:
            raise err
        return output

    def update_locals(self, **locals):
        self.locals.update(locals)

    def to_iterable_template(
        self, iterable: Expr, name: str, flat: bool
    ) -> IterableTemplate:
        return IterableTemplate(iterable, name, self, flat)

    def __add__(self, other) -> CompositeTemplate:
        if isinstance(other, Template):
            return CompositeTemplate([self, other])
        elif isinstance(other, CompositeTemplate):
            return CompositeTemplate([self] + other.templates)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +: '{self.__class__}' and '{type(other)}'"
            )


@dataclass
class CompositeTemplate:
    templates: List[Union[Template, CompositeTemplate]]

    def render(self, **locals) -> List[Any]:
        output = []
        for template in self.templates:
            _output, flat = _render(template, **locals)
            if flat:
                output += _output
            else:
                output.append(_output)
        return output

    def to_iterable_template(
        self, iterable: Expr, name: str, flat: bool
    ) -> IterableTemplate:
        return IterableTemplate(iterable, name, self, flat)

    def __add__(self, other) -> CompositeTemplate:
        if isinstance(other, Template):
            return CompositeTemplate(self.templates + [other])
        elif isinstance(other, CompositeTemplate):
            return CompositeTemplate(self.templates + other.templates)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +: '{self.__class__}' and '{type(other)}'"
            )


@dataclass
class IterableTemplate:
    iterable: Expr
    name: str
    template: Union[Template, CompositeTemplate]
    flat: bool

    def render(self, **locals) -> List[Any]:
        output = []
        for item in self.iterable.eval(None, locals):
            _output, flat = _render(self.template, **locals, **{self.name: item})
            if flat:
                output += _output
            else:
                output.append(_output)
        return output
