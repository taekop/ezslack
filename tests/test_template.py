from unittest import TestCase

from ezslack.schema import Expr, Option, OptionGroup, Section, TemplateList, Text


class TemplateTest(TestCase):
    def test_text(self):
        text_template = Text.template(text=Expr("data['text']"))
        text = text_template.render(data={"text": "ezslack"})
        self.assertEqual(Text(type="plain_text", text="ezslack"), text)

    def test_option_group(self):
        option_group_template = OptionGroup.template(
            label=Text(type="plain_text", text="ezslack"),
            options=TemplateList(
                Expr("options"),
                "option",
                Option.template(
                    text=Text.template(type="plain_text", text=Expr("option['text']")),
                    value=Expr("option['value']"),
                ),
            ),
        )
        option_group = option_group_template.render(
            options=[
                {"text": "text1", "value": "value1"},
                {"text": "text2", "value": "value2"},
            ]
        )
        self.assertEqual(
            OptionGroup(
                label=Text(type="plain_text", text="ezslack"),
                options=[
                    Option(text=Text(type="plain_text", text="text1"), value="value1"),
                    Option(text=Text(type="plain_text", text="text2"), value="value2"),
                ],
            ),
            option_group,
        )

    def test_raise_error_if_neither_provided(self):
        section_template = Section.template()
        self.assertRaises(ValueError, section_template.render)
