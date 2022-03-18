from typing import Optional

from slack_sdk import WebClient

from uw_iti.slack.models import PostMessageInput, PostMessageOutput


class SlackClient:
    def __init__(self, token: str, default_channel: Optional[str] = None):
        self._client = WebClient(token)
        self.default_channel = default_channel

    def post_message(self, request_input: PostMessageInput) -> PostMessageOutput:
        output = PostMessageOutput.construct(**request_input.dict())
        payload = request_input.dict(by_alias=True, exclude_none=True)
        response = self._client.chat_postMessage(**payload)
        output.message_id = response.data["message"]["ts"]
        output.channel_id = response.data["channel"]
        return output
