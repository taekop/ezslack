from unittest import TestCase

from ezslack.schema import (
    Expr,
    CompositeTemplate,
    ConditionalTemplate,
    IterableTemplate,
)
from tests.schema import Either, Menu, Text


class TemplateTest(TestCase):
    def test_render_expr(self):
        expr = Expr("data['text']")
        value = expr.eval(None, {"data": {"text": "ezslack"}})
        self.assertEqual("ezslack", value)

    def test_render_template(self):
        text_template = Text.template(text=Expr("data['text']"))
        text = text_template.render(data={"text": "ezslack"})
        self.assertEqual(Text(text="ezslack"), text)

    def test_render_list(self):
        menu_template = Menu.template(
            options=[
                Text.template(text=Expr("options[0]")),
                Text.template(text=Expr("options[1]")),
            ]
        )
        menu = menu_template.render(options=["0", "1"])
        self.assertEqual(
            Menu(options=[Text(text="0"), Text(text="1")]),
            menu,
        )

    def test_render_raise_validation_error_(self):
        either_template = Either.template()
        self.assertRaises(ValueError, either_template.render)

    def test_update_locals(self):
        text_template = Text.template(text=Expr("data['text']"))
        text_template.update_locals(data={"text": "ezslack"})
        text = text_template.render()
        self.assertEqual(Text(text="ezslack"), text)

    def test_template_with_condition(self):
        text_template = Text.template(text=Expr("data['text']"))
        with_condition = text_template.with_condition(Expr("condition"))
        self.assertEqual(
            ConditionalTemplate(Expr("condition"), text_template), with_condition
        )

    def test_template_to_iterable_template(self):
        template = Text.template(text=Expr("value"))
        iterable_template = template.to_iterable_template(Expr("texts"), "value", True)
        self.assertEqual(
            IterableTemplate(
                Expr("texts"), "value", Text.template(text=Expr("value")), True
            ),
            iterable_template,
        )

    def test_add_template_and_condition_template_and_composite_template(self):
        first_name_template = Text.template(text=Expr("data['first_name']"))
        middle_name_template = Text.template(
            text=Expr("data['middle_name']")
        ).with_condition(Expr("'middle_name' in data"))
        last_name_template = Text.template(text=Expr("data['last_name']"))
        name_template = first_name_template + middle_name_template + last_name_template
        email_template = Text.template(text=Expr("data['email']"))
        profile_template = name_template + email_template
        self.assertEqual(
            CompositeTemplate(
                [
                    first_name_template,
                    middle_name_template,
                    last_name_template,
                    email_template,
                ]
            ),
            profile_template,
        )

    def test_render_conditional_template(self):
        text_template = ConditionalTemplate(
            Expr("condition"), Text.template(text=Expr("data"))
        )
        with_condition = text_template.render(data="ezslack", condition=True)
        without_condition = text_template.render(data="ezslack", condition=False)
        self.assertEqual(with_condition, Text(text="ezslack"))
        self.assertEqual(without_condition, None)

    def test_render_composite_template(self):
        first_name_template = Text.template(text=Expr("data['first_name']"))
        middle_name_template = Text.template(
            text=Expr("data['middle_name']")
        ).with_condition(Expr("'middle_name' in data"))
        last_name_template = Text.template(text=Expr("data['last_name']"))
        name_template = CompositeTemplate(
            [first_name_template, middle_name_template, last_name_template]
        )

        short_name = name_template.render(
            data={"first_name": "first", "last_name": "last"}
        )
        self.assertEqual(
            [
                Text(text="first"),
                Text(text="last"),
            ],
            short_name,
        )

        long_name = name_template.render(
            data={"first_name": "first", "middle_name": "middle", "last_name": "last"}
        )
        self.assertEqual(
            [
                Text(text="first"),
                Text(text="middle"),
                Text(text="last"),
            ],
            long_name,
        )

    def test_composite_template_to_iterable_template(self):
        composite_template = CompositeTemplate([Text.template(text=Expr("value"))])
        iterable_text_template = composite_template.to_iterable_template(
            Expr("texts"), "value", True
        )
        self.assertEqual(
            IterableTemplate(
                Expr("texts"),
                "value",
                CompositeTemplate([Text.template(text=Expr("value"))]),
                True,
            ),
            iterable_text_template,
        )

    def test_render_iterable_template(self):
        options_template = IterableTemplate(
            Expr("options"), "option", Text.template(text=Expr("option")), False
        )
        options = options_template.render(options=["0", "1", "2"])
        self.assertEqual(
            [
                Text(text="0"),
                Text(text="1"),
                Text(text="2"),
            ],
            options,
        )
