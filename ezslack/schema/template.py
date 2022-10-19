from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel as PydanticBaseModel, validate_model
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union


class Expr(str):
    def eval(self, globals: Optional[Dict[str, Any]], locals: Optional[Dict[str, Any]]):
        return eval(self, globals, locals)


class TemplateBase(metaclass=ABCMeta):
    @abstractmethod
    def render(self, **locals) -> Any:
        pass


def _render(obj: Any, **locals) -> Tuple[Any, bool]:
    if isinstance(obj, list):
        return (_render_list(obj, None, **locals), False)
    elif isinstance(obj, Expr):
        return (obj.eval(None, locals), False)
    elif isinstance(obj, Template):
        return (obj.render(**locals), False)
    elif isinstance(obj, ConditionalTemplate):
        return (obj.render(**locals), False)
    elif isinstance(obj, CompositeTemplate):
        return (obj.render(**locals), obj.flat)
    elif isinstance(obj, IterableTemplate):
        return (obj.render(**locals), obj.flat)
    else:
        return (obj, False)


def _render_list(
    items: List[Any], locals_per_item: Optional[List[Dict[str, Any]]] = None, **locals
) -> List[Any]:
    output = []
    if locals_per_item is None:
        locals_per_item = [{}] * len(items)
    for item, additional_locals in zip(items, locals_per_item):
        _output, flat = _render(item, **locals, **additional_locals)
        if _output is None and isinstance(item, ConditionalTemplate):
            continue
        if flat:
            output += _output
        else:
            output.append(_output)
    return output


T = TypeVar("T", bound=PydanticBaseModel)


@dataclass
class Template(Generic[T], TemplateBase):
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

    def with_condition(self, condition: Expr):
        return ConditionalTemplate(condition, self)

    def to_iterable_template(
        self, iterable: Expr, name: str, flat: bool
    ) -> IterableTemplate:
        return IterableTemplate(iterable, name, self, flat)

    def __add__(self, other) -> CompositeTemplate:
        if isinstance(other, CompositeTemplate):
            return CompositeTemplate([self] + other.renderables)
        else:
            return CompositeTemplate([self, other])


@dataclass
class ConditionalTemplate(TemplateBase):
    condition: Expr
    renderable: Any

    def render(self, **locals) -> Any:
        if self.condition.eval(None, locals):
            return _render(self.renderable, **locals)[0]
        else:
            return None

    def with_condition(self, condition: Expr):
        return ConditionalTemplate(condition, self)

    def to_iterable_template(
        self, iterable: Expr, name: str, flat: bool
    ) -> IterableTemplate:
        return IterableTemplate(iterable, name, self, flat)

    def __add__(self, other) -> CompositeTemplate:
        if isinstance(other, CompositeTemplate):
            return CompositeTemplate([self] + other.renderables)
        else:
            return CompositeTemplate([self, other])


@dataclass
class CompositeTemplate(TemplateBase):
    renderables: List[Any]
    flat: bool = False

    def render(self, **locals) -> List[Any]:
        return _render_list(self.renderables, None, **locals)

    def to_iterable_template(
        self, iterable: Expr, name: str, flat: bool
    ) -> IterableTemplate:
        return IterableTemplate(iterable, name, self, flat)

    def __add__(self, other) -> CompositeTemplate:
        if isinstance(other, CompositeTemplate):
            return CompositeTemplate(self.renderables + other.renderables)
        else:
            return CompositeTemplate(self.renderables + [other])


@dataclass
class IterableTemplate(TemplateBase):
    iterable: Expr
    name: str
    renderable: Any
    flat: bool = False

    def render(self, **locals) -> List[Any]:
        values = self.iterable.eval(None, locals)
        renderables = [self.renderable] * len(values)
        locals_per_item = [{self.name: value} for value in values]
        return _render_list(renderables, locals_per_item, **locals)

    def __add__(self, other) -> CompositeTemplate:
        if isinstance(other, CompositeTemplate):
            return CompositeTemplate([self] + other.renderables)
        else:
            return CompositeTemplate([self, other])
