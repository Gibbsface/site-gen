from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode


def main():
    tn = TextNode("dummy text", TextType.BOLD)
    print(tn)

main()