from enum import Enum

class BlockType(Enum):
    PARAGRAPH = super.auto()
    HEADING = super.auto()
    CODE = super.auto()
    QUOTE = super.auto()
    UNORDERED = super.auto()
    ORDERED = super.auto()

def block_to_block_type(md_block):
    if md_block[0] == "#":
        return BlockType.HEADING
    if md_block[:2] == "```" and md_block[-3:] == "```":
        return BlockType.CODE
    if md_block[0] == ">":
        return BlockType.QUOTE
    if md_block[:1] == "- ":
        return BlockType.UNORDERED
    if md_block[:2] == "1. ":
        return BlockType.ORDERED
    return BlockType.PARAGRAPH

