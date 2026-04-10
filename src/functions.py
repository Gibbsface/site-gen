import re

from classes import *

###########################

def markdown_to_blocks(md):
    # check if empty
    if md == "":
        raise Exception("Invalid md: md cannot be an empty string")
    
    # code blocks need to be detected first so that we don't parse them into smaller blocks
    ans = separate_code_blocks_from_md(md)

    #TODO right now, ans is a list of alternating code-block-strings and paragraph-strings.
    # the paragraph strings need to be exploded into lists of blocks
    # this function should eventually return ans when it is a list of Blocks()
    
    # # split into a list of block-strings
    # try:
    #     ans = md.split("\n\n")
    #     ans = list(map(lambda x: x.strip(), ans))
    #     ans = list(filter(lambda x: x != "", ans))
    # except:
    #     raise Exception("Invalid md: could not split into a list of block-strings")
    
    # # map list-of-strings to list-of-Blocks, calling constructor on each Block
    # ans = list(map(lambda x: Block(x), ans))
    
    # return ans

            
def separate_code_blocks_from_md(md):
    code_str = ""
    ans = []
    in_code_block = False
    for line in md.split("\n"):
        if not in_code_block and line == "```":
            # entering into code block
            code_str = "```\n"
            in_code_block = True
        elif in_code_block and line != "```":
            # still in code block
            code_str += line + "\n"
        elif in_code_block and line == "```":
            # exiting code block
            ans.append(code_str + "```")
            in_code_block = False
        else:
            ans.append(line)

    # if you exited that loop while still in a code block, then ``` was not balanced
    if in_code_block:
        raise Exception("Error: invalid md. unbalanced code block")

    # now collapse the other lines
    current_str = ""
    lines_and_code_blocks = ans.copy()
    ans = []
    for line in lines_and_code_blocks:
        if len(line) >= 3 and line[0:3] == "```":
            #code block detected
            ans.append(current_str)
            ans.append(line)
            current_str = ""
        else:
            current_str += line + "\n"
    ans.append(current_str + "\n")
            
    return ans


############################

def text_node_to_html_node(text_node):
    match text_node.type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ans = []

    for n in old_nodes:
        if n.type is not TextType.TEXT:
            ans.append(n)
            continue

        tokens = n.text.split(delimiter)

        if len(tokens) % 2 == 0:
            raise Exception("Error: unmatched delimiter")
        
        in_text = True
        for t in tokens:
            if in_text:
                ans.append(TextNode(t, TextType.TEXT))
                in_text = False
            else:
                ans.append(TextNode(t, text_type))
                in_text = True
                
    return ans

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    ans = []

    change_was_made = False
    for n in old_nodes:
        if n.type is not TextType.TEXT:
            ans.append(n)
            continue

        matches = extract_markdown_images(n.text)
        if len(matches) == 0:
            ans.append(n)
            continue

        change_was_made = True
        match = matches[0]
        hand = n.text.split(f"![{match[0]}]({match[1]})", 1)

        if hand[0] != "":
            ans.append(TextNode(hand[0], TextType.TEXT))

        ans.append(TextNode(match[0], TextType.IMAGE, match[1]))

        if hand[1] != "":
            ans.append(TextNode(hand[1], TextType.TEXT))
        
    return ans if not change_was_made else split_nodes_image(ans)


def split_nodes_link(old_nodes):
    ans = []

    change_was_made = False
    for n in old_nodes:
        if n.type is not TextType.TEXT:
            ans.append(n)
            continue

        matches = extract_markdown_links(n.text)
        if len(matches) == 0:
            ans.append(n)
            continue

        change_was_made = True
        match = matches[0]
        hand = n.text.split(f"[{match[0]}]({match[1]})", 1)

        if hand[0] != "":
            ans.append(TextNode(hand[0], TextType.TEXT))

        ans.append(TextNode(match[0], TextType.LINK, match[1]))

        if hand[1] != "":
            ans.append(TextNode(hand[1], TextType.TEXT))
        
    return ans if not change_was_made else split_nodes_link(ans)


def text_to_textnodes(text):
    ans = [TextNode(text, TextType.TEXT)]
    ans = split_nodes_image(ans)
    ans = split_nodes_link(ans)
    ans = split_nodes_delimiter(ans, "**", TextType.BOLD)
    ans = split_nodes_delimiter(ans, "_", TextType.ITALIC)
    ans = split_nodes_delimiter(ans, "`", TextType.CODE)
    return ans




def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    ans = []
    for b in blocks:
        block_type = block_to_block_type(b)

def block_to_text_node(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return TextNode(block, TextType.TEXT)
        case BlockType.HEADING:
            pass
        case BlockType.CODE:
            pass
        case BlockType.QUOTE:
            pass
        case BlockType.UNORDERED:
            pass
        case BlockType.ORDERED:
            pass
