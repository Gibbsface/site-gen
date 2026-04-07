import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")

    def test_full(self):
        node = HTMLNode("h1", "dummy text", [HTMLNode()], {"href": "www.dts.edu"})
        self.assertEqual(str(node), "HTMLNode(h1, dummy text, [HTMLNode(None, None, None, None)], {'href': 'www.dts.edu'})")

    def test_props_to_html(self):
        node = HTMLNode("h1", "dummy text", [HTMLNode()], {"href": "www.dts.edu"})
        dummy = node.props_to_html()
        self.assertEqual(dummy, "href=\"www.dts.edu\" ")

if __name__ == "__main__":
    unittest.main()