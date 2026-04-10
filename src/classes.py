from enum import Enum, auto
import re

class TextType(Enum):
    PLAIN = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()

class BlockType(Enum):
    HEADING = auto()
    CODE = auto()
    PARAGRAPH = auto()

class Block:
    def __init__(self, content):
        self.content = content
        self.type = self.detect_type(content)

    def __repr__(self):
        return f"Block(type={self.type}, content=\"{self.content[0 : min(10, len(self.content))]}...\")"

    def detect_type(self, content):
        # check heading
        if re.match(r"^#{1,6} ", content) != None:
            return BlockType.HEADING
        
        # check code
        if re.search(r"^```", content) != None:
            return BlockType.CODE
        
        # default is just paragraph
        return BlockType.PARAGRAPH
        




