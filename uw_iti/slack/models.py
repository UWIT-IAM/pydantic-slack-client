from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Extra, Field, validator
from pytz import timezone


class SlackFormat:
    @staticmethod
    def link(href, text) -> str:
        return f"<{href} | {text}>"


class SlackBlockType(Enum):
    section = "section"
    mrkdwn = "mrkdwn"
    divider = "divider"
    header = "header"
    image = "image"
    text = "plain_text"
    context = "context"


class APIModel(BaseModel):
    class Config:
        extra = Extra.allow


class Block(APIModel):
    block_type: Union[str, SlackBlockType] = Field(
        default=SlackBlockType.mrkdwn, alias="type"
    )
    text: Optional[Union[str, Block]]


Block.update_forward_refs()


class ImageBlock(Block):
    block_type: Union[str, SlackBlockType] = Field("image", const=True, alias="type")
    # Require alt text to encourage accessibility
    text: str = Field(..., alias="alt_text")
    image_url: str


class ContextBlock(Block):
    block_type: Union[str, SlackBlockType] = Field("context", const=True, alias="type")
    elements: List[Block]

    @validator("elements", each_item=True)
    def validate_elements(cls, item: Block) -> Block:
        if SlackBlockType(item.block_type) not in (
            SlackBlockType.mrkdwn,
            SlackBlockType.text,
            SlackBlockType.image,
        ):
            raise ValueError("context blocks can only contain image and text elements")
        return item


class SectionBlock(Block):
    block_type: Union[str, SlackBlockType] = Field("section", const=True, alias="type")
    fields: List[Block] = []


class PostMessageInput(APIModel):
    timestamp: str = Field(
        default_factory=lambda: datetime.now(tz=timezone("US/Pacific")).isoformat(),
        alias="ts",
    )
    channel: str
    username: str
    icon_emoji: str
    blocks: List[Block]
    text: str


class PostMessageOutput(APIModel):
    class Config(APIModel.Config):
        orm_mode = True

    timestamp: str
    channel: str
    username: str
    blocks: List[Block]
    text: str
    message_id: str
    channel_id: str
