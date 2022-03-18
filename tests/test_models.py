import pytest
from pydantic import ValidationError

from uw_iti.slack.models import Block, ContextBlock, SlackBlockType


class TestContextBlock:
    @pytest.mark.parametrize(
        "block_type",
        [
            SlackBlockType.header,
            SlackBlockType.divider,
            SlackBlockType.context,
            SlackBlockType.section,
        ],
    )
    def test_validate_elements_fails(self, block_type):
        with pytest.raises(ValidationError):
            ContextBlock(elements=[Block.construct(block_type=block_type)])
