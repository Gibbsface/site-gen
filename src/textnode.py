from enum import Enum

class TextType(Enum):
    TEXT = ""
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "[ANCHOR](URL)"
    IMAGE = "![ALT](URL)"

class TextNode:
    def __init__(self, text, type, url=None):
        self.text = text
        self.type = type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and
                self.type == other.type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"
    