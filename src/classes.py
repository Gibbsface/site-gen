from enum import Enum, auto
from decoration import decorated_text_to_html
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
    QUOTE = auto()
    UNORDERED = auto()


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
                self.html = self.header_to_html(block.content)
            case BlockType.CODE:
                self.html = self.code_to_html(block.content)
            case BlockType.PARAGRAPH:
                self.html = self.paragraph_to_html(block.content)
            case BlockType.IMAGE:
                self.html = self.image_to_html(block.content)
            case BlockType.QUOTE:
                self.html = self.quote_to_html(block.content)
            case BlockType.UNORDERED:
                self.html = self.unordered_to_html(block.content)

    #TODO
    def unordered_to_html(self, s):
        ans = ""
        for line in s.split("\n"):
            if len(line) < 3:
                continue
            line = decorated_text_to_html(line[2:])
            line = f"<li>{line}</li>\n"
            ans += line
        ans = f"<ul>\n{ans}</ul>\n"
        return ans

    #DONE 
    def quote_to_html(self, s):
        ans = ""
        lines_list = s.split("\n")

        for line in lines_list:
            if line == "":
                continue
            line = line.replace(">", "", 1)
            line = line.lstrip()
            line += "<br>\n"
            ans += line
        ans = ans[:-5]
        ans = "<blockquote>" + ans + "</blockquote>"
        return ans

    #DONE
    def image_to_html(self, s):
        alt = re.findall(r"\[(.+)\]", s)[0]
        src = re.findall(r"\((.+)\)", s)[0]
        return f"<img src=\"{src}\" alt=\"{alt}\">"

    #DONE
    def code_to_html(self, s):
        return f"<code>{s}</code>"

    #DONE
    def paragraph_to_html(self, s):
        try:
            return f"<p>{decorated_text_to_html(s)}</p>"
        except:
            raise Exception(f"Error: trying to parse paragraph: {s}")

    #DONE
    def header_to_html(self, s):
        try:
            ans = re.findall(r"^(#+) (.+)", s)
            h_size = len(ans[0][0])
            text = ans[0][1]
            
            innerHTML = decorated_text_to_html(text)

            return f"<h{h_size}>{innerHTML}</h{h_size}>"
        except ValueError as e:
            raise e
        except:
            raise Exception(f"Error: trying to parse this as a header \"{s}\"")

    #DONE
    def __repr__(self):
        if len(self.html) < 20:
            return f"Node({self.html})"
        else:
            return f"Node({self.html[0:8]}...{self.html[-8:]})"
        
    #DONE
    def get_HTML(self):
        return self.html