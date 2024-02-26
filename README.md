# EzSlack

EzSlack is a Python framework wrapping [Bolt for Python](https://github.com/slackapi/bolt-python) to provide useful utilities.

- Encapsule parsing low-level information
- Provide `Handler` class to improve cohesion

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

Whenever subclass of [`Handler`](ezslack/handler/handler.py) is defined, handler methods are registered in [`REGISTRIES`](ezslack/handler/registry.py#L33). String arguments in handler decorator are automatically converted into regex pattern with anchors. Matched groups are passed to arguments and keyword arguments whether they are named.

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

## Supported features

Requests supported: `ACTION`, `MESSAGE`, `VIEW_CLOSED`, `VIEW_SUBMISSION`

Each request has an id such as `action_id`, `message.text`, `callback_id`. When a request id matches handling method's regex pattern, handler is instantiated with the following context fields, then call the method.

|       field        |         type          |                                         description                                          |                   event                    |
| :----------------: | :-------------------: | :------------------------------------------------------------------------------------------: | :----------------------------------------: |
|       `ack`        |         `Ack`         |        See [Reference](https://github.com/slackapi/bolt-python#making-things-happen)         |                     -                      |
|      `client`      |      `WebClient`      |        See  [Reference](https://github.com/slackapi/bolt-python#making-things-happen)        |                     -                      |
|     `respond`      |       `Respond`       |        See  [Reference](https://github.com/slackapi/bolt-python#making-things-happen)        |                     -                      |
|       `say`        |         `Say`         |        See  [Reference](https://github.com/slackapi/bolt-python#making-things-happen)        |                     -                      |
|    `channel_id`    |    `Optional[str]`    |                            Channel where the event was triggered                             |            `ACTION`, `MESSAGE`             |
|   `channel_name`   |    `Optional[str]`    |                            Channel where the event was triggered                             |                 `MESSAGE`                  |
|    `message_ts`    |    `Optional[str]`    |                                   Timestamp of the message                                   |            `ACTION`, `MESSAGE`             |
|     `metadata`     | `Optional[Metadata]`  |                                   Metadata of the message                                    |                  `ACTION`                  |
| `private_metadata` |    `Optional[str]`    |                                 Private metadata of the view                                 |      `VIEW_SUBMISSION`, `VIEW_CLOSED`      |
|    `request_id`    |         `str`         | Identifier such as `action_id`, `message.text`, `callback_id` which is used to match handler |                     -                      |
|    `thread_ts`     |    `Optional[str]`    |                                   Timestamp of the thread                                    |            `ACTION`, `MESSAGE`             |
|    `trigger_id`    |    `Optional[str]`    |                                  Trigger id from the event                                   |                  `ACTION`                  |
|     `user_id`      |    `Optional[str]`    |                                 User who triggers the event                                  |                     -                      |
|    `user_name`     |    `Optional[str]`    |                                 User who triggers the event                                  | `ACTION`, `VIEW_SUBMISSION`, `VIEW_CLOSED` |
|      `bot_id`      |    `Optional[str]`    |                                 Bot which triggers the event                                 |                 `MESSAGE`                  |
|    `view_state`    | `Optional[ViewState]` |                             View state which has selected values                             |      `VIEW_SUBMISSION`, `VIEW_CLOSED`      |
