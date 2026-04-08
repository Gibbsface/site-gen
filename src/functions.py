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
        print(tokens)

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


a = [TextNode("This is text with a `code block` word", TextType.TEXT)]      
print(split_nodes_delimiter(a, "`", TextType.CODE))