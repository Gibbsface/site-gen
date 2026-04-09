import re
from htmlnode import LeafNode
from textnode import TextType, TextNode

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



