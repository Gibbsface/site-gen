import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_link_repr(self):
        node = TextNode("Dummy text", TextType.LINK, "www.dts.edu")
        self.assertEqual(str(node), "TextNode(Dummy text, TextType.LINK, www.dts.edu)")

    def test_image_repr(self):
        node = TextNode("dummy image text", TextType.IMAGE, "/path/to/image")
        thingy = "TextNode(dummy image text, TextType.IMAGE, /path/to/image)"
        self.assertEqual(str(node), thingy)


if __name__ == "__main__":
    unittest.main()