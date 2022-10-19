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

## Handler

Whenever subclass of `Handler` is defined, handler methods are registered in [`HANDLER_REGISTRY`](ezslack/handler.py#L44). String arguments in handler decorator are automatically converted into regex pattern with anchors. Matched groups are passed to arguments and keyword arguments whether they are named.

```python
from ezslack import Handler, message

class MyHandler(Handler):
    @message("hello", "hi")
    def greet(self):
        self.ack()
        self.say(
            f"Nice to meet you <@{self.user_id}>",
            thread_ts=self.thread_ts,
        )

    @message(r"(?P<first>\w+)(?P<op>[+*])(?P<second>\w+)")
    def calculate(self, first, second, op):
        if op == "+":
            result = int(first) + int(second)
        else:
            result = int(first) * int(second)
        self.say(f"Result: {result}", thread_ts=self.thread_ts)
```

## Template

`Expr` is simple string class which would be evaluated with given bindings.

```python
from ezslack.schema import Expr

Expr("data").eval(globals={}, locals={"data": "value"})  # => "value"
```

You can create `Template` from `BaseModel` and assign values later. `Template` is `render(**locals)` ed by passing binding arguments, then corresponding `Expr` expressions are evaluated with those bindings.

Complex template can be achived with `ConditionalTemplate`, `CompositeTemplate`, `IterableTemplate`.

`ConditionalTemplate` is rendered same as `Template` or `None` whether condition is evaluated into `True`.

`CompositeTemplate` consists of list of `Template`, `ConditionalTemplate`, `CompositeTemplate`. Simply adding those components would return `CompositeTemplate`.

`IterableTemplate` is rendered into dynamic-size list. When `iterable` is evaluated to the list of values, each value is passed to `template` as `name` declared.

```python
from ezslack.schema import Expr, BaseModel, IterableTemplate

class Text(BaseModel):
    text: str

first_name_template = Text.template(text=Expr("data['first_name']"))
middle_name_template = Text.template(text=Expr("data['middle_name']")).with_condition(
    Expr("'middle_name' in data")
)
last_name_template = Text.template(text=Expr("data['last_name']"))
name_template = first_name_template + middle_name_template + last_name_template
people_template = IterableTemplate(Expr("people"), "data", name_template)
people_template.render(
    people=[
        {"first_name": "John", "last_name": "Smith"},
        {"first_name": "heung", "middle_name": "min", "last_name": "Son"},
    ]
)  # => [[Text(text='John'), Text(text='Smith')], [Text(text='heung'), Text(text='min'), Text(text='Son')]]
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
