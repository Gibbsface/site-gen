from enum import Enum, auto
import re

# these are all in-line node types
class TextType(Enum):
    PLAIN = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()

# these are all block-level node types
class BlockType(Enum):
    HEADING = auto()
    CODE = auto()
    PARAGRAPH = auto()
    IMAGE = auto()

class Block:
    def __init__(self, content, type=BlockType.PARAGRAPH):
        self.content = content
        self.type = type

    def __repr__(self):
        return f"Block(type={self.type}, content=\"{self.content[0 : min(10, len(self.content))]}...\")"
        

class Node:
    def __init__(self, block):
        # first make sure this is a Block()
        if not isinstance(block, Block):
            raise Exception(f"Error: cannot construct a Node from a non-block \"{block}\"")
        
        match block.type:
            case BlockType.HEADING:
                self.tag = get_heading_tag(block.content)
                self.props = None
                self.innerHTML = convert_decorations_to_html(block.content)
            case BlockType.CODE:
                self.tag = "code"
                self.props = None
                self.innerHTML = block.content
            case BlockType.PARAGRAPH:
                self.tag = "p"
                self.props = None
                self.innerHTML = convert_decorations_to_html(block.content)
            case BlockType.IMAGE:
                self.tag = "img"
                self.props = get_img_props(block.content)
                self.innerHTML = None

    def to_HTML(self):
        # this will output valid HTML of this node and all of its "children"
        pass