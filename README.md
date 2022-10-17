# EzSlack

EzSlack is a Python framework wrapping [Bolt for Python](https://github.com/slackapi/bolt-python) to provide useful utilities.

- Encapsule parsing low-level information
- Provide `Handler` class to improve cohesion
- API schema validation and `Template` support for data integrity

## Get Started

```python
from ezslack import App

# Running over HTTP
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
app.start(PORT)
# Running in Socket Mode
app = App(token=SLACK_BOT_TOKEN)
app.start_socket_mode(SLACK_APP_TOKEN)
```

## Example

```python
from ezslack import Handler, message

class MyHandler(Handler):
    @message("hello (\w+)")
    def on_hello_name(self, name):
        self.ack()
        self.client.chat_postMessage(
            channel=self.channel_id,
            thread_ts=self.thread_ts,
            text=f"Nice to meet you {name}",
        )
```

## Template

You can create `Template` and assign values later. `Template` is `render(**kwargs)` ed by passing binding arguments and corresponding `Expr` expressions are evaluated with those bindings.

On the otherhand, dynamic-size list can be created using `TemplateList`. Instantiating with `iterable: Expr`, `name: str`, `template: Template`, when `iterable` is evaluated into the items, each item is passed into `template` as `name` declared.

```python
from ezslack.schema import Expr, Option, StaticSelect, TemplateList, Text

select_menu_template = StaticSelect.template(
    options=TemplateList(
        Expr("options"),
        "option",
        Option.template(
            text=Text.template(type="plain_text", text=Expr("option['text']")),
            value=Expr("option['value']"),
        ),
    )
)

select_menu = select_menu_template.render(
    options=[
        {"text": "text1", "value": "value1"},
        {"text": "text2", "value": "value2"},
    ]
) # => StaticSelect(
#   options=[
#       Option(text=Text(type="plain_text", text="text1), value="value1"),
#       Option(text=Text(type="plain_text", text="text1), value="value1"),
#   ]
#)
```

## Supported features

Events supported: `ACTION`, `MESSAGE`, `VIEW_SUBMISSION`, `VIEW_CLOSED`

Each event has a request id like `action_id`, `message.text`, `callback_id`, `callback_id`. When a request id matches handling method's regular expression, handler instance with context fields call the method with matched groups as arguments.

|     field      |       type       |                                         description                                          |                   event                    |
| :------------: | :--------------: | :------------------------------------------------------------------------------------------: | :----------------------------------------: |
|  `request_id`  |      `str`       | Identifier such as `action_id`, `message.text`, `callback_id` which is used to match handler |                     -                      |
| `request_type` |  `RequestType`   |            event type enum: `ACTION`, `MESSAGE`, `VIEW_SUBMISSION`, `VIEW_CLOSED`            |                     -                      |
|     `ack`      |      `Ack`       |        See [Reference](https://github.com/slackapi/bolt-python#making-things-happen)         |                     -                      |
|     `body`     | `Dict[str, Any]` |        See  [Reference](https://github.com/slackapi/bolt-python#making-things-happen)        |                     -                      |
|    `client`    |   `WebClient`    |        See  [Reference](https://github.com/slackapi/bolt-python#making-things-happen)        |                     -                      |
|   `respond`    |    `Respond`     |        See  [Reference](https://github.com/slackapi/bolt-python#making-things-happen)        |                     -                      |
|     `say`      |      `Say`       |        See  [Reference](https://github.com/slackapi/bolt-python#making-things-happen)        |                     -                      |
|  `channel_id`  | `Optional[str]`  |                            Channel where the event was triggered                             |            `ACTION`, `MESSAGE`             |
| `channel_name` | `Optional[str]`  |                            Channel where the event was triggered                             |                 `MESSAGE`                  |
|  `message_ts`  | `Optional[str]`  |                                   Timestamp of the message                                   |            `ACTION`, `MESSAGE`             |
|  `thread_ts`   | `Optional[str]`  |                                   Timestamp of the thread                                    |            `ACTION`, `MESSAGE`             |
|  `trigger_id`  | `Optional[str]`  |                                  Trigger id from the event                                   |                  `ACTION`                  |
|   `user_id`    |      `str`       |                                 User who triggers the event                                  |                     -                      |
|  `user_name`   | `Optional[str]`  |                                 User who triggers the event                                  | `ACTION`, `VIEW_SUBMISSION`, `VIEW_CLOSED` |
