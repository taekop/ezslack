from unittest import TestCase

from ezslack.schema import Expr, CompositeTemplate, IterableTemplate
from tests.schema import Either, Menu, Text


class TemplateTest(TestCase):
    def test_render_expr(self):
        expr = Expr("data['text']")
        value = expr.eval(None, {"data": {"text": "ezslack"}})
        self.assertEqual("ezslack", value)

    def test_render_template(self):
        text_template = Text.template(text=Expr("data['text']"))
        text = text_template.render(data={"text": "ezslack"})
        self.assertEqual(Text(type="plain_text", text="ezslack"), text)

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
        self.assertEqual(Text(type="plain_text", text="ezslack"), text)

    def test_add_two_templates(self):
        first_name_template = Text.template(text=Expr("data['first_name']"))
        last_name_template = Text.template(text=Expr("data['last_name']"))
        name_template = CompositeTemplate([first_name_template, last_name_template])
        self.assertEqual(name_template, first_name_template + last_name_template)

    def test_add_template_and_composite_template(self):
        first_name_template = Text.template(text=Expr("data['first_name']"))
        last_name_template = Text.template(text=Expr("data['last_name']"))
        name_template = CompositeTemplate([first_name_template, last_name_template])
        email_template = Text.template(text=Expr("data['email']"))
        self.assertEqual(
            CompositeTemplate(
                [first_name_template, last_name_template, email_template]
            ),
            name_template + email_template,
        )
        self.assertEqual(
            CompositeTemplate(
                [email_template, first_name_template, last_name_template]
            ),
            email_template + name_template,
        )

    def test_render_composite_template(self):
        first_name_template = Text.template(text=Expr("data['first_name']"))
        last_name_template = Text.template(text=Expr("data['last_name']"))
        name_template = CompositeTemplate([first_name_template, last_name_template])
        name = name_template.render(data={"first_name": "first", "last_name": "last"})
        self.assertEqual(
            [
                Text(type="plain_text", text="first"),
                Text(type="plain_text", text="last"),
            ],
            name,
        )

    def test_template_to_iterable_template(self):
        template = Text.template(text=Expr("value"))
        iterable_template = template.to_iterable_template("texts", "value", True)
        self.assertEqual(
            IterableTemplate("texts", "value", Text.template(text=Expr("value")), True),
            iterable_template,
        )

    def test_composite_template_to_iterable_template(self):
        composite_template = CompositeTemplate([Text.template(text=Expr("value"))])
        iterable_text_template = composite_template.to_iterable_template(
            "texts", "value", True
        )
        self.assertEqual(
            IterableTemplate(
                "texts",
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
